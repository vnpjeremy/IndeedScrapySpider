# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.markup import remove_tags


class LearnScrapyPipeline(object):
    def process_item(self, item, spider):
        item['company'] = item['company'][0]
        item['company'] = remove_tags(item['company'])
        item['company'] = item['company'].lstrip('\n ')

        item['job_title'] = item['job_title'][0]
        item['location'] = item['location'][0]
        item['date'] = item['date'][0]

        return item
