from __future__ import absolute_import

import logging
from time import sleep
from datetime import datetime
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet import task, defer

from locations import LocationManager
from spiders import RecentSpider, DetailedItemsSpider

if __name__ == '__main__':
    logger = logging.getLogger("RecentSpider")
    logger.setLevel(level=logging.INFO)

    logging.info('CrawlerProcess initialized')
    locations = LocationManager().locations_list.keys()

    runner = CrawlerProcess(get_project_settings())


    def crawl():
        logging.info(f"Sleeping 1 minute at {datetime.now()} - just in case")
        sleep(60)
        for location in locations:
            runner.crawl(RecentSpider, location_name=location)
            runner.crawl(DetailedItemsSpider, location_name=location)
        d: defer = runner.join()
        d.addBoth(lambda _: crawl())


    crawl()
    runner.start(False)
