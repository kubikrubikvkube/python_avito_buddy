# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AvitoSimpleAd(scrapy.Item):
    type = scrapy.Field()
    id = scrapy.Field()
    userId = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    coords = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    userType = scrapy.Field()
    images = scrapy.Field()
    services = scrapy.Field()
    price = scrapy.Field()
    uri = scrapy.Field()
    uri_mweb = scrapy.Field()
    shop = scrapy.Field()
    background = scrapy.Field()
    isVerified = scrapy.Field()
    isFavorite = scrapy.Field()
    delivery = scrapy.Field()
    description = scrapy.Field()
    callAction = scrapy.Field()
    imageList = scrapy.Field()
    list = scrapy.Field()
