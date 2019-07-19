# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging
from datetime import datetime, timedelta
from json.decoder import JSONObject

import scrapy
from scrapy.exceptions import NotSupported, CloseSpider

from avito_russia.mongodb import MongoDB
from locations import LocationManager
from ..settings import API_KEY, BROKEN_ADS_THRESHOLD


class RecentSpider(scrapy.Spider):
    name = 'recent'
    allowed_domains = ['m.avito.ru']

    def __init__(self, *args, **kwargs):
        super().__init__()
        delta_timestamp = datetime.now() - timedelta(minutes=3)
        self.last_stamp = int(datetime.timestamp(delta_timestamp))
        self.page = 1
        self.broken_ads = 0
        self.broken_ads_in_a_row = 0
        self.location = location = LocationManager().get_location(kwargs.get("location_name"))
        self.recent_collection = MongoDB(location.recentCollectionName)
        self.detailed_collection = MongoDB(location.detailedCollectionName)
        self.url_pattern = 'https://m.avito.ru/api/9/items?key={key}&sort={sort}&locationId={location_id}&page=__page__&lastStamp=__timestamp__&display={display}&limit={limit}'.format(
            key=API_KEY,
            sort='date',
            location_id=location.id,
            display='list',
            limit=99)

    def preserve(self, ad: JSONObject) -> None:
        logging.debug(ad)

        if ad['type'] == 'item' or ad['type'] == 'xlItem':
            timestamp = ad['value']['time']
            id = ad['value']['id']
        elif ad['type'] == 'vip':
            timestamp = ad['value']['list'][0]['value']['time']
            id = ad['value']['list'][0]['value']['id']
        else:
            raise NotSupported()

        if self.last_stamp == timestamp:
            self.page += 1
        else:
            self.last_stamp = timestamp
            self.page = 1

        if self.recent_collection.collection.find_one({'value.id': id}):
            self.broken_ads += 1
            self.broken_ads_in_a_row += 1
        else:
            self.broken_ads_in_a_row = 0
            self.recent_collection.collection.insert_one(ad)

        if self.broken_ads_in_a_row > BROKEN_ADS_THRESHOLD:
            raise CloseSpider("Broken Ads threshold excedeed")

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

        if items:
            yield scrapy.Request(self.next_url())
