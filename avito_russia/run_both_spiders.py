import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from avito_russia.spiders.DetailedItemsSpider import DetailedItemsSpider
from avito_russia.spiders.RecentSpider import RecentSpider

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    logging.info('CrawlerProcess initialized')
    recent_spider = RecentSpider()
    detailed_spider = DetailedItemsSpider()
    process.crawl(recent_spider)
    process.crawl(detailed_spider)
    process.start()
