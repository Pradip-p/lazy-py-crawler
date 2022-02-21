#PID: 1 Description: test

import os
import sys
import scrapy
from scrapy import settings
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import logging
class LazyCrawler(LazyBaseCrawler):
    
    name = "quotes"
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 0,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
    #     'CONCURRENT_REQUESTS' : 1,'JOBDIR': './crawls', 'RETRY_TIMES': 20, "COOKIES_ENABLED": True
    #     }


    # custom_settings = {
    #     'ITEM_PIPELINES': {  
    #         "lazy_crawler.crawler.pipelines.MongoPipeline": 300
    #     }
    # }

    def start_requests(self):
        settings = get_project_settings()
        print("Your USER_AGENT is:\n%s" % (settings.get('ITEM_PIPELINES')))
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            }
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

# settings = get_project_settings()
# settings.update({
#     "LOG_ENABLED": "True",
# })
# # init the logger using setting
# configure_logging(settings)
# runner = CrawlerRunner(settings)
# runner.crawl(GrepsrBaseCrawler)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())
# reactor.run() # the script will block here until all crawling jobs are finished






process = CrawlerProcess()  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
