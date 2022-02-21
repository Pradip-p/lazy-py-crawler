
from email.mime import image
from ipaddress import ip_address
import os
from traceback import print_tb
from numpy import product
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
from lazy_crawler.lib.html import to_browser

class LazyCrawler(LazyBaseCrawler):
    
    name = "quotes"
    
    page_number = 2
    
    def start_requests(self):

        # url = 'https://hvacshoppers.com/product-category/brand/page/{}/'.format(self.page_number)
        url = "https://www.contactcanada.com/database/companies.php?portal=6&s=0&l=90"
        # for url in urls:        
            # url = "https://www.proshop.dk/Grafikkort/ASUS-GeForce-RTX-3070-Ti-TUF-OC-8GB-GDDR6X-RAM-Grafikkort/8500469"
        yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
    
        companys = response.xpath('//ul[@class="listResults"]/li/a/@href').extract()
        
        for url in companys:
            url = "https://www.contactcanada.com/database/" + url
            yield scrapy.Request(url, self.parse_product, dont_filter=True)
    
    def parse_product(self, response):
        # print(response.url)
        company_name = response.xpath('//h2[@class="headingCompany"]/text()').extract_first()
        # address = response.xpath('//div[@profileSectionWrapper]/p[@class="profileAddress"]/text()').extract_first()
        # tel = response.xpath('//div[@profileSectionWrapper]/ul[class="profileNumbers"]/li/text()').extract_first()
        # import ipdb; ipdb.set_trace()
        yield{
            "Company_Name": company_name,
            # "Address": address,
            # "Tel": tel,
        }
        # pass to new page  
        
        # if self.page_number < 4:
            
        #     self.page_number += 1
            
        #     yield scrapy.Request(
        #         'https://hvacshoppers.com/product-category/brand/page/{}/'.format(self.page_number),
        #         self.parse,
        #         dont_filter=True
        #     )

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
