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
from .settings import POSTGRES_USER, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_DBNAME, API_KEY, DEFAULT_REQUEST_HEADERS

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
        id = int(ad['id'])
        category_id = int(ad['category']['id']) if 'category' in ad else None
        category_name = str(ad['category']['name']) if 'category' in ad else None
        location = str(ad['location']) if 'location' in ad else None
        coords_lat = float(ad['coords']['lat']) if 'coords' in ad else None
        coords_lng = float(ad['coords']['lng']) if 'coords' in ad else None
        time = int(ad['time']) if 'time' in ad else None
        title = str(ad['title']) if 'title' in ad else None
        userType = str(ad['userType']) if 'userType' in ad else None
        images = str(ad['images']) if 'images' in ad else None
        services = str(ad['services']) if 'services' in ad else None
        price = str(ad['price']) if 'price' in ad else None
        uri = str(ad['uri']) if 'uri' in ad else None
        uri_mweb = str(ad['uri_mweb']) if 'uri_mweb' in ad else None
        isVerified = str(ad['isVerified']) if 'isVerified' in ad else None
        isFavorite = str(ad['isFavorite']) if 'isFavorite' in ad else None
        return [id, category_id, category_name, location, coords_lat, coords_lng, time, title, userType, images,
                services, price, uri, uri_mweb, isVerified, isFavorite]


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
        self.connection.execute("INSERT INTO avito_simple_ads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", list)
        self.connection.commit()
        self.processed_items += 1
        sqlite_logger.info(f'Processed {self.processed_items} items')
        return ad

    def open_spider(self, spider) -> None:
        """
        Pipeline constructor. Creating and/or opening DB connection
        :param spider:
        :return:
        """

        self.connection = sqlite3.connect('avito_russia.db')
        sqlite_logger.info("SQLiteSavingPipeline DB connection opened")
        self.connection.execute('''CREATE TABLE IF NOT EXISTS avito_simple_ads
                                                    (id integer,
                                                    category_id integer,
                                                    category_name text,
                                                    location text,
                                                    coords_lat real,
                                                    coords_lng real,
                                                    time integer,
                                                    title text,
                                                    userType text,
                                                    images text,
                                                    services text,
                                                    price text,
                                                    uri text,
                                                    uri_mweb text,
                                                    isVerified text,
                                                    isFavorite text)''')
        self.processed_items = 0

    def close_spider(self, spider) -> None:
        """
        Closing pipeline and disconnecting from SQLite database
        :param spider:
        :return:
        """

        sqlite_logger.info("SQLiteSavingPipeline closed")
        self.connection.close()


class PostgreSQLSavingPipeline(DatabaseSavingPipeline):
    def process_item(self, ad: AvitoSimpleAd, spider) -> AvitoSimpleAd:
        list = self.convert_ad_item_to_list(ad)
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT id FROM avito_simple_ads WHERE id = %s)", [ad['id']])
            exists = cursor.fetchone()[0]
            if exists:
                postgresql_logger.info(f'This ad already indexed and saved to DB {ad}')
                print("DropItem")
                raise DropItem()
            else:
                cursor.execute("INSERT INTO avito_simple_ads VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                               list)
                self.connection.commit()
                self.processed_items += 1
            print(f'Processed {self.processed_items} items')
            return ad

    def close_spider(self, spider) -> None:
        postgresql_logger.info("Closing PostgreSQLSavingPipeline")
        self.connection.close()

    def open_spider(self, spider) -> None:
        postgresql_logger.info("Starting PostgreSQLSavingPipeline")
        self.connection = psycopg2.connect(dbname=POSTGRES_DBNAME, user=POSTGRES_USER,
                                           password=POSTGRES_PASSWORD, host=POSTGRES_HOST)

        postgresql_logger.info("PostgreSQLSavingPipeline DB connection opened")
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT to_regclass('{POSTGRES_DBNAME}');")
            result = cursor.fetchone()
            is_table_exists = result[0] is not None
            postgresql_logger.debug(f'Is {POSTGRES_DBNAME} table exists - {is_table_exists}')
            cursor.execute('''CREATE TABLE IF NOT EXISTS avito_simple_ads
                                                                (id bigint NOT NULL,
                                                                category_id integer,
                                                                category_name text,
                                                                location text,
                                                                coords_lat float8,
                                                                coords_lng float8,
                                                                time bigint,
                                                                title text,
                                                                userType text,
                                                                images text,
                                                                services text,
                                                                price text,
                                                                uri text,
                                                                uri_mweb text,
                                                                isVerified bool,
                                                                isFavorite bool, PRIMARY KEY (id))''')

            self.connection.commit()
            self.processed_items = 0


class MongoDBSavingPipeline(DatabaseSavingPipeline):
    def open_spider(self, spider) -> None:
        self.client = pymongo.MongoClient()

    def close_spider(self, spider) -> None:
        self.client.close()

    def process_item(self, ad: AvitoSimpleAd, spider):
        url = f"https://m.avito.ru/api/13/items/{ad['id']}?key={API_KEY}&action=view"
        result = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
        assert result.status_code == 200
        result_json = result.json()
        result_json['_id'] = ad['id']
        avito_db = self.client["avito"]
        detailed_collection = avito_db["detailed"]
        r = detailed_collection.insert_one(result_json)
        assert r.inserted_id is not None
