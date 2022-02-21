
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
from lazy_crawler.lib.html import to_browser

class LazyCrawler(LazyBaseCrawler):

    
    def start_requests(self):

        urls = ['https://oricom.com.au/product-category/products/oricom-uhf-cb-radios/handheld/'
               'https://oricom.com.au/product-category/products/oricom-uhf-cb-radios/antennas/',
               'https://oricom.com.au/product-category/products/oricom-uhf-cb-radios/antenna-whips/',
               'https://oricom.com.au/product-category/products/oricom-uhf-cb-radios/brackets/',
               'https://oricom.com.au/product-category/products/tyre-pressure-monitors/',
               'https://oricom.com.au/product-category/products/oricom-vhf-marine-radios/fixed-mount-radios/',
               'https://oricom.com.au/product-category/products/vhf-marine-radios/handheld-vhf-marine-radios/',
               'https://oricom.com.au/product-category/products/oricom-vhf-marine-radios/marine-antennas/',
               'https://oricom.com.au/product-category/products/oricom-vhf-marine-radios/marine-brackets/',
               'https://oricom.com.au/product-category/products/oricom-uhf-cb-radios/bundle-and-save/',
               'https://oricom.com.au/product-category/products/oricom-uhf-cb-radios/premium-fixed-mount/',
               'https://oricom.com.au/product-category/products/oricom-uhf-cb-radios/fixed-mount/',
               'https://oricom.com.au/product-category/products/oricom-uhf-cb-radios/premium-handheld-radios/'
               ]
        for url in urls:        
            # url = "https://www.proshop.dk/Grafikkort/ASUS-GeForce-RTX-3070-Ti-TUF-OC-8GB-GDDR6X-RAM-Grafikkort/8500469"
            yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        # to_browser(response)
        product_url=response.xpath('//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]/@href').extract()
        for url in product_url:
            yield scrapy.Request(url, self.parse_product, dont_filter=True)
    
    def parse_product(self, response):
        # to_browser(response)
        sku = response.xpath('//span[@class="sku_wrapper"]/span[@class="sku"]/text()').extract_first()
        title = response.xpath('//h1[@class="product_title entry-title"]/text()').extract_first()
        price = response.xpath('//span[@class="woocommerce-Price-amount amount"]/bdi/text()').extract_first()
        image_url = response.xpath('//meta[@property="og:image"]/@content').extract_first()
        # desc = response.xpath('//div[@class="woocommerce-product-details__short-description"]').extract()
        key_feature = response.xpath('//div[@class="one_half"]/ul/li').extract()
        pack = response.xpath('//div[@id="tab-pack-includes"]/ul/li').extract()
        spec_sheet_url = response.xpath('//div[@id="tab-spec-sheet"]/p/a/@href').extract()
        user_guide_url = response.xpath('//div[@id="tab-user-guides"]/p/a/@href').extract()
        desc = key_feature + pack
        # import ipdb; ipdb.set_trace()
        yield{
            "SKU": sku,
            "Title": title,
            "Description": ' '.join(desc), #(converted into HTML) Key features and Pack Includes.
            "Spec sheet URL":','.join(spec_sheet_url), 
            "User Guide URL":','.join(user_guide_url),
            "Image URL":image_url,
            "Price":price,
            "Accessories":"",#(list of skus, seperated by comma)
        }

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start(stop_after_crawl=False ) # the script will block here until the crawling is finished
