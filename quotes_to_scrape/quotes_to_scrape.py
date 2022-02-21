
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
from lazy_crawler.lib.html import to_browser

class LazyCrawler(LazyBaseCrawler):
    print( os.environ.get('APP_ENV'))
    
    name = "quotes"
    
    def start_requests(self):
        settings = get_project_settings()
        
        print("Your USER_AGENT is:\n%s" % (settings.get('ITEM_PIPELINES')))
        
        url = 'http://quotes.toscrape.com/'
        
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # to_browser(response)
        for quote in response.css('div.quote'):
            yield {
                'author': quote.css('small.author::text').get(),
                'text': quote.css('span.text::text').get(),
                'tag':quote.css('.tags a.tag::text').get(),
                
                
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
