# -*- coding: utf-8 -*-

import scrapy
from scrapy.utils.response import open_in_browser

from avito_russia.avito_russia.avito_russia_utils import gen_random_string


class RussiaSpider(scrapy.Spider):
    name = 'russia'
    key = gen_random_string(44)
    allowed_domains = ['m.avito.ru']
    start_urls = ['https://m.avito.ru/']

    def parse(self, response):
        open_in_browser(response)
        # inspect_response(response, self)
