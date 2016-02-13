# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy.item import Item, Field


class LearnScrapyItem(Item):
    job_title = Field()
    company = Field()
    # linkURL = Field()
    location = Field()
    date = Field()
    # summary = Field()
    # print jobTitle
