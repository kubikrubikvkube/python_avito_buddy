import logging
import urllib
import uuid
from urllib.parse import parse_qsl, urlparse

from avito_russia import NamesDatabase
from items import DetailedItem
from spiders import DetailedItemsSpider, AvitoSpider

names_db = NamesDatabase()


class DetailedItemSaverPipeline:
    def __init__(self) -> None:
        logging.info("DetailedItemSaverPipeline initialised")

    def process_item(self, item: DetailedItem, spider: AvitoSpider):
        if not isinstance(spider, DetailedItemsSpider):
            logging.debug("DetailedItemSaverPipeline method called not from DetailedItemsSpider")
        elif "seller" not in item:
            logging.debug(f"DetailedItem {item} is not advertisement for sale. Skipping this item")
            pass
        else:
            #Resolve gender
            resolved_gender = names_db.resolve_gender(item['seller']['name'])
            if resolved_gender:
                item['gender'] = resolved_gender
            #Mark UUID
            item['uuid'] = str(uuid.uuid4())

            #Decode phonenumber
            decoded_phone_number = DetailedItem.decode_phone_number(item)
            if decoded_phone_number:
                item['phonenumber'] = decoded_phone_number
            #Set coordinates
            if item['coords']:
                item['location'] = {
                        "type": "Point",
                        "coordinates": [
                            item['coords']['lng'],
                            item['coords']['lat']
                        ]
                }

            #Decode userKey
            if item['userType'] == 'private' and item['seller']['link']:
                r = urllib.parse.unquote_plus(item['seller']['link'])
                q2 = parse_qsl(urlparse(r).query)
                userKey = str(q2[0][1]).strip()
                item['seller']['userKey'] = userKey

            item_json = dict(item)
            logging.debug(f"Processing {item_json}")
            spider.detailed_collection.insert_one(item_json)
