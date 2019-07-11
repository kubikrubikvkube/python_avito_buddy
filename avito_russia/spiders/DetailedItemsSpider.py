from __future__ import absolute_import

import json
import logging
from urllib import parse

import pymongo
import scrapy
from psycopg2._psycopg import connection
from pymongo.errors import DuplicateKeyError
from scrapy.exceptions import CloseSpider

from avito_russia.postgres import PostgreSQL
from ..settings import API_KEY, POSTGRES_DBNAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, \
    BROKEN_ADS_THRESHOLD


class DetailedItemsSpider(scrapy.Spider):
    name = 'detailed'
    allowed_domains = ['m.avito.ru']
    url_pattern = f"https://m.avito.ru/api/13/items/__id__?key={API_KEY}&action=view"
    db_connection: connection


    def __init__(self, name=None, **kwargs):
        logging.info(f"DetailedItemsSpider initialized")
        logging.info("Trying to establish PostgreSQL db_connection")
        self.pgsql = PostgreSQL(POSTGRES_DBNAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST)
        assert self.pgsql.is_table_exists(POSTGRES_DBNAME)
        logging.info("PostgreSQL DB db_connection opened")

        self.client = pymongo.MongoClient()
        avito_db = self.client["avito"]
        self.detailed_collection = avito_db["detailed"]
        logging.info("MongoDB db_connection opened")
        logging.info(f"MongoDB server info: {self.client.server_info()}")

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
            self.ids = ids = self.pgsql.select_items(POSTGRES_DBNAME, False, 25)
            self.pgsql.set_is_detailed(ids, True, POSTGRES_DBNAME)
        return f"https://m.avito.ru/api/13/items/{self.ids.pop(0)}?key={API_KEY}&action=view"

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        self.logger.debug(f'Parsing response {json_response}')
        try:
            if response.status == 200:
                item_id = json_response['id']
                json_response['_id'] = item_id
                r = self.detailed_collection.insert_one(json_response)
                self.broken_ads_in_a_row = 0
            else:
                request_url = response.request.url
                path = parse.urlparse(request_url).path
                item_id = path.split("/")[-1]
                json_response['_id'] = item_id
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
            logging.error(dke)

        with self.pgsql.db_connection.cursor() as cursor:
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
        spider.pgsql.db_connection.close()
        is_closed = spider.pgsql.db_connection.closed
        logging.info(f"PostgreSQL db_connection is closed {bool(is_closed)}")
        assert is_closed
        spider.client.close()
        logging.info("MongoDB db_connection is closed")
        logging.info(f"DetailedItemsSpider closed: {reason}")
        return super().close(spider, reason)
