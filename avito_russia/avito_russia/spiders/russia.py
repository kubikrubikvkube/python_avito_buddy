# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import scrapy


class Paginator:
    url_pattern = 'https://m.avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&sort=date&locationId=621540&page={page}&lastStamp={timestamp}&display=list&limit=99'

    def __init__(self) -> None:
        delta_timestamp = datetime.now() - timedelta(minutes=3)
        self.last_stamp = int(datetime.timestamp(delta_timestamp))
        self.page = 1
        self.uris = []

    def preserve(self, ad_json) -> None:
        uri = None
        timestamp = None
        if ad_json['type'] == 'item':
            uri = ad_json['value']['uri']
            timestamp = ad_json['value']['time']
        elif ad_json['type'] == 'vip':
            uri = ad_json['value']['list'][0]['value']['uri']
            timestamp = ad_json['value']['list'][0]['value']['time']

        if uri in self.uris:
            print(f'Last stamp is {self.last_stamp}')
            self.last_stamp = timestamp
            print(f'Page is {self.page}')
            self.page = 0
        else:
            print('Not in self.uris')
            print(f'Appending uri {uri}')
            self.uris.append(uri)
            self.page += 1
            print(f'Page is {self.page}')

    def next_url(self) -> str:
        page = str(self.page)
        last_stamp = str(self.last_stamp)
        return self.url_pattern.replace('{page}', page).replace('{timestamp}', last_stamp)


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

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.paginator = Paginator()

    def start_requests(self):
        self.start_urls = []
        self.start_urls.append(self.paginator.next_url())
        return super().start_requests()

    def parse(self, response):
        print(response)
        json_response = json.loads(response.body_as_unicode())
        items = json_response['result']['items']
        for item in items:
            self.paginator.preserve(item)
            yield AvitoSimpleAd(item['value'])
        next_url = self.paginator.next_url()
        if items:
            yield scrapy.Request(response.urljoin(next_url))
