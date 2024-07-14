import scrapy
from testscrapy1.items import *

class Testcrapy1Spider(scrapy.Spider):
    name = "testcrapy1"
    #allowed_domains = ["ssr1.scrape.center"]
    start_urls = ["https://ssr1.scrape.center/"]
    
    def parse(self, response):
        self.item = Testscrapy1Item()
        for i in response.css('.el-card__body'):
            self.item['name'] = ''.join(i.css('.m-b-sm ::text').extract())
            self.item['caro'] = '/'.join(i.css('.categories span ::text').extract())
            self.item['info'] = '/'.join(i.css('.m-v-sm span ::text').extract())    
        for i in response.xpath('//div[@class="el-card__body"]/div/div[1]/a/@href'):
            yield scrapy.Request(response.urljoin(i.extract()), self.parse_detail)
        for href in response.css(".number a"):
            index_page = ''.join(href.css('::text').extract())
            yield scrapy.Request(response.urljoin('page/'+index_page), self.parse)
            
    def parse_detail(self, response):
        self.item['story'] = ''.join(response.css('.drama p ::text').extract()).strip()
        self.item['actor'] = ''
        for i in response.xpath('//div[@class="actor el-col el-col-4"]'):
            self.item['actor'] += ''.join(i.css('p ::text').extract())+'||'
        image_list = response.xpath('//div[@class="el-image"]/img/@src').extract()
        if image_list.__len__() < 10:
            self.item['image_urls'] = image_list
        else:
            self.item['image_urls'] = image_list[:10]
        yield self.item
        