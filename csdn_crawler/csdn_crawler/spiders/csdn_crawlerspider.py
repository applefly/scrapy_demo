#!/usr/bin/python
# -*- coding:utf-8 -*-
#coding=utf-8
import re
import json
from scrapy.spider import BaseSpider as Spider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from csdn_crawler.items import CsdnCrawlerItem
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class CsdnSpider(Spider):
    """爬取标签"""
    name = "csdn_crawler"
    allowed_domains = ["blog.csdn.net"]
    start_urls = (
      #  'http://blog.csdn.net/applebite',
        'http://blog.csdn.net/applebite/article/details/46872819',
    )
    rules = [
        Rule(SgmlLinkExtractor(allow=('/applebite/article/details'),
                              restrict_xpaths=('//li[@class="next_article"]')),
             callback='parse_item',
             follow=True)
    ]

    def parse(self, response):
        sel = Selector(response)
        #sites=sel.xpath('//div[@class="list_item article_item"]/div[@class="article_title"]')
        sites=sel.xpath('//div[@class="article_title"]')
        items=[]
        for site in sites:
            item = CsdnCrawlerItem()
            item['name']=site.xpath('h1/span/a/text()').extract()[0]
            items.append(item)
            log.msg("add item...",level=2)
        log.msg("Append done.",level=1)

        prev=sel.xpath('//li[@class="prev_article"]/a/@href').extract()
        if len(prev) > 0 and prev[0]:
            items.append(Request('http://blog.csdn.net'+prev[0], callback=self.parse))

        next=sel.xpath('//li[@class="next_article"]/a/@href').extract()
        if len(next) > 0 and next[0]:
            items.append(Request('http://blog.csdn.net'+next[0], callback=self.parse))
        return items

