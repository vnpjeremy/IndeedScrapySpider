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

        item['link_url'] = item['link_url'][0]
        item['link_url'] = 'www.indeed.com' + item['link_url']

        if date_exclusion(self, item):
            raise DropItem("Too old %s" % item)

        if location_exclusion(self, item):
            raise DropItem("Location fail" % item)

        if job_title_exclusion(self, item):
            raise DropItem("Job title fail" % item)

        return item


def job_title_exclusion(self, item):
    if ('manufacturing' in item['job_title'] or
                'hvac' in item['job_title'] or
                'facility' in item['job_title'] or
                'facilities' in item['job_title'] or
                'hvac' in item['job_title'] or
                'field service' in item['job_title'] or
                'intern' in item['job_title'] or
                'safety' in item['job_title'] or
                'reliability' in item['job_title']):
        return True
    return False


def date_exclusion(self, item):
    if '30+' in item['date']:
        return True
    return False


def location_exclusion(self, item):
    if ('CA' in item['location'] or
                'WA' in item['location'] or
                'CO' in item['location'] or
                'TX' in item['location'] or
                'MN' in item['location'] or
                'FL' in item['location'] or
                'GA' in item['location'] or
                'MA' in item['location'] or
                'CT' in item['location'] or
                'NY' in item['location'] or
                'WI' in item['location'] or
                'MD' in item['location'] or
                'DE' in item['location'] or
                'VA' in item['location'] or
                'NJ' in item['location'] or
                'IL' in item['location']):
        return False
    return True
