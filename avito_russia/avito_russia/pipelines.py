"""
Avito AvitoSimpleAds processing pipelines
"""

import logging
import sqlite3
from abc import ABC, abstractmethod
from typing import List

import psycopg2 as psycopg2

from .items import AvitoSimpleAd
from .settings import POSTGRES_USER, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_DBNAME

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


class SavingPipeline(ABC):
    """
    Abstract class for avito saving pipelines to inherit from
    """

    @abstractmethod
    def process_item(self, ad: AvitoSimpleAd, spider):
        """
        Processing AvitoSimpleAd
        :param ad:
        :param spider:
        :return:
        """

    def ad_item_to_list(self, ad: AvitoSimpleAd) -> List:
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


class SQLiteSavingPipeline(SavingPipeline):
    """
    Pipeline to save using SQLite database
    """

    def process_item(self, ad: AvitoSimpleAd, spider) -> AvitoSimpleAd:
        logger.debug(f'Saving {ad} to SQLite DB')
        """
        Saving AvitoSimpleAd using SQLite database
        :param ad:
        :param spider:
        :return:
        """
        list = self.ad_item_to_list(ad)
        self.connection.execute("INSERT INTO avito_simple_ads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", list)
        self.connection.commit()
        self.processed_items += 1
        logger.info(f'Processed {self.processed_items} items')
        return ad

    def open_spider(self, spider) -> None:
        """
        Pipeline constructor. Creating and/or opening DB connection
        :param spider:
        :return:
        """

        self.connection = sqlite3.connect('avito_russia.db')
        logger.info("SQLiteSavingPipeline DB connection opened")
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

        logger.info("SQLiteSavingPipeline closed")
        self.connection.close()


class PostgreSQLSavingPipeline(SavingPipeline):

    def process_item(self, ad: AvitoSimpleAd, spider):
        list = self.ad_item_to_list(ad)
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO avito_simple_ads VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           list)
            self.connection.commit()
            self.processed_items += 1
            logger.info(f'Processed {self.processed_items} items')

    def close_spider(self, spider) -> None:
        self.connection.close()

    def open_spider(self, spider) -> None:
        self.connection = psycopg2.connect(dbname=POSTGRES_DBNAME, user=POSTGRES_USER,
                                           password=POSTGRES_PASSWORD, host=POSTGRES_HOST)

        logger.info("PostgreSQLSavingPipeline DB connection opened")
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT to_regclass('{POSTGRES_DBNAME}');")
            result = cursor.fetchone()
            is_table_exists = result[0] is not None
            print(f'Is table exists {is_table_exists}')
            cursor.execute('''CREATE TABLE IF NOT EXISTS avito_simple_ads
                                                                (id bigint,
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
                                                                isFavorite bool)''')

            self.connection.commit()
            self.processed_items = 0
