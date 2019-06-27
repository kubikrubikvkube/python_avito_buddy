import logging

import psycopg2
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

    custom_settings = {
        'ITEM_PIPELINES': {
            'avito_russia.pipelines.MongoDBSavingPipeline': 0,
        }
    }

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
        super().__init__(name, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super().from_crawler(crawler, *args, **kwargs)

    def start_requests(self):
        self.logger.debug(f'Starting requests processing')
        # Scrapy calls it only once, so it is safe to implement start_requests() as a generator.
        # генератор всех ссылок в постгресе с учётом дублирования
        return []

    def parse(self, response):
        self.logger.debug(f'Parsing response {response}')
        pass

    @staticmethod
    def close(spider, reason):
        spider.connection.close()
        is_closed = spider.connection.closed
        logger.info(f"PostgreSQL connection is closed {bool(is_closed)}")
        assert is_closed
        logging.info(f"DetailedItemsSpider closed: {reason}")
        return super().close(spider, reason)
