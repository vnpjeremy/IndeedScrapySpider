# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from learnScrapy.items import LearnScrapyItem
from scrapy.http import Request


class IndeedSpider(scrapy.Spider):
    name = "indeed_spider"
    allowed_domains = ["www.indeed.com"]
    start_urls = ["http://www.indeed.com/jobs?q=%28mechanical+or+aerospace%29+title%3Aengineer&l="
                  "united+states&sr=directhire&start=0",
                  ]
    base_url = "http://www.indeed.com/jobs?q=%28mechanical+or+aerospace%29+title%3Aengineer&l=" \
               "united+states&sr=directhire&start="

    for i in range(10, 30, 10):
        start_urls.append(base_url + str(i))
    pages = len(start_urls)

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//div[@class="  row  result" or @class="lastRow  row  result"]')
        sponsored = sel.xpath('//div[@data-tn-section="sponsoredJobs"]')
        url_prefix = "http://www.indeed.com"
        items = []

        """ Sponsored job listings have a different footprint """
        for ii in sponsored:
            sub_rows = ii.xpath('div')
            for jj in sub_rows:
                item = LearnScrapyItem()
                item['job_title'] = jj.xpath('a/@title').extract()
                item['company'] = jj.xpath('div/span[@class="company"]/text()').extract()
                if item['company'][0].isspace():
                    item['company'] = jj.xpath('div/span/a/text()').extract()

                item['location'] = jj.xpath('div/span[@class="location"]/text()').extract()
                item['date'] = jj.xpath('div/div/span[@class="date"]/text()').extract()
                item['link_url'] = jj.xpath('a/@href').extract()

                item = format_item(self, item)
                if not exclusion(self, item):
                    request = Request(item['link_url'], callback=self.parse_job_link)
                    request.meta['item'] = item
                    yield request
                    items.append(item)

        """ Gather normal job listings """
        for ii in rows:
            item = LearnScrapyItem()
            item['job_title'] = ii.xpath('h2/a/@title').extract()
            item['company'] = ii.xpath('span/span[@itemprop="name"]/text()').extract()
            if item['company'][0].isspace():
                item['company'] = ii.xpath('span/span/a/text()').extract()

            item['location'] = ii.xpath('span/span/span[@itemprop="addressLocality"]/text()').extract()
            item['date'] = ii.xpath('table/tr/td/div/div/span[@class="date"]/text()').extract()
            item['link_url'] = ii.xpath('h2/a/@href').extract()

            item = format_item(self, item)
            if not exclusion(self, item):
                request = Request(item['link_url'], callback=self.parse_job_link)
                request.meta['item'] = item
                yield request
                items.append(item)

        return

    def parse_job_link(self, response):
        sel = Selector(response)
        item = response.request.meta['item']
        item['link_response'] = response

        return item


def format_item(self, item):
    item['company'] = item['company'][0].lstrip('\n ')
    item['job_title'] = item['job_title'][0].lower()
    item['location'] = item['location'][0].lower()
    item['date'] = item['date'][0]
    item['link_url'] = 'http://www.indeed.com' + item['link_url'][0]
    return item


def exclusion(self, item):
    if date_exclusion(self, item):
        return True
    if not location_inclusion(self, item):
        return True
    if location_exclusion(self, item):
        return True
    if job_title_exclusion(self, item):
        return True
    return False


def date_exclusion(self, item):
    if '30+' in item['date']:
        return True
    return False


def location_exclusion(self, item):
    if 'news' in item['location']:
        return True
    return False


def location_inclusion(self, item):
    if ('ca' in item['location'] or
                'wa' in item['location'] or
                'co' in item['location'] or
                'tx' in item['location'] or
        #        'mn' in item['location'] or
        # 'FL' in item['location'] or
                'ga' in item['location'] or
                'ma' in item['location'] or
                'ct' in item['location'] or
                'ny' in item['location'] or
        # 'WI' in item['location'] or
                'md' in item['location'] or
                'va' in item['location'] or
                'nj' in item['location'] or
                'dc' in item['location'] or
                'il' in item['location']):
        return True
    return False


def job_title_exclusion(self, item):
    if ('manufacturing' in item['job_title'] or
                'hvac' in item['job_title'] or
                'facility' in item['job_title'] or
                'facilities' in item['job_title'] or
                'hvac' in item['job_title'] or
                'field' in item['job_title'] or
                'intern' in item['job_title'] or
                'safety' in item['job_title'] or
                'test' in item['job_title'] or
                'cost' in item['job_title'] or
                'sales' in item['job_title'] or
                'tooling' in item['job_title'] or
                'cnc' in item['job_title'] or
                'lighting' in item['job_title'] or
                'plant' in item['job_title'] or
                'stress' in item['job_title'] or
                'design' in item['job_title'] or
                'reliability' in item['job_title']):
        return True
    return False
