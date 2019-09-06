from __future__ import absolute_import

import logging
from datetime import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import defer

from locations import LocationManager
from spiders import DetailedItemsSpider, RecentSpider

if __name__ == '__main__':
    logger = logging.getLogger("RecentSpider")
    logger.setLevel(level=logging.INFO)

    logging.info('CrawlerProcess initialized')
    locations = LocationManager().locations_list.keys()

    runner = CrawlerProcess(get_project_settings())


    def crawl():
        logging.info(f"Sleeping 2 minutes at {datetime.now()} to avoid avito throttling")
        # sleep(120)
        for location in locations:
            runner.crawl(RecentSpider, location_name=location)
            runner.crawl(DetailedItemsSpider, location_name=location)
        d: defer = runner.join()
        d.addBoth(lambda _: crawl())


    crawl()
    runner.start(False)
