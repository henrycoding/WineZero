# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WinezeroItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    name = scrapy.Field()
    price = scrapy.Field()
    goodsId = scrapy.Field()
    recentComments = scrapy.Field()
    recentSales = scrapy.Field()
    detail = scrapy.Field()
    score = scrapy.Field()
    rank = scrapy.Field()
    totalSale = scrapy.Field()


