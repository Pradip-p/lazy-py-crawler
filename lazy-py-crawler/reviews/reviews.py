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
from scrapy import FormRequest
import json


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
    
    name = "chewy"

    allowed_domains = ['chewy.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',
        
        'CONCURRENT_REQUESTS' : 32,'CONCURRENT_REQUESTS_PER_IP': 32,

        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,'RETRY_TIMES': 1,

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
        
        url = 'https://www.chewy.com/brands'
        yield scrapy.Request(url, self.brand_url, dont_filter=True,
                errback=self.errback_http_ignored,
                headers= headers,
                )
    
    def brand_url(self, response, **kwargs):
        urls = response.xpath('//a[@class="jsx-3519525548 jsx-193800844 brand-link"]/@href').extract()
        for url in urls:
            url = 'https://www.chewy.com{}'.format(url)
            yield scrapy.Request(url, callback=self.data_category_id, dont_filter=True)
    


    def data_category_id(self, response):
        ids = response.xpath('//div/@data-category').extract()
        for _id in ids:
            url = 'https://www.chewy.com/api/pdp/graphql'
            payload = {
                "operationName": "Reviews",
                "variables": {
                    "sort": "MOST_RELEVANT",
                    "id": _id,
                    "after": "YXJyYXljb25uZWN0aW9uOjk="
                },
                "extensions": {},
                "query": "query Reviews($id: String!, $after: String, $feature: String, $filter: ReviewFilter, $sort: ReviewSort = MOST_RELEVANT, $hasPhoto: Boolean, $reviewText: String) {\n  product(id: $id) {\n    id\n    ...Reviews\n    ...ReviewFeatures\n    __typename\n  }\n}\n\nfragment Reviews on Product {\n  id\n  partNumber\n  name\n  reviews(\n    after: $after\n    feature: $feature\n    filter: $filter\n    first: 10\n    sort: $sort\n    hasPhoto: $hasPhoto\n    reviewText: $reviewText\n  ) {\n    totalCount\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    edges {\n      node {\n        id\n        ...Review\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Review on Review {\n  id\n  contentId\n  helpfulness\n  photos {\n    ...UserGeneratedPhoto\n    __typename\n  }\n  rating\n  submittedAt\n  submittedBy\n  contributorBadge\n  isIncentivized\n  text\n  title\n  __typename\n}\n\nfragment UserGeneratedPhoto on UserGeneratedPhoto {\n  __typename\n  caption\n  fullImage\n  thumbnail\n}\n\nfragment ReviewFeatures on Product {\n  id\n  partNumber\n  reviewFeatures\n  __typename\n}\n"
            }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': get_user_agent('random')
            }
            yield FormRequest(url, dont_filter=True, formdata={'json': json.dumps(payload)}, headers=headers, callback=self.parse_response )


    def parse_response(self, response):
        print(response.text)

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished