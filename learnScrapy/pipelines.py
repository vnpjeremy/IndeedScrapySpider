# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.selector import Selector
from scrapy.utils.markup import remove_tags
import lxml.html
import lxml.etree
import html2text
import BeautifulSoup

54


class LearnScrapyPipeline(object):
    def process_item(self, item, spider):
        if date_exclusion(self, item):
            raise DropItem("Too old %s" % item)

        if location_exclusion(self, item):
            raise DropItem("Location fail %s" % item)

        if job_title_exclusion(self, item):
            raise DropItem("Job title fail %s" % item)

        if text_exclusion(self, item):
            raise DropItem("Prohibited text %s" % item)

        return item


def text_exclusion(self, item):
    link_response = item['link_response'].body
    link_response = remove_javascript(link_response)
    link_response = remove_tags(link_response)
    link_response = link_response.lower()

    if ("master's" in link_response or
                "master" in link_response):
        return True
    return False


def remove_javascript(link_response):
    soup = BeautifulSoup.BeautifulSoup(link_response)
    to_extract = soup.findAll('script')
    for ii in to_extract:
        ii.extract()
    return soup.prettify()


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
