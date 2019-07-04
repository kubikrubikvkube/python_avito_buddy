from __future__ import absolute_import

import json
import logging
from urllib import parse

import psycopg2
import pymongo
import scrapy
from psycopg2._psycopg import connection
from pymongo.errors import DuplicateKeyError
from scrapy.exceptions import CloseSpider

from ..settings import API_KEY, POSTGRES_DBNAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, \
    BROKEN_ADS_THRESHOLD

logger = logging.getLogger("DetailedItemsSpider")
logger.setLevel(level=logging.DEBUG)

class DetailedItemsSpider(scrapy.Spider):
    name = 'detailed'
    allowed_domains = ['m.avito.ru']
    url_pattern = f"https://m.avito.ru/api/13/items/__id__?key={API_KEY}&action=view"
    connection: connection


    def __init__(self, name=None, **kwargs):
        logging.info(f"DetailedItemsSpider initialized")
        logger.info("Trying to establish PostgreSQL connection")
        self.connection = psycopg2.connect(dbname=POSTGRES_DBNAME, user=POSTGRES_USER,
                                           password=POSTGRES_PASSWORD, host=POSTGRES_HOST)
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT to_regclass('{POSTGRES_DBNAME}');")
            is_exists = cursor.fetchone()[0] is not None
            logger.info(f"Table {POSTGRES_DBNAME} exists {is_exists}")
            assert is_exists
        logger.info("PostgreSQL DB connection opened")

        self.client = pymongo.MongoClient()
        avito_db = self.client["avito"]
        self.detailed_collection = avito_db["detailed"]
        logger.info("MongoDB connection opened")
        logger.info(f"MongoDB server info: {self.client.server_info()}")

        self.parsed_items = 0
        self.broken_ads = 0
        self.broken_ads_in_a_row = 0
        self.ids = []
        super().__init__(name, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super().from_crawler(crawler, *args, **kwargs)

    def start_requests(self):
        self.logger.debug(f'Starting requests processing')
        self.start_urls = [self.next_url()]
        return super().start_requests()

    def next_url(self) -> str:
        if not self.ids:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {POSTGRES_DBNAME} WHERE is_detailed = False ORDER BY random() LIMIT 50")
                # TODO если программа завершает свою работу до окончания обработки пачки id'шников они
                # TODO оставшиеся айдишники никогда не будут обработаны
                for raw_id in cursor:
                    id = raw_id[0]
                    self.ids.append(id)
                for id in self.ids:
                    cursor.execute(f"UPDATE {POSTGRES_DBNAME} SET is_detailed = True WHERE id = {id}")
                    cursor.connection.commit()
        return f"https://m.avito.ru/api/13/items/{self.ids.pop(0)}?key={API_KEY}&action=view"

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        self.logger.debug(f'Parsing response {json_response}')
        try:
            if response.status == 200:
                item_id = json_response['id']
                json_response['_id'] = item_id
                r = self.detailed_collection.insert_one(json_response)
                assert r.inserted_id is not None and r.inserted_id == item_id
                self.broken_ads_in_a_row = 0
            else:
                request_url = response.request.url
                path = parse.urlparse(request_url).path
                item_id = path.split("/")[-1]
                json_response['_id'] = item_id
                r = self.detailed_collection.insert_one(json_response)
                assert r.inserted_id is not None and r.inserted_id == item_id
                self.broken_ads += 1
                self.broken_ads_in_a_row += 1
                print(f"Broken {self.broken_ads},in a row {self.broken_ads_in_a_row}")
        except DuplicateKeyError as dke:
            # переписать логику. Возможно обработано фрагментированно, а значит должны спрашивать монгу
            # о том, обработан ли уже такой id, и если да, то игнорить.
            # Это позволит обрабатывать базу многопоточно.
            print(dke)
            self.broken_ads += 1
            self.broken_ads_in_a_row += 1
            print(f"Broken {self.broken_ads},in a row {self.broken_ads_in_a_row} - DuplicateKeyError")
            logger.error(dke)

        with self.connection.cursor() as cursor:
            cursor.execute(f"UPDATE {POSTGRES_DBNAME} SET is_detailed = True WHERE id = {item_id}")
            cursor.connection.commit()
        self.parsed_items += 1
        print(f"Parsed items {self.parsed_items}")
        if self.broken_ads_in_a_row > BROKEN_ADS_THRESHOLD:
            raise CloseSpider("Broken Ads threshold excedeed")
        else:
            yield scrapy.Request(self.next_url())




    @staticmethod
    def close(spider, reason):
        spider.connection.close()
        is_closed = spider.connection.closed
        logger.info(f"PostgreSQL connection is closed {bool(is_closed)}")
        assert is_closed
        spider.client.close()
        logging.info("MongoDB connection is closed")
        logging.info(f"DetailedItemsSpider closed: {reason}")
        return super().close(spider, reason)
