# -*- coding: utf-8 -*-
import json

import scrapy


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
    start_urls = [None]

    def start_requests(self):
        return super().start_requests()

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        items = json_response['result']['items']
        for item in items:
            yield AvitoSimpleAd(item['value'])
        next_page_url = None
        if items:
            yield scrapy.Request(response.urljoin(next_page_url))
