from __future__ import absolute_import

import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from locations import LocationManager
from spiders import RecentSpider, DetailedItemsSpider

if __name__ == '__main__':
    logger = logging.getLogger("RecentSpider")
    logger.setLevel(level=logging.INFO)

    process = CrawlerProcess(get_project_settings())
    logging.info('CrawlerProcess initialized')
    locations = LocationManager().locations_list.keys()
    for location in locations:
        recent_spider = RecentSpider(location_name=location)
        process.crawl(recent_spider, location_name=location)
        detailed_spider = DetailedItemsSpider(location_name=location)
        process.crawl(detailed_spider, location_name=location)
    process.start()
