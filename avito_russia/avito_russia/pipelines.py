# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import sqlite3

from .items import AvitoSimpleAd

logger = logging.getLogger('avito_russia.pipelines')


class SQLiteSavingPipeline(object):

    def process_item(self, ad: AvitoSimpleAd, spider):
        cursor = self.connection.cursor()
        id = int(ad['id']) if 'id' in ad else None
        category = str(ad['category']) if 'category' in ad else None
        location = str(ad['location']) if 'location' in ad else None
        coords = str(ad['coords']) if 'coords' in ad else None
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

        cursor.execute("INSERT INTO avito_simple_ads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       [
                           id,
                           category,
                           location,
                           coords,
                           time,
                           title,
                           userType,
                           images,
                           services,
                           price,
                           uri,
                           uri_mweb,
                           isVerified,
                           isFavorite,
                       ]
                       )
        self.connection.commit()
        self.processed_items += 1
        logger.info('Processed %s items', self.processed_items)
        return ad

    def open_spider(self, spider):
        logger.info("SQLiteSavingPipeline opened")
        self.connection = sqlite3.connect('avito_russia.db')
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS avito_simple_ads
                             (id integer,
                             category text,
                             location text,
                             coords text,
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



    def close_spider(self, spider):
        logger.info("SQLiteSavingPipeline closed")
        self.connection.close()
