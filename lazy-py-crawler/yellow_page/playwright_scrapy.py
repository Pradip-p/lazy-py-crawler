import scrapy
import os
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent
from scrapy.spidermiddlewares.httperror import HttpError

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"


class AwesomeSpider(scrapy.Spider):
    name = "yellowpages"
    allowed_domains = ['yellowpages.com.au']
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'RETRY_TIMES': 1,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'REDIRECT_ENABLED' : False,
        "DOWNLOAD_HANDLERS": DOWNLOAD_HANDLERS,
        "TWISTED_REACTOR": TWISTED_REACTOR,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        },
        'DOWNLOAD_DELAY': 4,  # Delay in seconds
    }
    def errback_http_ignored(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status in [302,403]:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                print('Waiting for a second and re-calling with a new proxy IP')
                # time.sleep(100)  # Wait for a second
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

    def _retry_request(self, request, reason, spider):
        retryreq = request.copy()
        retryreq.meta['retry_times'] = request.meta.get('retry_times', 0) + 1
        retryreq.dont_filter = True
        proxy = {
        "server": "http://proxy.speedproxies.net:12321",
        "proxy_username": "curadigitala4828",
        "proxy_password": "34d89f51e9f5",
        }
        retryreq.meta['playwright_context_kwargs']['proxy'] = proxy
        return retryreq

    def start_requests(self):
        # GET request
        search_terms = ["massage"]  # Replace with the desired search terms

        for search_term in search_terms:

            # for page_num in range(1, 30):
            headers = {
            "User-Agent": get_user_agent('random'),
            "Referer": "https://www.yellowpages.com.au/",
            }
            # url = f"https://www.yellowpages.com.au/search/listings?clue={search_term}&locationClue=All+States"
            url = 'https://www.yellowpages.com.au/search/listings?clue=massage&locationClue=All+States'
            yield scrapy.Request(
                url=url,
                headers= headers,
                meta={
                    "playwright": True,
                    "playwright_context": "new",
                    "playwright_context_kwargs": {
                        "java_script_enabled": False,
                        "ignore_https_errors": True,
                        "proxy": {
                            "server": "http://proxy.speedproxies.net:12321",
                            "username": "curadigitala4828",
                            "password": "34d89f51e9f5",
                        },
                    },
                },
                # errback=self.errback_http_ignored,  # Assign the error callback
                dont_filter=True
            )


    def parse(self, response):
        # name = response.xpath("//h3[contains(@class,'MuiTypography-root')]/text()").extract()
        # phone = response.xpath('//span[@class="MuiButton-label"]/text()').extract()
        # yield{
        #     'name': name,
        #     'Phone': phone
        # }

        # main_div = response.xpath('//div[@class="Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded"]')
        # print('*'*10, main_div)
        # for res in main_div:
            # url = res.xpath('.//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/@href').extract_first()
            # name = res.xpath('.//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/h3/text()').extract_first()
            # short_desc = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 bKFqNV"]/p/text()').extract_first()
            # ph_num = res.xpath('.//button[@class="MuiButtonBase-root MuiButton-root MuiButton-text ButtonPhone MuiButton-textPrimary MuiButton-fullWidth"]/span[@class="MuiButton-label"]/text()').extract_first()
            # desc = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 iswkLA"]//text()').extract()
            # addr = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 bvRSwt"]/a/p/text()').extract_first()
            # website = res.xpath('.//a[@class="MuiButtonBase-root MuiButton-root MuiButton-text ButtonWebsite MuiButton-textSecondary MuiButton-fullWidth"]/@href').extract_first()
            # name = res.xpath("//h3[contains(@class,'MuiTypography-root')]/text()").extract_first()
            # yield {
                # 'Name': name,
                # 'Phone Number': ph_num,
                # 'Address': addr,
                # 'URL': 'https://www.yellowpages.com.au{}'.format(url),
                # 'Website': website,
                # 'Short Desc': short_desc,
                # 'Description': ' '.join(desc),
                # 'Scrapped URL': response.url
            # }

        # 'response' contains the page as seen by the browser

        urls = response.xpath('//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/@href').extract()
        for url in urls:
            url = 'https://www.yellowpages.com.au{}'.format(url)
            headers = {
            "User-Agent": get_user_agent('random'),
            "Referer": "https://www.yellowpages.com.au/",
            }

            yield scrapy.Request(
                    url=url,
                    callback=self.parse_page,
                    headers= headers,
                    meta={
                        "playwright": True,
                        "playwright_context": "new",
                        "playwright_context_kwargs": {
                            "java_script_enabled": False,
                            "ignore_https_errors": True,
                            "proxy": {
                                "server": "http://proxy.speedproxies.net:12321",
                                "username": "curadigitala4828",
                                "password": "34d89f51e9f5",
                            },
                        },
                    },
                    # errback=self.errback_http_ignored,  # Assign the error callback
                    dont_filter=True
                )

    def parse_page(self, response):
        name = response.xpath('//h1/a[@class="listing-name"]/text()').extract_first()
        addr = response.xpath('//div[@class="listing-address mappable-address mappable-address-with-poi"]/text()').extract_first()
        phone = response.xpath('//a[@class="click-to-call contact contact-preferred contact-phone"]/@href').extract_first()
        email = response.xpath('//div[@class="contacts"]/div[@class="main"]/a[@class="contact contact-main contact-email"]/@data-email').extract_first()
        website = response.xpath('//div[@class="contacts"]/div[@class="main"]/a[@class="contact contact-main contact-url"]/@href').extract_first()
        details = response.xpath('//p[@class="details"]/text()').extract()
        desc = response.xpath('//ul[@class="item-list item-list-usp"]/li/text()').extract()
        full_desc = ' '.join(details) + ' '.join(desc)

        yield{
            'Name': name,
            'Address': addr,
            'Phone': phone,
            'Email': email,
            "Website":website,
            "URL": response.url,
            'Description': full_desc
        }


        # main_div = response.xpath('//div[@class="Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded"]')
        # print('*'*10, main_div)
        # for res in main_div:
        #     url = res.xpath('.//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/@href').extract_first()
        #     name = res.xpath('.//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/h3/text()').extract_first()
        #     short_desc = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 bKFqNV"]/p/text()').extract_first()
        #     ph_num = res.xpath('.//button[@class="MuiButtonBase-root MuiButton-root MuiButton-text ButtonPhone MuiButton-textPrimary MuiButton-fullWidth"]/span[@class="MuiButton-label"]/text()').extract_first()
        #     desc = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 iswkLA"]//text()').extract()
        #     addr = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 bvRSwt"]/a/p/text()').extract_first()
        #     website = res.xpath('.//a[@class="MuiButtonBase-root MuiButton-root MuiButton-text ButtonWebsite MuiButton-textSecondary MuiButton-fullWidth"]/@href').extract_first()

        #     yield {
        #         'Name': name,
        #         'Phone Number': ph_num,
        #         'Address': addr,
        #         'URL': 'https://www.yellowpages.com.au{}'.format(url),
        #         'Website': website,
        #         'Short Desc': short_desc,
        #         'Description': ' '.join(desc),
        #         'Scrapped URL': response.url
        #     }

        #next page urls
        # last_next_page_url = response.xpath('//a/span[contains(text(), "Next")]/ancestor::a/@href').get()
        # # next_page_urls = response.xpath('//a[@class="MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-fullWidth"]/@href').extract()
        # # last_next_page_url = next_page_urls[-1] if next_page_urls else None
        # print('*'*10, last_next_page_url)
        # if last_next_page_url:
        #     last_next_page_url = 'https://www.yellowpages.com.au{}'.format(last_next_page_url)
        #     headers = {
        #     "User-Agent": get_user_agent('random'),
        #     "Referer": "https://www.yellowpages.com.au/",
        #     }

        #     yield scrapy.Request(
        #             url=last_next_page_url,
        #             callback=self.parse,
        #             headers= headers,
        #             meta={
        #                 "playwright": True,
        #                 "playwright_context": "new",
        #                 "playwright_context_kwargs": {
        #                     "java_script_enabled": False,
        #                     "ignore_https_errors": True,
        #                     "proxy": {
        #                         "server": "http://proxy.speedproxies.net:12321",
        #                         "username": "curadigitala4828",
        #                         "password": "34d89f51e9f5",
        #                     },
        #                 },
        #             },
        #             errback=self.errback_http_ignored,  # Assign the error callback
        #             dont_filter=True
        #         )

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(AwesomeSpider)
process.start() # the script will block here until the crawling is finished
