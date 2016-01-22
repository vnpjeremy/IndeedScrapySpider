# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.selector import Selector
from learnScrapy.items import LearnscrapyItem
# from scrapy.linkextractors import SgmlLinkExtractor
# from scrapy.shell import inspect_response


class IndeedSpider(CrawlSpider):
    name = "indeedspider"
    allowed_domains = ["www.indeed.com"]
    start_urls = [
        'http://www.indeed.com/jobs?q=mechanical+engineer&l=united+states&sort=date',
    ]

    # rules = (
    #      Rule(SgmlLinkExtractor(allow=('jobs?q=mechanical+engineer&l=united+states&sort=date', )),
    #           callback='parse_item', follow=True),
    # )  # follow=True added...needed?

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
                item['jobTitle'] = sub.xpath('a/@title').extract()[0]
                item['company'] = sub.xpath('div/span[@class="company"]/text()') \
                    .extract()[0].strip('\n\t ')
                item['location'] = sub.xpath('div/span[@class="location"]/text()').extract()[0]
                items.append(item)

        """ Gather normal job listings, minus the last 'special' one """
        for row in rows:
            item = LearnscrapyItem()
            item['jobTitle'] = row.xpath('h2/a/@title').extract()[0]
            item['company'] = row.xpath('span/span[@itemprop="name"]/text()') \
                .extract()[0].strip('\n\t ')
            item['location'] = row.xpath('span/span/span[@itemprop="addressLocality"]/text()') \
                .extract()[0].strip('\n\t ')
            # item['date'] = row.xpath('tbody/tr/td/div[2]/div/span[1]') \
            #     .extract()[0].strip('\n\t ')

            # /html/body/table[2]/tbody/tr/td/table/tbody/tr/td[2]/div[10]/table/tbody/tr/td/div[2]/div/span[1]

            items.append(item)

        """ Get the last normal job listing """
        item = LearnscrapyItem()
        item['jobTitle'] = lastrow.xpath('h2/a/@title').extract()[0]
        item['company'] = lastrow.xpath('span/span[@itemprop="name"]/text()') \
            .extract()[0].strip('\n\t').lstrip()
        item['location'] = lastrow.xpath('span/span/span[@itemprop="addressLocality"]/text()') \
            .extract()[0].strip('\n\t ')
        items.append(item)

        return items
