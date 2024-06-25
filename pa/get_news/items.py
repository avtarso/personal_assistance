# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    tags = scrapy.Field()
    author = scrapy.Field()
    quote = scrapy.Field()


class EconomicsItem(scrapy.Item):
    time = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()


class PoliticsItem(scrapy.Item):
    time = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
