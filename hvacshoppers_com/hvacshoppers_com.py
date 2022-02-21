
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
from lazy_crawler.lib.image import process_image_instagram


class LazyCrawler(LazyBaseCrawler):
    
    name = "quotes"
    
    page_number = 2
    
    def start_requests(self):

        url = 'https://hvacshoppers.com/product-category/brand/page/{}/'.format(self.page_number)
        # for url in urls:        
            # url = "https://www.proshop.dk/Grafikkort/ASUS-GeForce-RTX-3070-Ti-TUF-OC-8GB-GDDR6X-RAM-Grafikkort/8500469"
        yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        # products = response.xpath("//*[@id="left-area"]/ul/li[1]/a[1]/@href").extract()
        products = response.xpath('//ul[@class="products columns-3"]/li/a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]/@href').extract()
    
        for product in products:
            yield scrapy.Request(product, self.parse_product, dont_filter=True)
    
    def parse_product(self, response):
        product_url = response.url
        product_name = response.xpath('//h1[@class="product_title entry-title"]/text()').extract_first()
        image_url = response.xpath('//div[@class="woocommerce-product-gallery__image"]/a/@href').extract_first()
        price = response.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/bdi/text()').extract_first()
        sku = response.xpath('//span[@class="sku_wrapper"]/span[@class="sku"]/text()').extract_first()
        desc = response.xpath('//div[@class="richText-root-2t- "]//text()').extract()
        # import ipdb; ipdb.set_trace()
        #download image
        res=process_image_instagram(image_url, "random")
        
        yield{
            
            'Product Name': product_name,
            "Price": price,
            "Sku": sku,
            "Description": desc,
            "image_url": image_url,
            'product_url': product_url,
        }
        # pass to new page  
        
        if self.page_number < 4:
            
            self.page_number += 1
            
            yield scrapy.Request(
                'https://hvacshoppers.com/product-category/brand/page/{}/'.format(self.page_number),
                self.parse,
                dont_filter=True
            )

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
