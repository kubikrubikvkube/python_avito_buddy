import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from avito_russia.avito_russia.spiders.RecentSpider import RecentSpider

if __name__ == '__main__':
    s = get_project_settings()
    process = CrawlerProcess(s)
    logging.info('CrawlerProcess initialized')
    spider = RecentSpider()
    logging.info('RecentSpider initialized')
    process.crawl(spider)
    logging.info('Crawling set-up completed')
    logging.info('Starting CrawlerProcess')
    process.start()
