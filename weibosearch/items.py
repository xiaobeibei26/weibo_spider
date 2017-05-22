# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibosearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'weibo'
    id=scrapy.Field()
    url = scrapy.Field()
    user =scrapy.Field()
    content = scrapy.Field()
    comment_count = scrapy.Field()
    forward_count = scrapy.Field()
    like_count =scrapy.Field()
    publish_time = scrapy.Field()
    keyword =scrapy.Field()