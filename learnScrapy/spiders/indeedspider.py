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
        items = []

        for row in rows:
            item = LearnscrapyItem()
            item['jobTitle'] = row.xpath('h2[@class="jobtitle"]/a/@title').extract()
            item['company'] = row.xpath('span/span[@itemprop="name"]/text()').extract()[0].strip(' \n')
           # item['company2'] = row.xpath('a[@title]').extract()
            items.append(item)

        return items
