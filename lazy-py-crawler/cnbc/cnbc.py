
import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
import scrapy
import pytz
from datetime import datetime
import time
from dateutil.parser import parse


class LazyCrawler(LazyBaseCrawler):

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'DEBUG',
        'CHANGE_PROXY_AFTER': 1,
        'USE_PROXY': True,
        'CONCURRENT_REQUESTS': 126,
        'CONCURRENT_REQUESTS_PER_IP': 26,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'JOBDIR': './crawls',
        'RETRY_TIMES': 2,
        "COOKIES_ENABLED": True,
        'DOWNLOAD_TIMEOUT': 500,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }
    next_offset = 0
    page_num = 1
    start_offset = 0
    page_size = 24
    asset_ids = ["15839069","10001147", "19854910"]# 
    base_url = "https://webql-redesign.cnbcfm.com/graphql"
    query_variables = '{{"id":"{}","offset":{},"pageSize":{},"nonFilter":true,"includeNative":false,"include":[]}}'
    query_extensions = '{{"persistedQuery":{{"version":1,"sha256Hash":"{}"}}}}'
    
    def start_requests(self):
        for asset_id in self.asset_ids:
            url = self.build_url(asset_id, self.start_offset)
            yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True, meta={'asset_id': asset_id})

    def parse_url(self, response):
        json_data = json.loads(response.text)
        try:
            assets = json_data['data']['assetList']['assets']
        except KeyError:
            return None
        
        if assets:
            for asset in assets:
                url = asset['url']
                yield scrapy.Request(url, callback=self.parse_article_detail, dont_filter=True, meta={'asset': asset})

        # Extract pagination information

        total_items = json_data['data']['assetList']['pagination']['totalCount']
        if total_items == 'null':
            return None
        else:
            self.next_offset = self.next_offset + self.page_size
            # Send subsequent requests with different offsets
            while self.next_offset < total_items:
                asset_id = response.meta['asset_id']
                url = self.build_url(asset_id,self.next_offset)
                yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True, meta={'asset_id':asset_id})
                self.next_offset += self.page_size

    def parse_article_detail(self, response):
        asset = response.meta['asset']
        ########################
        datePublished = asset['datePublished']
        description = asset['description']
        title = asset['title']
        # headline = asset['headline']
        linkHeadline = asset['linkHeadline']
        author = []
        for i in asset['author']:
            author.append(i['name'])

        article_text = response.xpath('//div[@class="group"]/p//text()').extract()
        published_time_str = asset['datePublished']
        if published_time_str:
            published_time = parse(published_time_str)
            # Convert the datetime to UTC timezone
            published_time_utc = published_time.astimezone(pytz.utc)
            if published_time_utc < pytz.utc.localize(datetime(2021, 1, 1)) or published_time_utc > pytz.utc.localize(datetime(2023, 4, 30)):
                return None
            else:
                yield {
                    'title':title,
                    'author': ' '.join(author), 
                    'datePublished':datePublished,
                    'linkHeadline':linkHeadline,
                    'url':response.url,
                    'short_description':description,
                    'article_text':article_text
                }
    def build_url(self, asset_id, offset):
        variables = self.query_variables.format(asset_id, offset, self.page_size)
        extensions = self.query_extensions.format("43ed5bcff58371b2637d1f860e593e2b56295195169a5e46209ba0abb85288b7")
        return f"{self.base_url}/graphql?operationName=getAssetList&variables={variables}&extensions={extensions}"


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished

