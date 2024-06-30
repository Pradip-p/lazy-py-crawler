import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent
import gc
import csv
import random
import time
from scrapy.spidermiddlewares.httperror import HttpError

class LazyCrawler(scrapy.Spider):

    name = "yellow_page"
    allowed_domains = ['yellowpages.com.au']
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 2,
        'COOKIES_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 180,
        'REDIRECT_ENABLED' : False,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }
    
    def errback_http_ignored(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 430 or 302:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                print('crawler waiting for 4 minutes')
                time.sleep(30)  # Wait for 4 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

            if response.status == 503:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                time.sleep(480)  # Wait for 8 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

    def _retry_request(self, request, reason, spider):
        retryreq = request.copy()
        retryreq.meta['retry_times'] = request.meta.get('retry_times', 0) + 1
        retryreq.dont_filter = True
        return retryreq
    
    HEADERS = {
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        # "Accept-Language": "en-US,en;q=0.5",
        # "Accept-Encoding": "gzip, deflate",
        # "Connection": "keep-alive",
        # "Upgrade-Insecure-Requests": "1",
        # "Sec-Fetch-Dest": "document",
        # "Sec-Fetch-Mode": "navigate",
        # "Sec-Fetch-Site": "none",
        # "Sec-Fetch-User": "?1",
        # "Cache-Control": "max-age=0",
        ##new header files.
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.yellowpages.com.au',
        'Upgrade-Insecure-Requests': '1',
        #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    
    def start_requests(self):
        for page_num in range(1,35):
            proxy_list = self.read_proxy_list_from_csv('proxy_list.csv')
            if not proxy_list:
                self.logger.error('No proxies found in the CSV file.')
                return

            proxy = random.choice(proxy_list)
            proxy_url = f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
        
            url = 'https://www.yellowpages.com.au/search/listings?clue=massage&locationClue=All+States&pageNumber={}'.format(page_num)    
            # url = 'https://www.yellowpages.com.au/search/listings?clue=massage&locationClue=All+States'
            headers = {
                'User-Agent': get_user_agent('random'),
                **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
                }
            
            yield scrapy.Request(url, callback=self.parse_load, 
                                meta={
                                    'proxy': proxy_url,
                                    'proxy_auth': f'{proxy["user"]}:{proxy["pass"]}',
                                    'handle_httpstatus_list': [407],  # Retry on 407 Proxy Authentication Required
                                    'proxy_list':proxy_list
                                },
                                errback=self.errback_http_ignored,
                                headers= headers, 
                                dont_filter=True)

    def parse_load(self, response):
        main_div = response.xpath('//div[@class="Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded"]')
        for res in main_div:
            name = res.xpath('//h3[@class="MuiTypography-root jss288 MuiTypography-h3 MuiTypography-displayBlock"]/text()').extract_first()
            addr = res.xpath('//p[@class="MuiTypography-root jss289 MuiTypography-body2 MuiTypography-colorTextSecondary"]/text()').extract_first()
            ph_num = res.xpath('//button[@class="MuiButtonBase-root MuiButton-root MuiButton-text ButtonPhone MuiButton-textPrimary MuiButton-fullWidth"]/span[@class="MuiButton-label"]/text()').extract_first()
            short_desc = res.xpath('//p[@class="MuiTypography-root jss302 MuiTypography-subtitle2"]/text()').extract_first()
            desc  =res.xpath('//div[@class="Box__Div-sc-dws99b-0 iswkLA"]//text()').extract()
            
            yield{
                'Name': name,
                'Address': addr,
                'Phone Number': ph_num,
                'Short Desc': short_desc,
                'Description': ' '.join(desc) 
            }
            
            
            
            
            
            
            
            
            
        # next_url =  response.xpath('//a[@class="MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-fullWidth"]/@href').extract_first()
        # if next_url:
        #     url = 'https://www.yellowpages.com.au'.format(next_url)
        #     proxy = random.choice(response.meta['proxy_list'])
        #     proxy_url = f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
        #     # yield scrapy.Request(url, callback=self.parse_load, meta=response.meta, dont_filter=True)
        #     headers = {
        #     'User-Agent': get_user_agent('random'),
        #     }
        #     yield scrapy.Request(url, callback=self.parse_load, 
        #                      meta={
        #                         'proxy': proxy_url,
        #                         'proxy_auth': f'{proxy["user"]}:{proxy["pass"]}',
        #                         'handle_httpstatus_list': [407],  # Retry on 407 Proxy Authentication Required
        #                         'proxy_list':response.meta['proxy_list']
        #                     },
        #                     errback=self.errback_http_ignored,
        #                     headers= headers, 
        #                     dont_filter=True)

        # name = response.xpath('//h3[@class="MuiTypography-root jss371 MuiTypography-h3 MuiTypography-displayBlock"]/text()').extract()
        # short = response
        # urls = response.xpath('//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/@href').extract()
    
        # proxy_list = self.read_proxy_list_from_csv('proxy_list.csv')

        # if not proxy_list:
        #     self.logger.error('No proxies found in the CSV file.')
        #     return
    
        # urls = response.xpath('//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/@href').extract()
        # for url in urls:
        #     proxy = random.choice(proxy_list)
        #     proxy_url = f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
        
        #     url = 'https://www.yellowpages.com.au' + url
        #     yield scrapy.Request(url, callback=self.parse_page, meta={'proxy': proxy_url, 'proxy_auth': f'{proxy["user"]}:{proxy["pass"]}'}, dont_filter=True)

            # yield scrapy.Request(url, callback=self.parse_page, meta=response.meta, dont_filter=True)

    def parse_page(self, response):
        name = response.xpath('//h1/a[@class="listing-name"]/text()').get()
        address = response.xpath('//span[@class="glyph icon-pin-location"]/text()').get()
        short_desc = response.xpath('//p[@class="listing-short-description"]/text()').get()
        phone_no = response.xpath('//span[@class="text middle  "]/div[@class="desktop-display-value"]/text()').get()

        yield {
            'name': name,
            'Address': address,
            'Short Desc': short_desc,
            'phone number': phone_no
        }
        
    def read_proxy_list_from_csv(self, filename):
        proxy_list = []
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    proxy_parts = row[0].split(':')
                    proxy = {
                        'host': proxy_parts[0],
                        'port': proxy_parts[1],
                        'user': proxy_parts[2],
                        'pass': proxy_parts[3]
                    }
                    proxy_list.append(proxy)
        except FileNotFoundError:
            self.logger.error(f"CSV file '{filename}' not found.")
        except Exception as e:
            self.logger.error(f"Error reading proxy list from CSV: {e}")

        return proxy_list



# class LazyCrawler(LazyBaseCrawler):

#     name = "yellow_page"

#     custom_settings = {
#         'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',
#         'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,
#         'CONCURRENT_REQUESTS_PER_DOMAIN': 1,'RETRY_TIMES': 2,
#         "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,
#         'ITEM_PIPELINES' :  {
#         'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': None
#         }
#     }
    
#     # Proxy configuration
#     proxy_host = 'proxy.speedproxies.net'
#     proxy_port = '12321'
#     proxy_user = 'curadigitala4828'
#     proxy_pass = '34d89f51e9f5'
    
#     # Set the proxy for the spider
#     proxy = f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
    

#     def start_requests(self):
        
#         meta = {'proxy': self.proxy, 'proxy_auth': f'{self.proxy_user}:{self.proxy_pass}'}
#         # meta = {'proxy': proxy}
#         url='https://www.yellowpages.com.au/search/listings?clue=massage&locationClue=All+States'
#         # Start the request with the configured proxy
#         yield scrapy.Request(url, callback=self.parse, meta=meta, dont_filter=True)
        
        
#     def parse(self, response):
#         urls = response.xpath('//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]/@href').extract()
#         # Extract data from individual URLs
#         for url in urls:
#             url = 'https://www.yellowpages.com.au'.format(url)
#             yield scrapy.Request(url, callback=self.parse_page, meta=response.meta, dont_filter=True)
            
#         # next_page_url =  response.xpath('//a[@class="MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-fullWidth"]/@herf').extract_first()
#         # if next_page_url:
#         #     yield scrapy.Request(next_page_url, callback=self.parse, meta=response.meta, dont_filter=True)

            
            
#     def parse_page(self, response):
#         # Extract data from the page
#         # Example: Extracting the name and address
#         name = response.xpath('//h1/a[@class="listing-name"]/text()').get()
#         address = response.xpath('//span[@class="glyph icon-pin-location"]/text()').get()
#         short_desc = response.xpath('//p[@class="listing-short-description"]/text()').get()
#         phone_no = response.xpath('//span[@class="text middle  "]/div[@class="desktop-display-value"]/text()').get()
        
#         yield{
#             'name': name,
#             'Address': address,
#             'Short Desc': short_desc,
#             'phone number': phone_no
#         }


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished