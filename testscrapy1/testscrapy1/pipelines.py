import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from pathvalidate import sanitize_filename as sf

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
    number = 0
    def get_media_requests(self, item, info):
        list = [Request(u) for u in item['image_urls']]
        for i in list:
            i.item = item
        return list
        
    def file_path(self, request, response = None, info = None, *, item = None):
        #image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()  # nosec
        self.number += 1
        return f"{sf(request.item['name'])}/{sf(request.item['name'])}_{self.number}.jpg"    
