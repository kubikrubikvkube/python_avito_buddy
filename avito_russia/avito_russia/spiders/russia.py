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

    def __init__(self, last_stamp: int = None) -> None:
        if last_stamp is None:
            delta_timestamp = datetime.now() - timedelta(minutes=3)
            self.last_stamp = int(datetime.timestamp(delta_timestamp))
        else:
            self.last_stamp = int(last_stamp)
        self.page = 1

    def preserve(self, ad: JSONObject) -> None:
        assert ad['type'] is not None
        assert ad['value'] is not None

        timestamp = None
        if ad['type'] == 'item':
            assert ad['value']['id'] is not None
            timestamp = ad['value']['time']
        elif ad['type'] == 'vip':
            assert ad['value']['list'][0]['value']['id'] is not None
            timestamp = ad['value']['list'][0]['value']['time']
        else:
            pass
            # raise NotImplementedError ?

        if self.last_stamp == timestamp:
            self.page += 1
        else:
            self.last_stamp = timestamp
            self.page = 1

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
        assert json_response is not None
        assert json_response['status'] == 'ok'
        items = json_response['result']['items']
        for item in items:
            self.paginator.preserve(item)
            yield AvitoSimpleAd(item['value'])

        if items:
            yield scrapy.Request(self.paginator.next_url())
