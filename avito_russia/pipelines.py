import logging

from spiders import DetailedItemsSpider


class DetailedItemSaverPipeline(object):

    def process_item(self, item, spider):
        if not isinstance(spider, DetailedItemsSpider):
            pass
        else:
            item_json = dict(item)
            logging.debug(f"Processing {item_json}")
            spider.detailed_collection.insert_one(item_json)
