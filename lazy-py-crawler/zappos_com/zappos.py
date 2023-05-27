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

class LazyCrawler(LazyBaseCrawler):
    def errback_http_ignored(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 430:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                time.sleep(240)  # Wait for 4 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

            if response.status == 503:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                time.sleep(480)  # Wait for 8 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

    def _retry_request(self, request, reason, spider):
        retryreq = request.copy()
        retryreq.meta['retry_times'] = request.meta.get('retry_times', 0) + 1
        retryreq.dont_filter = True
        return retryreq
    
    name = "zappos"

    allowed_domains = ['zappos.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',
        
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,

        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,'RETRY_TIMES': 2,

        # "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,

        'ITEM_PIPELINES' :  {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': None
        }
    }


    HEADERS = {
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
    }

    def start_requests(self): #project start from here.
        headers = {
            'User-Agent': get_user_agent('random'),
            **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
            }
        url = 'https://www.zappos.com/men-shirts-tops'
        yield scrapy.Request(url, self.parse_json, dont_filter=True,
                errback=self.errback_http_ignored,
                headers= headers,
                )
    

    def parse_json(self, response):

        urls = response.xpath('//a[@class="dk-z"]/@href').extract()
        for url in urls:
            url = 'https://www.zappos.com/{}'.format(url)
            yield scrapy.Request(url, callback= self.parse_detail, dont_filter=True)
    
    def parse_detail(self, response):
        name = response.xpath('//span[@class="Aq-z"]/text()').extract_first()
        
        images = response.xpath('//img[@class="sja-z"]/@src').extract()
        
        for img_url in images:
            # Extract the filename from the URL
            filename = os.path.basename(img_url)

            # Find the position of the first and second dot in the filename
            first_dot_index = filename.find(".")
            second_dot_index = filename.find(".", first_dot_index + 1)

            # Remove the text between the two dots in the filename
            modified_filename = filename[:first_dot_index] + filename[second_dot_index:]

            # Replace the original filename with the modified filename in the URL
            modified_url = img_url.replace(filename, modified_filename)
            process_image(name,modified_url)
        
        # print('Donwloaded!!!')
        gc.collect()

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished