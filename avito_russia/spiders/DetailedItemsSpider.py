import logging
from json.decoder import JSONObject

import scrapy

from avito_russia.settings import API_KEY


class DetailedItemsSpider(scrapy.Spider):
    name = 'detailed'
    allowed_domains = ['m.avito.ru']
    url_pattern = f"https://m.avito.ru/api/13/items/__id__?key={API_KEY}&action=view"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        logging.info(f"DetailedItemsSpider initialized")
        return super().from_crawler(crawler, *args, **kwargs)

    def preserve(self, ad: JSONObject) -> None:
        pass

    def start_requests(self):
        self.logger.debug(f'Starting requests processing')
        # Scrapy calls it only once, so it is safe to implement start_requests() as a generator.
        # генератор всех ссылок в постгресе с учётом дублирования
        return []

    def parse(self, response):
        self.logger.debug(f'Parsing response {response}')
        pass

    @staticmethod
    def close(spider, reason):
        logging.info(f"DetailedItemsSpider closed: {reason}")
        return super().close(spider, reason)
