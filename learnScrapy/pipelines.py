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
import re


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
        if not text_inclusion(self, body):
            raise DropItem("Lacks mandatory text %s" % item)
        # 
        if text_exclusion(self, body):
            raise DropItem("Prohibited text %s" % item)

        return item


def format_response(self, item):
    body = item['link_response'].body
    body = remove_javascript(body)
    h = html2text.HTML2Text()
    h.ignore_links = True
    try:
        body = h.handle(body.decode('utf8'))
        body = body.lower()
    except Exception as oops:
        logging.warning("Html2text screwed up!!")
        logging.warning(oops.args)
    return body


def text_exclusion(self, body):
    anti_text = []
    anti_text.append(r"secret")
    anti_text.append(r"cnc")
    anti_text.append(r"nuclear")
    for ii in anti_text:
        if re.search(r"\b" + ii + r"\b", body):
            return True
    return False


def text_inclusion(self, body):
    text = []
    text.append(r"master")
    text.append(r"master's")
    text.append(r"phd")
    for ii in text:
        if re.search(r"\b" + ii + r"\b", body):
            return True
    return False


""" remove_javascript:
    This should be done with lxml via elem.getparent().remove(elem), but
    something fishy was going on with the getparent() function. Punt for now. """


def remove_javascript(link_response):
    soup = BeautifulSoup.BeautifulSoup(link_response)
    to_extract = soup.findAll('script')
    for ii in to_extract:
        ii.extract()
    return soup.prettify()

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


# def date_exclusion(self, item):
#     if '30+' in item['date']:
#         return True
#     return False
# 
# 
# def location_inclusion(self, item):
#     locations = []
#     locations.append(r"ca")
#     locations.append(r"wa")
#     locations.append(r"co")
#     locations.append(r"tx")
#     locations.append(r"mn")
#     locations.append(r"fl")
#     locations.append(r"ga")
#     locations.append(r"ct")
#     locations.append(r"ny")
#     locations.append(r"wi")
#     locations.append(r"md")
#     locations.append(r"dc")
#     locations.append(r"va")
#     locations.append(r"nj")
#     locations.append(r"il")
#
#     for ii in locations:
#         if re.search(r"\b" + ii + r"\b", item['location']):
#             return True
#     return False
