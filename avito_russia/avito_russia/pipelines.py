# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

logger = logging.getLogger('avito_russia.pipelines')


class AvitoRussiaPipeline(object):
    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        logger.warning("AvitoRussiaPipeline opened")

    def close_spider(self, spider):
        logger.warning("AvitoRussiaPipeline closed")
