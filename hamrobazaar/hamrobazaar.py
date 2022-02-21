
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

class LazyCrawler(scrapy.Spider):
    
    name = "hamrobazaar"
    
    allowed_domains = ["https://hamrobazaar.com"]
    
    def start_requests(self):
        
        url = "https://hamrobazaar.com/register.php"
        
        yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        to_browser(response)
        #get get_form_fields    
        form_fields = get_form_fields(selector='//form', response=response, selector_type='xpath', excluded_fields=[], allowed_fields=[])
        print(form_fields)


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
