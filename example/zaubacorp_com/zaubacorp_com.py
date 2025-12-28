import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent
from scrapy.shell import inspect_response
from scrapy import FormRequest
import datetime
import re
# from lazy_crawler.crawler.pipelines import JsonWriterPipeline
class LazyCrawler(scrapy.Spider):

    name = "zaubacorp"

    allowed_domains = ['zaubacorp.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_IP': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'RETRY_TIMES': 2,
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'DOWNLOAD_TIMEOUT': 180,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': None
        }
    }

    def start_requests(self): #project start from here.
        url = 'https://www.zaubacorp.com/company-list'
        yield scrapy.Request(url, self.parse, dont_filter=True, )


    def parse(self, response):
        urls = response.xpath('//td/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, self.parse_details, dont_filter=True, )

    def parse_details(self, response):

        inspect_response(response, self)
        yield {}





settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
