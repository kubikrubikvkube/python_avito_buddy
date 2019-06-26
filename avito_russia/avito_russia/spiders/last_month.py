# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime, timedelta
from json.decoder import JSONObject

import scrapy
from scrapy.exceptions import NotSupported

from ..items import AvitoSimpleAd
from ..settings import API_KEY

logging.disable()


class LastMonthSpider(scrapy.Spider):
    name = 'last_month'
    allowed_domains = ['m.avito.ru']
    url_pattern = 'https://m.avito.ru/api/9/items?key={key}&sort={sort}&locationId={location_id}&page=__page__&lastStamp=__timestamp__&display={display}&limit={limit}'.format(
        key=API_KEY,
        sort='date',
        location_id='621540',
        display='list',
        limit=99)

    def __init__(self):
        super().__init__()
        delta_timestamp = datetime.now() - timedelta(minutes=3)
        self.last_stamp = int(datetime.timestamp(delta_timestamp))
        self.page = 1

    def preserve(self, ad: JSONObject) -> None:
        logging.debug(ad)

        if ad['type'] == 'item' or ad['type'] == 'xlItem':
            timestamp = ad['value']['time']
        elif ad['type'] == 'vip':
            timestamp = ad['value']['list'][0]['value']['time']
        else:
            raise NotSupported()

        if self.last_stamp == timestamp:
            self.page += 1
        else:
            self.last_stamp = timestamp
            self.page = 1

    def next_url(self) -> str:
        page = str(self.page)
        last_stamp = str(self.last_stamp)
        return self.url_pattern.replace('__page__', page).replace('__timestamp__', last_stamp)

    def start_requests(self):
        self.start_urls = [self.next_url()]
        return super().start_requests()

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        assert json_response is not None
        assert json_response['status'] == 'ok'
        items = json_response['result']['items']

        for item in items:
            self.preserve(item)
            yield AvitoSimpleAd(item['value'])

        if items:
            yield scrapy.Request(self.next_url())