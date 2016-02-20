# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from learnScrapy.items import LearnScrapyItem
from scrapy.http import Request


# from scrapy.utils.markup import remove_tags


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
    item['company'] = item['company'][0]
    # item['company'] = remove_tags(item['company'])
    item['company'] = item['company'].lstrip('\n ')

    item['job_title'] = item['job_title'][0]
    item['job_title'] = item['job_title'].lower()
    item['location'] = item['location'][0]
    item['date'] = item['date'][0]

    item['link_url'] = item['link_url'][0]
    item['link_url'] = 'http://www.indeed.com' + item['link_url']
    return item


def exclusion(self, item):
    if date_exclusion(self, item):
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
    if ('CA' in item['location'] or
                'WA' in item['location'] or
                'CO' in item['location'] or
                'TX' in item['location'] or
                'MN' in item['location'] or
        # 'FL' in item['location'] or
                'GA' in item['location'] or
                'MA' in item['location'] or
                'CT' in item['location'] or
                'NY' in item['location'] or
        # 'WI' in item['location'] or
                'MD' in item['location'] or
                'DE' in item['location'] or
                'VA' in item['location'] or
                'NJ' in item['location']):
        # 'IL' in item['location']):
        return False
    return True


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
