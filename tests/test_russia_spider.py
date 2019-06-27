import unittest

import requests
from scrapy.crawler import CrawlerProcess

from avito_russia.avito_russia.spiders.RecentSpider import RecentSpider


class RussiaTest(unittest.TestCase):
    def test_russia_spider(self):
        response = requests.get('https://m.avito.ru')
        url = response.url

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

        process.crawl(RecentSpider)
        process.start()


if __name__ == '__main__':
    unittest.main()
