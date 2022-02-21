import os
import sys
from tabnanny import check
from turtle import title
from urllib import request
import scrapy
from scrapy import settings
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import time
from lazy_crawler.lib.html import to_browser

class LazyCrawler(LazyBaseCrawler):
    
    name = "quotes"
    page_number = 1
    
    def start_requests(self):
        settings = get_project_settings()
        print("Your USER_AGENT is:\n%s" % (settings.get('ITEM_PIPELINES')))
        # url = 'https://www.threadsquad.com/'
        url = 'https://www.micolet.com/tops/noname/2975125'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        to_browser(response)
        # yield scrapy.Request(response.url, callback=self.parse_detail, dont_filter=True)
        
            
        for item in response.css('div.itemtiles a.item'):
            url = "https://www.threadsquad.com" + item.xpath('//*[@id="mainBar"]/div/a/@href').get()
            
            title= item.xpath('//*[@id="mainBar"]/div/a/figure/figcaption/text()').get()
            price= item.xpath('//*[@id="mainBar"]/div/a/figure/figcaption/var/text()').get()
            check =item.xpath('//*[@id="mainBar"]/div/a/figure/img/@src').get()
            if check is not None:
                image= "https://www.threadsquad.com/"+item.xpath('//*[@id="mainBar"]/div/a/figure/img/@src').get()
            else:
                image = ''
            # print(url)
            yield scrapy.Request(url, self.parse_detail,meta= {"title":title,'price':price,"image":image} ,dont_filter=True)
            
        self.page_number += 1
        next_page = "https://www.threadsquad.com/page/"+str(self.page_number)
        if self.page_number <= 10:
            time.sleep(5)
            yield response.follow(next_page, self.parse)
            
    def parse_detail(self, response):
        yield {
            "Title": response.meta['title'],
            "Price": response.meta['price'],
            "Image": response.meta['image'],
            "Description":response.css("div.description::text").get(),
            "Detail":response.css("div.productDetails::text").get(),   
            "Url": response.url,         
        }
        
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

process = CrawlerProcess()  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
