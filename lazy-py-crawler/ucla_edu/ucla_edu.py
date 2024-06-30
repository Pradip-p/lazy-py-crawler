
import base64
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.html import to_browser
from lazy_crawler.lib.user_agent import get_user_agent
import ipdb

class LazyCrawler(scrapy.Spider):

    name = "westchestermedicalcenter"
    
    allowed_domains = ['westchestermedicalcenter.org']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 2,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 180,
        'REDIRECT_ENABLED' : False,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': None
        }
    }
    

    
    
    def start_requests(self):

        url = 'https://www.westchestermedicalcenter.org/neurosurgery2'
        
        headers = {
            'User-Agent': get_user_agent('random'),
            }
        
        yield scrapy.Request(url, callback=self.parse_details,
                            headers= headers, 
                            dont_filter=True)


    def parse_details(self, response):
        # to_browser(response)
        # Residents
        residents = response.xpath('//div[@id="cpsys_DynamicTab_d64c8276-3907-45fc-a37f-84f033d06d95_3"]')
        name = residents.xpath('//p/span/strong/text()').extract()
        post_graduate_year = '' #coming from name to.
        school_name = residents.xpath('//p/span/span/text()').extract()
        print(school_name)

                
            
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
