import json
import logging

import psycopg2
import pymongo
import scrapy
from psycopg2._psycopg import connection

from avito_russia.settings import API_KEY, POSTGRES_DBNAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST

logger = logging.getLogger("DetailedItemsSpider")
logger.setLevel(level=logging.DEBUG)

class DetailedItemsSpider(scrapy.Spider):
    name = 'detailed'
    allowed_domains = ['m.avito.ru']
    url_pattern = f"https://m.avito.ru/api/13/items/__id__?key={API_KEY}&action=view"
    connection: connection

    custom_settings = {}

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
        super().__init__(name, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super().from_crawler(crawler, *args, **kwargs)

    def start_requests(self):
        self.logger.debug(f'Starting requests processing')
        self.start_urls = [self.next_url()]
        return super().start_requests()

    def next_url(self) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {POSTGRES_DBNAME} WHERE is_detailed = False ORDER BY time DESC LIMIT 1")
            raw_result = cursor.fetchone()
            assert raw_result is not None
            id = raw_result[0]
            return f"https://m.avito.ru/api/13/items/{id}?key={API_KEY}&action=view"

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        self.logger.debug(f'Parsing response {json_response}')
        # insert into mongodb
        #
        item_id = json_response['id']
        json_response['_id'] = item_id
        r = self.detailed_collection.insert_one(json_response)
        assert r.inserted_id is not None and r.inserted_id == item_id
        with self.connection.cursor() as cursor:
            cursor.execute(f"UPDATE {POSTGRES_DBNAME} SET is_detailed = True WHERE id = {item_id}")
            cursor.connection.commit()
        self.parsed_items += 1
        print(f"Parsed items {self.parsed_items}")
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
