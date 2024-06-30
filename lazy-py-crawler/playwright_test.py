import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import base64

from lazy_crawler.lib.user_agent import get_user_agent


class LazyCrawler(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = "https://www.bloomberg.com/news/newsletters/2023-05-27/the-us-budget-battle-china-s-security-focus-weekend-reads"
        yield scrapy.Request(url, meta={'playwright': True})

    def parse(self, response):
        title = response.xpath('//h1[@class="headline__699ae8fb"]/text()').extract_first()
        yield {
            'title': title
        }


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start()
