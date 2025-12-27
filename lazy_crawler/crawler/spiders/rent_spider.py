import scrapy
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler


class RentSpider(LazyBaseCrawler):
    name = "rent_spider"
    start_urls = ["https://www.rent.com/georgia/atlanta-apartments"]

    def start_requests(self):
        print("Starting RentSpider with Playwright and stealth settings...")
        for url in self.start_urls:
            # Using playwright_request from LazyBaseCrawler which includes stealth
            yield self.playwright_request(url, self.parse)

    def parse(self, response):
        self.logger.info(f"Successfully reached: {response.url}")
        self.logger.info(f"Page Title: {response.css('title::text').get()}")

        # Simple extraction to see if we got actual content or a challenge page
        listings = response.css('article[data-testid="property-card"]')
        self.logger.info(f"Found {len(listings)} property listings.")
        print("*" * 100)

        if len(listings) == 0:
            self.logger.warning(
                "No listings found. We might be seeing a CAPTCHA or a different page structure."
            )
            # Check for common CAPTCHA indicators
            if (
                "captcha" in response.text.lower()
                or "challenge" in response.text.lower()
            ):
                self.logger.error("CAPTCHA detected!")

        for listing in listings:
            yield {
                "name": listing.css('div[data-testid="property-title"]::text').get(),
                "price": listing.css('span[data-testid="property-price"]::text').get(),
                "address": listing.css(
                    'div[data-testid="property-address"]::text'
                ).get(),
            }
