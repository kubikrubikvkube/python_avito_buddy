# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import scrapy


class RussiaSpiderHelper:
    current_link: str = None

    @classmethod
    def get_key(cls) -> str:
        return 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'

    @staticmethod
    def last_stamp() -> int:
        almost_now = datetime.now() - timedelta(minutes=5)
        timestamp: float = datetime.timestamp(almost_now)
        return int(timestamp)

    @classmethod
    def next_link(cls) -> str:
        if not cls.current_link:
            cls.key = cls.get_key()
            cls.last_stamp = cls.last_stamp()
            cls.page = 0
            cls.limit = 99
        cls.current_link = f'https://m.avito.ru/api/9/items?key={cls.key}&sort=default&locationId=621540&page={cls.page + 1}&lastStamp={cls.last_stamp}&display=list&limit={cls.limit}'
        return cls.current_link


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
    start_urls = [RussiaSpiderHelper.next_link()]

    def start_requests(self):
        return super().start_requests()

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        items = json_response['result']['items']
        for item in items:
            yield AvitoSimpleAd(item['value'])

        next_page_url = RussiaSpiderHelper.next_link()
        if items:
            yield scrapy.Request(response.urljoin(next_page_url))
