import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import base64

from lazy_crawler.lib.user_agent import get_user_agent

class LazyCrawler(scrapy.Spider):

    name = "bloomberg"
    allowed_domains = ['www.bloomberg.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 4,'RANDOMIZE_DOWNLOAD_DELAY':False,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'JOBDIR': './crawls', 'RETRY_TIMES': 4, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 500,
        'ITEM_PIPELINES' : {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': None
        },
        'handle_httpstatus_list' : [500, 503, 504, 400, 408, 307, 403],
    }



    def start_requests(self):
        sections = ['economics']

        for section in sections:
            url = 'https://www.bloomberg.com/lineup-next/api/paginate?id=story_list_2&page={}-v2&offset=0'.format(section)

            yield scrapy.Request(url, self.parse_json, dont_filter=True, meta={'section_id':section}, headers ={'User-Agent': get_user_agent('random')})

    def parse_json(self, response):
        try:
            res = response.json()
            # process the JSON data

        except json.decoder.JSONDecodeError as e:
            self.logger.error("Error parsing JSON response: %s", str(e))
            return




settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start()
