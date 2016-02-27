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
import logging


class LearnScrapyPipeline(object):
    def process_item(self, item, spider):
        # if date_exclusion(self, item):
        #     raise DropItem("Too old %s" % item)
        # if not location_inclusion(self, item):
        #     raise DropItem("Location fail %s" % item)
        # if job_title_exclusion(self, item):
        #     raise DropItem("Job title fail %s" % item)

        body = format_response(self, item)
        # 
        # d_text = "ASSERT"
        # if not text_inclusion(self, link_response. d_text):
        #     raise DropItem("Lacks mandatory text %s" % item)
        # 
        # if text_exclusion(self, link_response):
        #     raise DropItem("Prohibited text %s" % item)

        return item


def format_response(self, item):
    body = item['link_response'].body
    body = remove_javascript(body)
    h = html2text.HTML2Text()
    h.ignore_links = True
    try:
        body = h.handle(body.decode('utf8'))
        body = body.lower()
    except Exception as thing:
        logging.warning("Html2text screwed up!!")
        logging.warning(thing.args)
    return body


# def text_exclusion(self, link_response):
#     if ("secret" in link_response or
#                 "cnc" in link_response or
#                 "nuclear" in link_response):
#         return True
#     return False
# 
# 
# def text_inclusion(self, link_response, d_text):
#     if ("master's" in link_response or
#                 "master" in link_response or
#                 "phd" in link_response):
#         return True
#     return False
# 
#
""" This should be done with lxml via elem.getparent().remove(elem), but
    something fishy was going on with the getparent() function. Punt for now. """


def remove_javascript(link_response):
    soup = BeautifulSoup.BeautifulSoup(link_response)
    to_extract = soup.findAll('script')
    for ii in to_extract:
        ii.extract()
    return soup.prettify()

# 
# def job_title_exclusion(self, item):
#     if ('manufacturing' in item['job_title'] or
#                 'hvac' in item['job_title'] or
#                 'facility' in item['job_title'] or
#                 'facilities' in item['job_title'] or
#                 'hvac' in item['job_title'] or
#                 'field service' in item['job_title'] or
#                 'intern' in item['job_title'] or
#                 'safety' in item['job_title'] or
#                 'reliability' in item['job_title']):
#         return True
#     return False
# 
# 
# def date_exclusion(self, item):
#     if '30+' in item['date']:
#         return True
#     return False
# 
# 
# def location_inclusion(self, item):
#     if ('CA' in item['location'] or
#                 'WA' in item['location'] or
#                 'CO' in item['location'] or
#                 'TX' in item['location'] or
#                 'MN' in item['location'] or
#                 'FL' in item['location'] or
#                 'GA' in item['location'] or
#                 'MA' in item['location'] or
#                 'CT' in item['location'] or
#                 'NY' in item['location'] or
#                 'WI' in item['location'] or
#                 'MD' in item['location'] or
#                 'DE' in item['location'] or
#                 'VA' in item['location'] or
#                 'NJ' in item['location'] or
#                 'IL' in item['location']):
#         return True
#     return False
