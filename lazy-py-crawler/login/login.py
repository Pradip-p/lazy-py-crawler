import scrapy
import os
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent

class LazyCrawler(LazyBaseCrawler):
    name = 'login'

    custom_settings = {
        'ITEM_PIPELINES' : {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': None
        }
    }
    
    start_urls = ['http://quotes.toscrape.com/login']
    
    def parse(self, response):
        # Extract CSRF token and other login form data
        # csrf_token = response.css('input[name="csrf_token"]::attr(value)').get()
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        # Extract other login form data as needed
        
        # Send a POST request with login data
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'username': 'admin',
                'password': 'admin',
                'csrf_token': csrf_token,
                # Add other login form fields and their values as needed
            },
            callback=self.after_login, dont_filter = True
        )
    
    def after_login(self, response):
        # Check if login was successful
        print(response.xpath('.//div[@class = "col-md-4"]/p/a/text()'))

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
