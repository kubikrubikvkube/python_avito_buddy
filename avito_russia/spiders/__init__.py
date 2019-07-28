from __future__ import absolute_import

import json
from datetime import datetime, timedelta
from json.decoder import JSONObject

import scrapy
from bson import ObjectId
from scrapy.exceptions import NotSupported, CloseSpider
from scrapy.http import TextResponse

from items import DetailedItem
from locations import LocationManager
from mongodb import MongoDB
from settings import API_KEY, BROKEN_ADS_THRESHOLD


class AvitoSpider(scrapy.Spider):
    allowed_domains: str = ['m.avito.ru']
    parsed_items: int = 0
    broken_ads: int = 0
    broken_ads_in_a_row: int = 0

    def increment_broken_ads(self) -> None:
        self.broken_ads += 1
        self.broken_ads_in_a_row += 1

    def reset_broken_ads_in_a_row(self) -> None:
        self.broken_ads_in_a_row = 0


class DetailedItemsSpider(AvitoSpider):

    url_pattern = f"https://m.avito.ru/api/13/items/__id__?key={API_KEY}&action=view"

    def __init__(self,*args, **kwargs):
        self.location_name = location_name = kwargs.get("location_name")
        self.name = location_name + "_detailed"
        self.location = location = LocationManager().get_location(location_name)
        self.document_ids_ready_for_processing = []
        self.detailed_collection = MongoDB(location.detailedCollectionName)
        self.recent_collection = MongoDB(location.recentCollectionName)
        self.start_urls = [self.next_url()]
        super().__init__(name=self.name)
        self.logger.info(f"DetailedItemsSpider initialized")



    def next_url(self) -> str:
        if not self.document_ids_ready_for_processing:
            documents = self.recent_collection.collection.find({"isDetailed": {"$ne": True}}).limit(10)
            internal_ids = []
            for document in documents:
                internal_ids.append(document['_id'])
                document_id = DetailedItem.resolve_item_id(document)
                self.document_ids_ready_for_processing.append(document_id)
            for internal_id in internal_ids:
                self.recent_collection.collection.update_one(
                    {"_id": ObjectId(str(internal_id))},
                    {"$set": {"isDetailed": True}})

        if self.document_ids_ready_for_processing:
            return f"https://m.avito.ru/api/13/items/{self.document_ids_ready_for_processing.pop(0)}?key={API_KEY}&action=view"
        else:
            raise CloseSpider(f"All items processed for spider {self.name} - closing detailed spider")


    def parse(self, response:TextResponse):
        self.logger.debug(f'Parsing response {response}')
        if response.status == 200:
            self.reset_broken_ads_in_a_row()
            json_response = json.loads(response.body_as_unicode())

            yield DetailedItem(json_response)
        else:
            self.increment_broken_ads()
            self.logger.info(f"Broken {self.broken_ads},in a row {self.broken_ads_in_a_row}")

        self.parsed_items += 1
        self.logger.info(f"Parsed items {self.parsed_items} for {self.location.detailedCollectionName}")

        if self.broken_ads_in_a_row > BROKEN_ADS_THRESHOLD:
            raise CloseSpider("Broken Ads threshold excedeed")
        else:
            yield scrapy.Request(self.next_url())


class RecentSpider(AvitoSpider):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("location_name") + "_recent"
        delta_timestamp = datetime.now() - timedelta(minutes=3)
        self.last_stamp = int(datetime.timestamp(delta_timestamp))
        self.page = 1
        self.location = location = LocationManager().get_location(kwargs.get("location_name"))
        self.recent_collection = MongoDB(location.recentCollectionName)
        self.detailed_collection = MongoDB(location.detailedCollectionName)
        self.url_pattern = 'https://m.avito.ru/api/9/items?key={key}&sort={sort}&locationId={location_id}&page=__page__&lastStamp=__timestamp__&display={display}&limit={limit}'.format(
            key=API_KEY,
            sort='date',
            location_id=location.id,
            display='list',
            limit=99)
        self.start_urls = [self.next_url()]
        super().__init__(name=self.name)

    def preserve(self, ad: JSONObject) -> None:
        self.logger.debug(ad)

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

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        assert json_response is not None
        assert json_response['status'] == 'ok'
        items = json_response['result']['items']

        for item in items:
            self.preserve(item)

        if items:
            yield scrapy.Request(self.next_url())
