"""
Avito AvitoSimpleAds processing pipelines
"""

import logging
import sqlite3
from abc import ABC, abstractmethod
from typing import List

import psycopg2 as psycopg2
import pymongo as pymongo
import requests
from scrapy.exceptions import DropItem

from .items import AvitoSimpleAd
from .settings import POSTGRES_USER, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_DBNAME, API_KEY, \
    DEFAULT_REQUEST_HEADERS, DROPPED_ITEMS_THRESHOLD

sqlite_logger = logging.getLogger("SQLiteSavingPipeline")
sqlite_logger.setLevel(level=logging.DEBUG)

postgresql_logger = logging.getLogger("PostgreSQLSavingPipeline")
postgresql_logger.setLevel(level=logging.DEBUG)


class DatabaseSavingPipeline(ABC):
    """
    Abstract class for avito saving pipelines to inherit from
    """

    @abstractmethod
    def process_item(self, ad: AvitoSimpleAd, spider) -> AvitoSimpleAd:
        """
        Processing AvitoSimpleAd
        :param ad:
        :param spider:
        :return:
        """

    def convert_ad_item_to_list(self, ad: AvitoSimpleAd) -> List:
        assert ad['id'] is not None
        assert ad['time'] is not None
        return [int(ad['id']), int(ad['time'])]


class SQLiteSavingPipeline(DatabaseSavingPipeline):
    """
    Pipeline to save using SQLite database
    """

    def process_item(self, ad: AvitoSimpleAd, spider) -> AvitoSimpleAd:
        sqlite_logger.debug(f'Saving {ad} to SQLite DB')
        """
        Saving AvitoSimpleAd using SQLite database
        :param ad:
        :param spider:
        :return:
        """
        list = self.convert_ad_item_to_list(ad)
        self.connection.execute("INSERT INTO avito_simple_ads VALUES (?,?)", list)
        self.connection.commit()
        spider.processed_items += 1
        sqlite_logger.info(f'Processed {spider.processed_items} items')
        return ad

    def open_spider(self, spider) -> None:
        """
        Pipeline constructor. Creating and/or opening DB connection
        :param spider:
        :return:
        """

        self.connection = sqlite3.connect('avito_russia.db')
        sqlite_logger.info("SQLiteSavingPipeline DB connection opened")
        self.connection.execute(
            '''CREATE TABLE IF NOT EXISTS avito_simple_ads(id integer,time integer,is_processed text)''')

    def close_spider(self, spider) -> None:
        """
        Closing pipeline and disconnecting from SQLite database
        :param spider:
        :return:
        """

        sqlite_logger.info("SQLiteSavingPipeline closed")
        self.connection.close()


class PostgreSQLSavingPipeline(DatabaseSavingPipeline):

    def __init__(self) -> None:
        self.dropped_items = 0
        self.dropped_items_in_a_row = 0
        self.processed_items = 0
        super().__init__()

    def process_item(self, ad: AvitoSimpleAd, spider) -> AvitoSimpleAd:
        with self.connection.cursor() as cursor:
            request = f"SELECT EXISTS(SELECT id FROM {POSTGRES_DBNAME} WHERE id = %s)"
            cursor.execute(request, [ad['id']])
            exists = cursor.fetchone()[0]
            if exists:
                postgresql_logger.info(f'This ad already indexed and saved to DB {ad}')
                self.dropped_items += 1
                self.dropped_items_in_a_row += 1
                msg = f"Dropped items {self.dropped_items}, dropped items in a row {self.dropped_items_in_a_row}"
                if self.dropped_items_in_a_row > DROPPED_ITEMS_THRESHOLD:
                    spider.should_be_closed = True
                    spider.close_reason = "Dropped Items threshold excedeed"
                print(msg)
                raise DropItem()
            else:
                list = self.convert_ad_item_to_list(ad)
                request = f"INSERT INTO {POSTGRES_DBNAME} VALUES (%s,%s,false)"
                cursor.execute(request, list)
                self.connection.commit()
                self.processed_items += 1
                self.dropped_items_in_a_row = 0
            print(f'Processed {self.processed_items} items')
            postgresql_logger.debug(f'Processed {self.processed_items} items')
            return ad

    def close_spider(self, spider) -> None:
        postgresql_logger.info("Closing PostgreSQLSavingPipeline")
        self.connection.close()

    def _is_table_exists(self, table_name: str) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT to_regclass('{table_name}');")
            result = cursor.fetchone()
            is_table_exists = result[0] is not None
            return is_table_exists

    def open_spider(self, spider) -> None:
        postgresql_logger.info("Starting PostgreSQLSavingPipeline")
        self.connection = psycopg2.connect(dbname=POSTGRES_DBNAME, user=POSTGRES_USER,
                                           password=POSTGRES_PASSWORD, host=POSTGRES_HOST)

        postgresql_logger.info("PostgreSQLSavingPipeline DB connection opened")
        with self.connection.cursor() as cursor:
            is_table_exists = self._is_table_exists(POSTGRES_DBNAME)
            postgresql_logger.debug(f"Is '{POSTGRES_DBNAME}' table exists - {is_table_exists}")
            if not is_table_exists:
                cursor.execute("CREATE TABLE IF NOT EXISTS {}"
                               "(id bigint NOT NULL,"
                               "time bigint,"
                               "is_detailed bool,"
                               "PRIMARY KEY (id)"
                               ")".format(POSTGRES_DBNAME))
                is_exists_after = self._is_table_exists(POSTGRES_DBNAME)
                assert is_exists_after
                info_msg = f"Is '{POSTGRES_DBNAME}' table exists after CREATE TABLE execution - {is_exists_after}"
                cursor.execute(f"CREATE UNIQUE INDEX idx_id ON {POSTGRES_DBNAME}(id);")
                cursor.execute(f"CREATE INDEX idx_time ON {POSTGRES_DBNAME}(time);")
                cursor.execute(f"CREATE INDEX idx_is_detailed ON {POSTGRES_DBNAME}(is_detailed);")
                postgresql_logger.debug(info_msg)
            self.connection.commit()


class MongoDBSavingPipeline(DatabaseSavingPipeline):
    def open_spider(self, spider) -> None:
        self.client = pymongo.MongoClient()
        avito_db = self.client["avito"]
        self.detailed_collection = avito_db["detailed"]

    def close_spider(self, spider) -> None:
        self.client.close()

    def process_item(self, ad: AvitoSimpleAd, spider):
        url = f"https://m.avito.ru/api/13/items/{ad['id']}?key={API_KEY}&action=view"
        result = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
        assert result.status_code == 200
        result_json = result.json()
        result_json['_id'] = ad['id']
        r = self.detailed_collection.insert_one(result_json)
        assert r.inserted_id is not None
        return ad
