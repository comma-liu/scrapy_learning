# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from pathlib import PurePosixPath
from urllib.parse import urlparse

class Testscrapy1Pipeline:
    def open_spider(self, item):
        self.f = open('./testspider.md', 'w+', encoding='utf-8')
        self.num = 1
    def process_item(self, item, spider):
        self.f.write(f'这是第{self.num}部电影:\n');self.num = self.num + 1
        self.f.write(str(item))
        self.f.write('\n')
        return item
    def close_spider(self, item):
        self.f.close()

class MyImagesPipeline(ImagesPipeline):
    pass    
