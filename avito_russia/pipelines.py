import logging
import urllib
import uuid
from urllib.parse import parse_qsl, urlparse

import requests

from items import DetailedItem
from phonenumbers import PhoneNumberValidator
from settings import GENDER_RESOLVER_HOST
from spiders import DetailedItemsSpider, AvitoSpider


class DetailedItemSaverPipeline:
    def __init__(self) -> None:
        logging.info("DetailedItemSaverPipeline initialised")

    def process_item(self, raw_item: DetailedItem, spider: AvitoSpider):
        if not isinstance(spider, DetailedItemsSpider):
            logging.debug("DetailedItemSaverPipeline method called not from DetailedItemsSpider")
        elif "seller" not in raw_item:
            logging.debug(f"DetailedItem {raw_item} is not advertisement for sale. Skipping this item")
        else:
            processed_item = {}

            # 0. Prepare nested dicts
            processed_item['seller'] = {}
            processed_item['sharing'] = {}
            processed_item['price'] = {}

            # 1. Preserve categoryId
            processed_item['categoryId'] = raw_item['categoryId']

            # 2. Preserve anonymousNumber
            if 'anonymousNumber' in raw_item:
                processed_item['anonymousNumber'] = raw_item['anonymousNumber']

            # 3. Preserve description
            if 'description' in raw_item:
                processed_item['description'] = raw_item['description']

            # 4. Resolve gender
            if 'seller' in raw_item and 'name' in raw_item['seller']:
                name_request_json = {
                    "name": raw_item['seller']['name']
                }
                r = requests.post(GENDER_RESOLVER_HOST, json=name_request_json)
                if r.status_code == 200:
                    gender = r.json()['gender']
                    if gender != "UNKNOWN":
                        processed_item['gender'] = gender.lower()

            # 5. Resolve coordinates
            processed_item['location'] = {
                "type": "Point",
                "coordinates": [
                    raw_item['coords']['lng'],
                    raw_item['coords']['lat']
                ]
            }

            # 6. Preserve location
            if 'metroId' in raw_item:
                processed_item['metroId'] = raw_item['metroId']

            # 7. Preserve advertisement URL
            if 'sharing' in raw_item and 'url' in raw_item['sharing']:
                processed_item['sharing']['url'] = raw_item['sharing']['url']

            # 8. Preserve parameters
            processed_item['parameters'] = raw_item['parameters']

            # 9. Decode phonenumber
            decoded_phone_number = DetailedItem.decode_phone_number(raw_item)
            if decoded_phone_number and PhoneNumberValidator.is_valid(decoded_phone_number):
                processed_item['phoneNumber'] = decoded_phone_number

            # 10. Preserve seller manager name
            if 'seller' in raw_item and 'manager' in raw_item['seller']:
                processed_item['seller']['manager'] = raw_item['seller']['manager']

            # 11. Preserve shopId
            if 'shopId' in raw_item:
                processed_item['shopId'] = raw_item['shopId']

            # 12. Resolve price
            invalid_price_values = ["Цена не указана", "Договорная", "Бесплатно"]
            price = raw_item['price']['value']
            if not invalid_price_values.count(price):
                processed_item['price']['value'] = int(price.replace(" ", ""))

            # 13. Preserve seller name
            if 'seller' in raw_item and 'name' in raw_item['seller']:
                processed_item['seller']['name'] = raw_item['seller']['name']

            # 14. Preserve userHashId
            if raw_item['seller'] and raw_item['seller']['userHashId']:
                processed_item['seller']['userHashId'] = raw_item['seller']['userHashId']

            # 15. Preserve seller userkey
            if 'seller' in raw_item and 'userKey' in raw_item['seller']:
                processed_item['seller']['userKey'] = raw_item['seller']['userKey']

            # 16. Preserve timestamp
            processed_item['time'] = raw_item['time']

            # 17. Preserve title
            processed_item['title'] = raw_item['title']

            # 18. Preserve description
            if 'description' in raw_item:
                processed_item['description'] = raw_item['description']

            # 19. Preserve userType
            processed_item['userType'] = raw_item['userType']

            # 20. Resolve UUID
            processed_item['uuid'] = str(uuid.uuid4())

            # 21. Resolve userKey
            if raw_item['userType'] == 'private' and raw_item['seller']['link']:
                r = urllib.parse.unquote_plus(raw_item['seller']['link'])
                q2 = parse_qsl(urlparse(r).query)
                userKey = str(q2[0][1]).strip()
                processed_item['seller']['userKey'] = userKey

            # 22. Mark format version
            processed_item['formatVersion'] = '1.2'

            # logging.debug(f"Processing {processed_item}")
            logging.debug(f"Processing {processed_item['uuid']}")
            spider.detailed_collection.insert_one(processed_item)
