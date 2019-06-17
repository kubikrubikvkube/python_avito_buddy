# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response


class RussiaSpider(scrapy.Spider):
    name = 'russia'
    allowed_domains = ['m.avito.ru']
    start_urls = ['https://m.avito.ru/']

    def parse(self, response):
        # open_in_browser(response)
        inspect_response(response, self)
