# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from learnScrapy.items import LearnScrapyItem


class IndeedSpider(scrapy.Spider):
    name = "indeed_spider"
    allowed_domains = ["www.indeed.com"]
    start_urls = [
        'http://www.indeed.com/jobs?q=mechanical+engineer&l=',
    ]
    base_url = "http://www.indeed.com/jobs?q=mechanical+engineer&start="

    for i in range(10, 30, 10):
        start_urls.append(base_url + str(i))

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//div[@class="  row  result" or @class="lastRow  row  result"]')
        sponsored = sel.xpath('//div[@data-tn-section="sponsoredJobs"]')

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
            items.append(item)

        return items
