from __future__ import absolute_import

import json
import logging

import scrapy
from psycopg2._psycopg import connection
from pymongo.errors import DuplicateKeyError
from scrapy.exceptions import CloseSpider, NotSupported

from avito_russia.mongodb import MongoDB
from locations import LocationManager
from ..settings import API_KEY, BROKEN_ADS_THRESHOLD


class DetailedItemsSpider(scrapy.Spider):
    name = 'detailed'
    allowed_domains = ['m.avito.ru']
    url_pattern = f"https://m.avito.ru/api/13/items/__id__?key={API_KEY}&action=view"
    db_connection: connection

    def __init__(self, name=None, **kwargs):
        logging.info(f"DetailedItemsSpider initialized")
        location_name = kwargs.get("location_name")
        self.location = location = LocationManager().get_location(location_name)
        self.detailedCollection = MongoDB(location.detailedCollectionName)
        self.recentCollection = MongoDB(location.recentCollectionName)
        self.parsed_items = 0
        self.broken_ads = 0
        self.broken_ads_in_a_row = 0
        super().__init__(name, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super().from_crawler(crawler, *args, **kwargs)

    def start_requests(self):
        self.logger.debug(f'Starting requests processing')
        self.start_urls = [self.next_url()]
        return super().start_requests()

    def next_url(self) -> str:
        document = self.recentCollection.collection.find_one_and_update({"isDetailed": {"$ne": True}},
                                                                        {"$set": {"isDetailed": True}})
        if document['type'] == 'item' or document['type'] == 'xlItem':
            id = document['value']['id']
        elif document['type'] == 'vip':
            id = document['value']['list'][0]['value']['id']
        else:
            raise NotSupported()

        return f"https://m.avito.ru/api/13/items/{id}?key={API_KEY}&action=view"

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        self.logger.debug(f'Parsing response {json_response}')
        try:
            if response.status == 200:
                self.detailedCollection.insert_one(json_response)
                self.broken_ads_in_a_row = 0
            else:
                self.broken_ads += 1
                self.broken_ads_in_a_row += 1
                print(f"Broken {self.broken_ads},in a row {self.broken_ads_in_a_row}")
        except DuplicateKeyError as dke:
            logging.warning(dke)
            self.broken_ads += 1
            self.broken_ads_in_a_row += 1
            print(f"Broken {self.broken_ads},in a row {self.broken_ads_in_a_row} - DuplicateKeyError")

        self.parsed_items += 1
        print(f"Parsed items {self.parsed_items}")
        if self.broken_ads_in_a_row > BROKEN_ADS_THRESHOLD:
            raise CloseSpider("Broken Ads threshold excedeed")
        else:
            yield scrapy.Request(self.next_url())

    @staticmethod
    def close(spider, reason):
        logging.info(f"DetailedItemsSpider closed: {reason}")
        return super().close(spider, reason)
