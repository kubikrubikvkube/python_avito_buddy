from __future__ import absolute_import

import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from avito_russia.spiders.DetailedItemsSpider import DetailedItemsSpider

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    logging.info('CrawlerProcess initialized')
    spider = DetailedItemsSpider()
    logging.info('DetailedItemsSpider initialized')
    process.crawl(spider)
    logging.info('Crawling set-up completed')
    logging.info('Starting CrawlerProcess')
    process.start()
