# -*- coding: utf-8 -*-
import json
import operator
from datetime import datetime, timedelta
from typing import Optional

import scrapy


class RussiaSpiderHelper:
    current_link: str = None
    processed: dict = {}

    @classmethod
    def add_processed(cls, id, timestamp) -> None:
        cls.processed[id] = timestamp

    @classmethod
    def is_processed(cls, id) -> bool:
        return id in cls.processed.keys()

    @classmethod
    def processed_timestamp(cls, id) -> Optional[int]:
        return cls.processed[id]

    @classmethod
    def generate_url(cls) -> str:
        if not cls.processed:
            delta_timestamp = datetime.now() - timedelta(minutes=1)
            timestamp: float = int(datetime.timestamp(delta_timestamp))
            print(f'Initial timestamp is {timestamp}')
            return f'https://m.avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&sort=default&locationId=621540&page=1&lastStamp={timestamp}&display=list&limit=30'
        else:
            sorted_dict = sorted(cls.processed.items(), key=operator.itemgetter(1))
            latest_timestamp = sorted_dict[0][1]
            print(f'Sorted dict value 1 is {latest_timestamp}')
            return f'https://m.avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&sort=default&locationId=621540&page=1&lastStamp={latest_timestamp}&display=list&limit=30'


class AvitoSimpleAd(scrapy.Item):
    type = scrapy.Field()
    id = scrapy.Field()
    userId = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    coords = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    userType = scrapy.Field()
    images = scrapy.Field()
    services = scrapy.Field()
    price = scrapy.Field()
    uri = scrapy.Field()
    uri_mweb = scrapy.Field()
    shop = scrapy.Field()
    background = scrapy.Field()
    isVerified = scrapy.Field()
    isFavorite = scrapy.Field()
    delivery = scrapy.Field()
    description = scrapy.Field()
    callAction = scrapy.Field()
    imageList = scrapy.Field()
    list = scrapy.Field()


class RussiaSpider(scrapy.Spider):
    name = 'russia'

    allowed_domains = ['m.avito.ru']
    offset = 30
    start_urls = [RussiaSpiderHelper.generate_url()]

    def start_requests(self):
        return super().start_requests()

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        items = json_response['result']['items']
        for item in items:
            if item['type'] == 'vip' or RussiaSpiderHelper.is_processed(item['value']['id']):
                pass
            elif item['type'] != 'vip' and not RussiaSpiderHelper.is_processed(item['value']['id']):
                id = item['value']['id']
                timestamp = item['value']['time']
                RussiaSpiderHelper.add_processed(id, timestamp)
            yield AvitoSimpleAd(item['value'])

        next_page_url = RussiaSpiderHelper.generate_url()
        if items:
            yield scrapy.Request(response.urljoin(next_page_url))
