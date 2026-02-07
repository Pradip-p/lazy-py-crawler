
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import logging

class EisauCrawler(LazyBaseCrawler):
    name = "eisau"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 2,
        'RETRY_TIMES': 3,
        'COOKIES_ENABLED': True,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300,
        }
    }

    def start_requests(self):
        url = 'https://www.eisau.com.au/industries-and-categories/'
        yield scrapy.Request(url, self.parse_start_page)

    def parse_start_page(self, response):
        # Extract all category links directly
        category_links = response.xpath('//a[contains(@href, "/listing-category/")]/@href').getall()

        # Deduplicate links
        category_links = list(set(category_links))

        self.logger.info(f"Found {len(category_links)} categories")

        for url in category_links:
            yield scrapy.Request(url, self.parse_listings, dont_filter=True)

    def parse_listings(self, response):
        self.logger.info(f"Parsing category: {response.url}")

        # Iterate over each listing card
        listings = response.xpath('//li[contains(@class, "listing_cards")]')

        for listing in listings:
            # Extract basic info from hidden inputs or text
            business_name = listing.xpath('.//input[@name="listing_title"]/@value').get()
            email = listing.xpath('.//input[@name="provider_email"]/@value').get()
            listing_url = listing.xpath('.//input[@name="lising_url"]/@value').get()

            # Fallback if hidden inputs are missing
            if not business_name:
                business_name = listing.xpath('.//a[contains(@class, "listing_header_title")]/text()').get()
            if not listing_url:
                listing_url = listing.xpath('.//a[contains(@class, "listing_header_title")]/@href').get()

            # Phone
            # The phone might be hidden or in a span. User provided HTML shows <a class="hidephone" href="tel:...">
            phone = listing.xpath('.//a[@class="hidephone"]/text()').get()

            # Categories (Industry -> Category, Category -> Sub-Category based on user request/html structure)
            # HTML:
            # Industry -> Canteens...
            # Category -> Equipment Supply...

            # Using specific table text matches
            industry = listing.xpath('.//td[contains(@class, "listing_table_title")][contains(., "Industry")]/following-sibling::td//a/text()').getall()
            industry = ", ".join(industry) if industry else ""

            sub_category = listing.xpath('.//td[contains(@class, "listing_table_title")][contains(., "Category")]/following-sibling::td//a/text()').getall()
            sub_category = ", ".join(sub_category) if sub_category else ""

            item_data = {
                'Business Name': business_name,
                'Email Address': email,
                'Phone Number': phone,
                'Category': industry,      # User's "Category" maps to site's "Industry" likely, or vice versa.
                                           # User asked for "Category, Sub- Category".
                                           # Site has "Industry" (High level) and "Category" (Specific).
                                           # I will map Industry -> Category, Site Category -> Sub-Category.
                'Sub-Category': sub_category,
                'Listing URL': listing_url,
                'First Name': "",
                'Last Name': "",
                'Title': "",
                'Imported': ""
            }

            if listing_url:
                yield response.follow(
                    listing_url,
                    self.parse_detail,
                    cb_kwargs={'item': item_data},
                    errback=self.parse_detail_errback,
                    dont_filter=True
                )
            else:
                # If no listing URL, save what we have
                import datetime
                item_data['Imported'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item_data

        # Pagination
        next_page = response.xpath('//a[contains(@class, "next")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse_listings, dont_filter=True)

    def parse_detail(self, response, item):
        import datetime

        # User requested explicitly NOT to extract First/Last Name and Title.
        # Just processing the page to confirm it exists/was visited,
        # but leaving these fields empty as per instruction.

        first_name = ""
        last_name = ""
        title = ""

        item['First Name'] = first_name
        item['Last Name'] = last_name
        item['Title'] = title
        item['Imported'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield item

    def parse_detail_errback(self, failure):
        self.logger.error(f"Failed to fetch detail page: {failure.request.url} - {failure.value}")
        item = failure.request.cb_kwargs['item']

        import datetime
        # Ensure fields exist even if empty
        item['First Name'] = item.get('First Name', "")
        item['Last Name'] = item.get('Last Name', "")
        item['Title'] = item.get('Title', "")
        item['Imported'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield item

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(EisauCrawler)
process.start()
