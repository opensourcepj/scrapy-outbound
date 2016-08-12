# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OutboundarticlesItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    summary = scrapy.Field()
    published = scrapy.Field()
    article_content_goose = scrapy.Field()
    article_content_readability = scrapy.Field()
