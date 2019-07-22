import logging

from avito_russia import NamesDatabase
from spiders import DetailedItemsSpider


class DetailedItemSaverPipeline:
    def __init__(self) -> None:
        logging.info("DetailedItemSaverPipeline initialised")
        self.names_db = NamesDatabase()

    def process_item(self, item, spider):
        if not isinstance(spider, DetailedItemsSpider):
            pass
        else:
            resolved_gender = self.names_db.resolve_gender(item['seller']['name'])
            if resolved_gender:
                item['gender'] = resolved_gender

            item_json = dict(item)
            logging.debug(f"Processing {item_json}")
            spider.detailed_collection.insert_one(item_json)
