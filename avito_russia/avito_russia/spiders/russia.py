# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from json.decoder import JSONObject

import scrapy

from ..items import AvitoSimpleAd


class Paginator:
    url_pattern = 'https://m.avito.ru/api/9/items?key={key}&sort={sort}&locationId={location_id}&page=__page__&lastStamp=__timestamp__&display={display}&limit={limit}'.format(
        key='af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir',
        sort='date',
        location_id='621540',
        display='list',
        limit=99
    )

    def __init__(self) -> None:
        delta_timestamp = datetime.now() - timedelta(minutes=3)
        self.last_stamp = int(datetime.timestamp(delta_timestamp))
        self.page = 1

    def preserve(self, ad: JSONObject) -> None:
        timestamp = None
        if ad['type'] == 'item':
            timestamp = ad['value']['time']
        elif ad['type'] == 'vip':
            timestamp = ad['value']['list'][0]['value']['time']

        if self.last_stamp == timestamp:
            self.increment_page()
        else:
            self.last_stamp = timestamp
            self.page = 1

    def increment_page(self) -> None:
        self.page += 1

    def next_url(self) -> str:
        page = str(self.page)
        last_stamp = str(self.last_stamp)
        return self.url_pattern.replace('__page__', page).replace('__timestamp__', last_stamp)


class RussiaSpider(scrapy.Spider):
    name = 'russia'

    allowed_domains = ['m.avito.ru']
    offset = 30

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.paginator = Paginator()

    def start_requests(self):
        self.start_urls = [self.paginator.next_url()]
        return super().start_requests()

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        items = json_response['result']['items']
        for item in items:
            self.paginator.preserve(item)
            yield AvitoSimpleAd(item['value'])

        if items:
            yield scrapy.Request(self.paginator.next_url())
