from __future__ import absolute_import

import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from avito_russia.spiders.RecentSpider import RecentSpider

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    logging.info('CrawlerProcess initialized')
    recent_spider = RecentSpider(location_name="SAINT-PETERSBURG")

    process.crawl(recent_spider, location_name="SAINT-PETERSBURG")
    # detailed_spider = DetailedItemsSpider()
    # process.crawl(detailed_spider)
    process.start()
