from __future__ import absolute_import

import logging

from scrapy.crawler import CrawlerRunner
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


    def crawl_both():
        runner = CrawlerRunner(get_project_settings())
        for location in locations:
            runner.crawl(RecentSpider, location_name=location)
            runner.crawl(DetailedItemsSpider, location_name=location)
        d: defer = runner.join()
        d.addBoth(lambda _: logging.info("Deferred returned that crawling is finished"))


    l = task.LoopingCall(crawl_both)
    l.start(28800)  # call every 8 hours
    reactor.run()
