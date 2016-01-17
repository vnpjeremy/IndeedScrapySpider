# -*- coding: utf-8 -*-
import scrapy
#from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from learnScrapy.items import LearnscrapyItem
#from scrapy.shell import inspect_response

class IndeedSpider(scrapy.Spider):
    name = "indeedspider"
    allowed_domains = ["www.indeed.com"]
    start_urls = [
        'http://www.indeed.com/jobs?q=mechanical+engineer&l=united+states',
    ]

    def parse(self, response):
        sel = Selector(response)
#                       can also apparently do response.xpath() directly
        rows = sel.xpath('//div[@class="  row  result"]')
        sponsored = sel.xpath('//div[@data-tn-section="sponsoredJobs"]')
        lastRow = sel.xpath('//div[@class="lastRow  row  result"]')
        items = []

        """ Gather the Job listings under 'sponsored """
        for spons in sponsored:
            subRows = spons.xpath('div')
            for sub in subRows:
                item = LearnscrapyItem()
                item['jobTitle'] = sub.xpath('a/@title').extract()[0]
                item['company'] = sub.xpath('div/span[@class="company"]/text()')\
                    .extract()[0].strip('\n\t ')  # seems [0] is necessary. ?
               # item['location'] = sub.xpath('div/span[@class="location"]/text()').extract()[0]
                items.append(item)

        """ Gather normal job listings, minus the last 'special' one """
        for row in rows:
            item = LearnscrapyItem()
            item['jobTitle'] = row.xpath('h2/a/@title').extract()[0]
          # try strip('\n\t ') instead of two strip calls. Maybe work better?
            item['company'] = row.xpath('span/span[@itemprop="name"]/text()') \
                .extract()[0].strip('\n\t ')
            items.append(item)

        """ Get the last normal job listing """
        item = LearnscrapyItem()
        item['jobTitle'] = lastRow.xpath('h2/a/@title').extract()[0]
        item['company'] = lastRow.xpath('span/span[@itemprop="name"]/text()').extract()[0].strip('\n\t').lstrip()
        items.append(item)

        return items
