# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from learnScrapy.items import LearnScrapyItem


class IndeedSpider(scrapy.Spider):
    name = "indeed_spider"
    allowed_domains = ["www.indeed.com"]
    start_urls = [
        'http://www.indeed.com/jobs?q=mechanical+engineer&l=wilmington+de&radius=0',
    ]
    base_url = "http://www.indeed.com/jobs?q=mechanical+engineer&l=wilmington+de&radius=0&start="

    # for i in range(10, 50, 10):
    #     start_urls.append(base_url + str(i))

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//div[@class="  row  result" or @class="lastRow  row  result"]')
        sponsored = sel.xpath('//div[@data-tn-section="sponsoredJobs"]')

        items = []
        for ii in sponsored:
            sub_rows = ii.xpath('div')
            for jj in sub_rows:
                item = LearnScrapyItem()
                item['job_title'] = jj.xpath('a/@title').extract()
                item['company'] = jj.xpath('div/span[@class="company"]/text()').extract()
                item['location'] = jj.xpath('div/span[@class="location"]/text()').extract()
                item['date'] = jj.xpath('div/div/span[@class="date"]/text()').extract()
                items.append(item)

        """ Gather normal job listings, minus the last 'special' one """
        for row in rows:
            item = LearnScrapyItem()
            item['job_title'] = row.xpath('h2/a/@title').extract()
            item['company'] = row.xpath('span/span[@itemprop="name"]/text()').extract()
            item['location'] = row.xpath('span/span/span[@itemprop="addressLocality"]/text()').extract()
            item['date'] = row.xpath('table/tr/td/div/div/span[@class="date"]/text()').extract()
            items.append(item)

        return items
