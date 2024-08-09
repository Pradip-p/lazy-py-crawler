import scrapy
#!/usr/bin/env python
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
import gc
import time
from scrapy.spidermiddlewares.httperror import HttpError
from lazy_crawler.lib.image import process_image
import pandas as pd


class LazyCrawler(LazyBaseCrawler):
    name = 'proxy_test'
    start_urls = ['https://example.com', 'https://example.org', 'https://example.net']

    def parse(self, response):
        self.log(f'Parsed {response.url}')


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
