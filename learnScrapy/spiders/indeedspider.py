# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from learnScrapy.items import LearnScrapyItem
from scrapy.http import Request


class IndeedSpider(scrapy.Spider):
    name = "indeed_spider"
    allowed_domains = ["www.indeed.com"]
    start_urls = [
        'http://www.indeed.com/jobs?q=mechanical+title%3Aengineer&sr=directhire',
    ]
    base_url = "http://www.indeed.com/jobs?q=mechanical+title%3Aengineer&sr=directhire&start="

    for i in range(10, 10, 10):
        start_urls.append(base_url + str(i))

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
                item['location'] = jj.xpath('div/span[@class="location"]/text()').extract()
                item['date'] = jj.xpath('div/div/span[@class="date"]/text()').extract()
                item['link_url'] = jj.xpath('a/@href').extract()
                items.append(item)

        """ Gather normal job listings """
        for ii in rows:
            item = LearnScrapyItem()
            item['job_title'] = ii.xpath('h2/a/@title').extract()
            item['company'] = ii.xpath('span/span[@itemprop="name"]/text()').extract()
            item['location'] = ii.xpath('span/span/span[@itemprop="addressLocality"]/text()').extract()
            item['date'] = ii.xpath('table/tr/td/div/div/span[@class="date"]/text()').extract()
            item['link_url'] = ii.xpath('h2/a/@href').extract()

            url = url_prefix + item['link_url'][0]
            item = format_item(self, item)

            if not location_exclusion(self, item):
                request = Request(url, callback=self.parse_job_link)
                request.meta['item'] = item
                yield request
                items.append(item)

        return

    def parse_job_link(self, response):
        sel = Selector(response)
        item = response.request.meta['item']

        return item


def format_item(self, item):
    item['location'] = item['location'][0]
    return item


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
