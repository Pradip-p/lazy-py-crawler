
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
        url = 'https://www.eisau.com.au/listing-category/equipment-supply/'
        yield scrapy.Request(url, self.parse_listings)

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
                'Listing URL': listing_url
            }

            if listing_url:
                yield response.follow(listing_url, self.parse_detail, cb_kwargs={'item': item_data})

        # Pagination
        next_page = response.xpath('//a[contains(@class, "next")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse_listings)

    def parse_detail(self, response, item):
        import datetime
        import re

        # Try to find contact person info from the full text
        # Patterns: "Contact:", "Contact Person:", "Key Contact:"
        text = " ".join(response.xpath('//body//text()').getall())

        # Enhanced regex list
        patterns = [
            r'(?:Contact(?:\sPerson)?|Key\sContact|Director|Manager)\s*:\s*([A-Za-z\s\.]+)',
        ]

        full_name = ""
        for pattern in patterns:
            contact_match = re.search(pattern, text, re.IGNORECASE)
            if contact_match:
                full_name = contact_match.group(1).strip()
                break

        first_name = ""
        last_name = ""
        title = ""

        # Fallback to email if no name found
        if not full_name and item.get('Email Address'):
            email_parts = item['Email Address'].split('@')[0].split('.')
            if len(email_parts) >= 1:
                # Filter out generic terms
                if email_parts[0].lower() not in ['info', 'sales', 'admin', 'enquiry', 'enquiries', 'support', 'office']:
                    full_name = " ".join([p.capitalize() for p in email_parts])

        if full_name:
            # Split into first/last (naive)
            parts = full_name.split()
            if len(parts) >= 1:
                first_name = parts[0]
            if len(parts) >= 2:
                last_name = " ".join(parts[1:])

        item['First Name'] = first_name
        item['Last Name'] = last_name
        item['Title'] = title
        item['Imported'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield item

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(EisauCrawler)
process.start()
