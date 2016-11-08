# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs

class CsdnCrawlerPipeline(object):
    def __init__(self):
        self.file = codecs.open('csdn_data_utf8.txt', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        a=item['name'].strip()
        self.file.write(a+'\n')
        return item
    def spider_closed(self, spider):
        self.file.close()
