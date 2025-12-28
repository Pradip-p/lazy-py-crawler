import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging

class QuotesCrawler(scrapy.Spider):

    name = "quotes"

    # Configure logging
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    # Custom settings
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'JOBDIR': './crawls',
        'RETRY_TIMES': 2,
        "COOKIES_ENABLED": False,
        'DOWNLOAD_TIMEOUT': 15,
    }

    # Start URL
    def start_requests(self):
        url = 'https://quotes.toscrape.com/'
        yield scrapy.Request(url, self.parse_quotes, dont_filter=True)

    # Parse each page of quotes
    def parse_quotes(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('span[@class="text"]/text()').get()
            author = quote.xpath('span/small[@class="author"]/text()').get()

            yield {
                'quote': text,
                'author': author,
            }

        # Follow the "Next" button link to scrape subsequent pages
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, self.parse_quotes)

# Initialize and run the CrawlerProcess with custom settings
process = CrawlerProcess(get_project_settings())
process.crawl(QuotesCrawler)
process.start()
