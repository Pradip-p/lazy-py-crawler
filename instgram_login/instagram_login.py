
from email.mime import image
from ipaddress import ip_address
import os
from traceback import print_tb
from numpy import product
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
from lazy_crawler.lib.html import to_browser
from lazy_crawler.lib.forms import get_form_fields
from scrapy.http import FormRequest


class LazyCrawler(scrapy.Spider):
    
    name = 'login'
    
    allowed_domains = ['quotes.toscrape.com']
    
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self,response):
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        yield FormRequest.from_response(response,
                                        formdata={'csrf_token': csrf_token,
                                                    'username': 'user',
                                                    'password': 'pass',
                                                    'user_agent': get_user_agent()},
                                        callback=self.parse_after_login,
                                        dont_filter=True)
            
    def parse_after_login(self,response):
        to_browser(response)
        pass

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
