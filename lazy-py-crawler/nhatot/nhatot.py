
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
import json

class LazyCrawler(LazyBaseCrawler):

    name = "nhatot"
    
    allowed_domains = ["nhatot.com.vn"]

    custom_settings = {
        'DOWNLOAD_DELAY': 4,'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 2, "COOKIES_ENABLED": True,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Ct-Fingerprint": "c5c72d8b-a5bd-4e3a-8a5c-285dde28fcba",
        "Ct-Platform": "web",
        "Origin": "https://www.nhatot.com",
        "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": get_user_agent('random')
    }

    def start_requests(self):
        url = 'https://gateway.chotot.com/v1/public/ad-listing'
        
        payload = {
            "limit": "100",
            "protection_entitlement": "true",
            "cg": "1000",
            "st": "s,k",
            "key_param_included": "true"
        }
        
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, method='GET',
                             body=json.dumps(payload),  )

    def parse(self, response):
        data = response.json()
        ads = data['ads']
        for ad in ads:
            list_id = ad.get('list_id')
            # Second API use to crawl Listing Information:
            url = 'https://gateway.chotot.com/v1/public/ad-listing/{}'.format(list_id)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_list_information, dont_filter=True)
    
    def parse_list_information(self, response):
        json_response = response.json()
        yield json_response['ad']
        
        
            
            # You can now use list_id as needed, perhaps yielding it or passing to another callback
          
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished

