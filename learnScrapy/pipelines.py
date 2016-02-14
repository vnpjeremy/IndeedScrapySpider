# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.markup import remove_tags
from scrapy.exceptions import DropItem


class LearnScrapyPipeline(object):
    def process_item(self, item, spider):
        item['company'] = item['company'][0]
        item['company'] = remove_tags(item['company'])
        item['company'] = item['company'].lstrip('\n ')

        item['job_title'] = item['job_title'][0]
        item['job_title'] = item['job_title'].lower()
        item['location'] = item['location'][0]
        item['date'] = item['date'][0]

        if '30+' in item['date']:
            raise DropItem("Too old %s" % item)

        item['link_url'] = item['link_url'][0]
        item['link_url'] = 'www.indeed.com' + item['link_url']

        # if(job_title_exclusion(self, item)):
        #     raise DropItem("Title exclusion" % item)
        if 'manufacturing' in item['job_title']:
            raise DropItem("Title fail" % item)

        return item

        # def job_title_exclusion(self, item):
        #     return True
