import scrapy
from testscrapy1.items import *
import copy

class Testcrapy1Spider(scrapy.Spider):
    name = "testcrapy1"
    #allowed_domains = ["ssr1.scrape.center"]
    start_urls = ["https://ssr1.scrape.center/"]
    item = Testscrapy1Item()
    number = 1
    
    def parse(self, response):
        for i in response.css('.el-card__body') :
           self.item['name'] = i.css('.m-b-sm ::text').extract_first()
           self.item['caro'] = '/'.join(i.css('.categories span ::text').extract())
           self.item['info'] = '/'.join(i.css('.m-v-sm span ::text').extract()) 
           yield scrapy.Request(f'https://ssr1.scrape.center/detail/{self.number}', self.parse_detail, meta = {'item': copy.deepcopy(self.item)})
           self.number += 1
        nextpage = response.xpath('//a[@class="next"]/@href').extract_first()
        if nextpage:
           yield scrapy.Request(f'https://ssr1.scrape.center{nextpage}', self.parse)
    def parse_detail(self, response):
        item = response.meta['item']
        item['story'] = ''.join(response.css('.drama p ::text').extract()).strip()
        item['actor'] = ''
        for i in response.xpath('//div[@class="actor el-col el-col-4"]'):
           item['actor'] += ''.join(i.css('p ::text').extract())+'||'
        image_list = response.xpath('//div[@class="el-image"]/img/@src').extract()
        if image_list.__len__() < 10:
           item['image_urls'] = image_list
        else:
           item['image_urls'] = image_list[:11]
        yield item
        