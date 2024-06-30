
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
import logging
from scrapy.linkextractors import LinkExtractor
import scrapy
import string
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionLost
from twisted.internet import reactor


# from lazy_crawler.puppeteer.puppeteer import browse
class LazyCrawler(LazyBaseCrawler):

    logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
    )
    
    custom_settings = {
        'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 126,'CONCURRENT_REQUESTS_PER_IP': 26,'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'JOBDIR': './crawls', 'RETRY_TIMES': 2, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 500,
        'ITEM_PIPELINES' : {
        'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': None
        },
        'DOWNLOAD_DELAY': 0,
        'RETRY_HTTP_CODES': [402],
    }

    # Create an empty set to store unique words
    unique_words = set()

    settings = get_project_settings()
    
    headers = get_user_agent('random')

    def start_requests(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        url = 'https://www.phrases.com/letter/0'
        # for letter in alphabet:
        #     url = 'https://www.phrases.com/letter/{}/99999'.format(letter)

            # yield scrapy.Request(url, self.get_urls, dont_filter=True)
        yield scrapy.Request(url, self.get_urls, errback=self.handle_error, dont_filter=True)
    
    def handle_error(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 402:
                self.logger.warning(f'HTTP Error 402 on {response.url}, retrying in 10 seconds...')
                return self._retry(failure.request, 10)
        elif failure.check(TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionLost):
            self.logger.warning(f'Timeout error on {failure.request.url}, retrying...')
            return self._retry(failure.request)

        self.logger.error(repr(failure))

    def _retry(self, request, delay=0):
        if not delay:
            return request.copy()

        new_request = request.copy()
        new_request.dont_filter = True
        reactor.callLater(delay, self.crawler.engine.schedule, new_request, self)
        return None
    
    def get_urls(self, response):
        urls = response.xpath('//table[@class="tdata"]/tbody/tr/td/a/@href').extract()

        for url in urls:
            url = 'https://www.phrases.com'+ url
            yield scrapy.Request(url, self.get_text, errback=self.handle_error, dont_filter=True)
    
    def get_text(self, response):
        word = response.xpath('//h1/a/span/text()').extract_first()
        
        # Write the unique words to a file
        with open('phrases_One.txt', 'a') as f:
            if word:
                if word not in self.unique_words:
                    f.write(word + '\n')
                    self.unique_words.add(word)


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished

