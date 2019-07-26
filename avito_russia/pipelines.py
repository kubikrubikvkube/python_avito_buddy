import logging
import uuid
from uuid import SafeUUID

from avito_russia import NamesDatabase
from items import DetailedItem
from spiders import DetailedItemsSpider

names_db = NamesDatabase()


class DetailedItemSaverPipeline:
    def __init__(self) -> None:
        logging.info("DetailedItemSaverPipeline initialised")

    def process_item(self, item, spider):
        if not isinstance(spider, DetailedItemsSpider):
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


            item_json = dict(item)
            logging.debug(f"Processing {item_json}")
            spider.detailed_collection.insert_one(item_json)
