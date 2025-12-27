import scrapy
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler


class TestStealthSpider(LazyBaseCrawler):
    name = "test_stealth"
    start_urls = ["https://bot.sannysoft.com/"]

    def start_requests(self):
        for url in self.start_urls:
            yield self.playwright_request(url, self.parse)

    def parse(self, response):
        self.logger.info(f"Response status: {response.status}")
        # Capture a screenshot if possible or just check the title/content
        # In a real scenario, we'd check if specific "bot detected" strings are absent.
        self.logger.info(f"Page title: {response.css('title::text').get()}")
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
        }
