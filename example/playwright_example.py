import os
import scrapy
from scrapy.crawler import CrawlerProcess
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler

class PlaywrightSpider(LazyBaseCrawler):
    name = "playwright_spider"

    # We can use the helper method from LazyBaseCrawler
    def start_requests(self):
        url = "https://example.com"
        yield self.playwright_request(url, self.parse)

    def parse(self, response):
        # The response is now fully rendered by Playwright
        yield {
            "title": response.css("h1::text").get(),
            "url": response.url,
            "playwright_rendered": True
        }

if __name__ == "__main__":
    # Ensure Scrapy settings are loaded
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'lazy_crawler.crawler.settings')

    from scrapy.utils.project import get_project_settings
    process = CrawlerProcess(get_project_settings())
    process.crawl(PlaywrightSpider)
    process.start()
