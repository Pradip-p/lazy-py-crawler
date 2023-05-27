#!/usr/bin/env python
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.cleaner import strip_html
import base64
from lazy_crawler.lib.user_agent import get_user_agent
import gc
import json
import time

class LazyCrawler(LazyBaseCrawler):

    name = "livaroom"

    allowed_domains = ['livaroom.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 4,'LOG_LEVEL': 'DEBUG',
        
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,

        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,'RETRY_TIMES': 2,

        "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,

        'ITEM_PIPELINES' :  {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }
    ###all category avaiable in livroom
    categories =  [
        {
        'living':['https://livaroom.com/collections/living-room'],
        'bedroom':['https://livaroom.com/collections/bedroom'],
        'kitchen & dining':['https://livaroom.com/collections/kitchen-dining'],
        'home & entertainment':['https://livaroom.com/collections/home-entertainment'],
        'baby & kids furniture':['https://livaroom.com/collections/baby-kids-furniture'],
        'outdoor':['https://livaroom.com/collections/outdoor'],
        'home-decor':['https://livaroom.com/collections/home-decor'],
        'bathroom':['https://livaroom.com/collections/bathroom'],
        'office':['https://livaroom.com/collections/office']
        }
    ]
    proxy = 'p.webshare.io:80'
    # user_pass = base64.encodebytes("hpiukvrn-rotate:yahyayahya".encode()).decode()
    user_pass = base64.encodebytes("gkoffhkj-rotate:9qsx6zrpagq6".encode()).decode()

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        ###add
        # 'Proxy-Authorization': 'Basic ' + user_pass,
    }

    proxy = 'p.webshare.io:80'
    # user_pass = base64.encodebytes("hpiukvrn-rotate:yahyayahya".encode()).decode()
    user_pass = base64.encodebytes("gkoffhkj-rotate:9qsx6zrpagq6".encode()).decode()
    
    def start_requests(self): #project start from here.
        # for category in self.categories:
        #     category = category.items()
        #     for key, value in category:
        #         category_name = key
        #         urls = value
        #         for url in urls:
        #             time.sleep(5) #sleep for 10 sec
        #             yield scrapy.Request(url, self.parse_json, dont_filter=True,
        #                                  headers=self.HEADERS, meta={'category_name':category_name})
        url = 'https://livaroom.com/collections/zuo'
        yield scrapy.Request(url, self.parse_json, dont_filter=True,headers=self.HEADERS)

    def parse_json(self, response):
        data_json_product = response.xpath('//li[@class="product"]/div[@class="product-item"]/@data-json-product').extract()
        for json_data in data_json_product:
            json_data = json.loads(json_data)
            yield json_data

        next_page = response.xpath('//ul[@class="pagination__list list-unstyled"]/li[@class="pagination-arrow"][last()]/a/@href').extract_first()
        ###logical error, fixed it.
        if next_page:
            url = 'https://livaroom.com{}'.format(next_page)
            yield scrapy.Request(url, self.parse_json, dont_filter=True,headers=self.HEADERS)
            
        gc.collect()


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished