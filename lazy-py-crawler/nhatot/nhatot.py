
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
import json
from scrapy.spidermiddlewares.httperror import HttpError
import time
import undetected_chromedriver as uc
# from selenium import webdriver

class LazyCrawler(LazyBaseCrawler):

    def __init__(self):
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument( '--headless' )
        self.driver = uc.Chrome(options = options)


        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

        # self.driver = webdriver.Chrome(options=chrome_options)
        
    name = "nhatot"
    
    allowed_domains = ["nhatot.com.vn"]

    custom_settings = {
        'DOWNLOAD_DELAY': 4,'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 2, "COOKIES_ENABLED": True,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': None
        }
    }
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        # "Ct-Fingerprint": "c5c72d8b-a5bd-4e3a-8a5c-285dde28fcba",
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

    def errback_http_ignored(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 430 or 302 or 404:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                print('crawler waiting for 10 second')
                time.sleep(10)  # Wait for 10 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

            if response.status == 503:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                time.sleep(20)  # Wait for 8 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

    def _retry_request(self, request, reason, spider):
        retryreq = request.copy()
        retryreq.meta['retry_times'] = request.meta.get('retry_times', 0) + 1
        retryreq.dont_filter = True
        return retryreq
    
    def start_requests(self):
        url = 'https://gateway.chotot.com/v1/public/ad-listing'
        
        payload = {
            "limit": "10",
            "protection_entitlement": "true",
            "cg": "1000",
            "st": "s,k",
            "key_param_included": "true"
        }
        
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, method='GET',
                             body=json.dumps(payload),errback=self.errback_http_ignored  )

    def parse(self, response):
        data = response.json()
        ads = data['ads']
        for ad in ads:
            list_id = ad.get('list_id')
            # Second API use to crawl Listing Information:
            url = 'https://gateway.chotot.com/v1/public/ad-listing/{}'.format(list_id)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_list_information, 
                    errback=self.errback_http_ignored,dont_filter=True)
    
    def parse_list_information(self, response):
        json_response = response.json()
        list_id = json_response['ad']['list_id']
        url = 'https://www.nhatot.com/{}.htm'.format(list_id)
         
        phone_number = self.scrape_phone_from_url(url)
        
    def scrape_phone_from_url(self, url):
        self.driver.get(url)
        phone_number = ''
        time.sleep(30)
        # Close the browser
        # self.driver.quit()    

        return phone_number
    
            
            # You can now use list_id as needed, perhaps yielding it or passing to another callback
          
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished

