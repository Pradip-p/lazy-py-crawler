import scrapy
import os
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"


class AwesomeSpider(scrapy.Spider):
    name = "awesome"
    
    custom_settings = {
        "DOWNLOAD_HANDLERS": DOWNLOAD_HANDLERS,
        "TWISTED_REACTOR": TWISTED_REACTOR,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        },
        'DOWNLOAD_DELAY': 2,  # Delay in seconds
    }
    def start_requests(self):
        # GET request
        for page_num in range(1, 3):
            headers = {
            "User-Agent": get_user_agent('random'),
            "Referer": "https://www.yellowpages.com.au/",
            }
            url = f"https://www.yellowpages.com.au/search/listings?clue=massage&locationClue=All+States&pageNumber={page_num}"
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
            )
            print('crawler waiting for 10 sec')
        # time.sleep(10)  # Delay between requests in seconds

    def parse(self, response):
        # 'response' contains the page as seen by the browser
        main_div = response.xpath('//div[@class="Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded"]')
        for res in main_div:
            name = res.xpath('.//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/h3/text()').extract_first()
            short_desc = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 bKFqNV"]/p/text()').extract_first()
            ph_num = res.xpath('.//button[@class="MuiButtonBase-root MuiButton-root MuiButton-text ButtonPhone MuiButton-textPrimary MuiButton-fullWidth"]/span[@class="MuiButton-label"]/text()').extract_first()
            desc = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 iswkLA"]//text()').extract()
        #     addr = res.xpath('.//p[@class="MuiTypography-root jss412 MuiTypography-body2"]/text()').extract_first()
            addr = res.xpath('.//div[@class="Box__Div-sc-dws99b-0 bvRSwt"]/a/p/text()').extract_first()
            yield {
                'Name': name,
                'Phone Number': ph_num,
                'Address': addr,
                'Short Desc': short_desc,
                'Description': ' '.join(desc)
            }

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(AwesomeSpider)
process.start() # the script will block here until the crawling is finished
