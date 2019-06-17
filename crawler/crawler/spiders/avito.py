# -*- coding: utf-8 -*-
import scrapy


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['http://avito.ru/']

    def parse(self, response):
        pass
