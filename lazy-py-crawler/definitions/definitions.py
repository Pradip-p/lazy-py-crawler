
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
import logging
from scrapy.linkextractors import LinkExtractor
import scrapy
import string

# from lazy_crawler.puppeteer.puppeteer import browse
class LazyCrawler(LazyBaseCrawler):

    # Create an empty set to store unique words
    unique_words = set()

    custom_settings = {
        'DOWNLOAD_DELAY': 0,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 126,'CONCURRENT_REQUESTS_PER_IP': 26,'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'JOBDIR': './crawls', 'RETRY_TIMES': 2, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 500,
        'ITEM_PIPELINES' : {
        'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': None
        }
    }


    settings = get_project_settings()
    

    def start_requests(self):
        another_urls = [
            'https://www.rhymes.com/rhymes/0'
            'https://www.definitions.net/definitions/0/99999',
            'https://www.synonyms.com/synonyms/0/EN',
        ]
        
        urls = [
            'https://www.anagrams.net/letter/{}/99999',
            'https://www.rhymes.com/rhymes/{}/99999',
            'https://www.definitions.net/definitions/{}/99999',
            'https://www.synonyms.com/synonyms/{}/99999'
        ]

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for url in urls:
            for letter in alphabet:
                formatted_url = url.format(letter)
                yield scrapy.Request(formatted_url, self.get_text, dont_filter=True,headers={
                'User-Agent': get_user_agent('random')
            })
        
        for url in another_urls:
            yield scrapy.Request(formatted_url, self.get_text, dont_filter=True,headers={
                'User-Agent': get_user_agent('random')
            })



    def get_text(self, response):
        text = response.xpath('//table[@class="tdata"]/tbody/tr/td/a/text()').extract()
        
        # Remove left and right spaces from each word
        text = [word.strip() for word in text]
        
        # Write the unique words to a file
        with open('phrases.txt', 'a') as f:
            for word in set(text):
                if word not in self.unique_words:
                    f.write(word + '\n')
                    self.unique_words.add(word)

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished

