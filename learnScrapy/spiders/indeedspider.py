# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from learnScrapy.items import LearnscrapyItem


class IndeedSpider(scrapy.Spider):
    name = "indeedspider"
    allowed_domains = ["www.indeed.com"]
    start_urls = [
        # 'http://www.indeed.com/jobs?q=mechanical+engineer&l=united+states&sort=date',
        'http://www.indeed.com/jobs?q=title%3A%28energy+engineer%29&l=united+states',
    ]
    # base_url = "http://www.indeed.com/jobs?q=mechanical+engineer&l=united+states&sort=date&start="
    # for i in range(10, 110, 10):
    #     start_urls.append(base_url + str(i))

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//div[@class="  row  result"]')
        sponsored = sel.xpath('//div[@data-tn-section="sponsoredJobs"]')
        lastrow = sel.xpath('//div[@class="lastRow  row  result"]')

        """ Gather the Job listings under 'sponsored """
        items = []
        for spons in sponsored:
            subrows = spons.xpath('div')
            for sub in subrows:
                item = LearnscrapyItem()
                item['jobtitle'] = sub.xpath('a/@title').extract()[0]
                item['company'] = sub.xpath('div/span[@class="company"]'
                                            '/text()').extract()[0].lstrip('\n\t ')
                item['location'] = sub.xpath('div/span[@class="location"]'
                                             '/text()').extract()[0]
                item['date'] = sub.xpath('div/div/span[@class="date"]'
                                         '/text()').extract()[0]
                items.append(item)

        """ Gather normal job listings, minus the last 'special' one """
        for row in rows:
            item = LearnscrapyItem()
            item['jobtitle'] = row.xpath('h2/a/@title').extract()[0]
            item['company'] = row.xpath('span/span[@itemprop="name"]'
                                        '/text()').extract()[0].lstrip('\n\t ')
            item['location'] = row.xpath('span/span/span[@itemprop="addressLocality"]'
                                         '/text()').extract()[0].strip('\n\t ')
            item['date'] = row.xpath('table/tr/td/div/div/span[@class="date"]'
                                     '/text()').extract()[0]
            items.append(item)

        """ Get the last normal job listing """
        item = LearnscrapyItem()
        item['jobtitle'] = lastrow.xpath('h2/a/@title').extract()[0]
        item['company'] = lastrow.xpath('span/span[@itemprop="name"]'
                                        '/text()').extract()[0].lstrip('\n\t ')
        item['location'] = lastrow.xpath('span/span/span[@itemprop="addressLocality"]'
                                         '/text()').extract()[0].strip('\n\t ')
        item['date'] = lastrow.xpath('table/tr/td/div/div/span[@class="date"]'
                                     '/text()').extract()[0]
        items.append(item)

        return items
