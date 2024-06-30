
import base64
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.html import to_browser
from lazy_crawler.lib.user_agent import get_user_agent
import ipdb
import re

class LazyCrawler(scrapy.Spider):

    name = "uclahealth"
    
    allowed_domains = ['uclahealth.org']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 2,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 180,
        'REDIRECT_ENABLED' : False,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
        }
    }
    
    def start_requests(self):

        url = 'https://www.uclahealth.org/departments/neurosurgery/education/residency-training/clinical-faculty'
        
        headers = {
            'User-Agent': get_user_agent('random'),
            }
        
        yield scrapy.Request(url, callback=self.parse_details,
                            headers= headers, 
                            dont_filter=True)
        # url = 'https://www.westchestermedicalcenter.org/neurosurgery2'
        # yield scrapy.Request(url, callback=self.parse_westchestermedicalcenter, dont_filter=True)

    def parse_details(self, response):
        faculty = response.xpath('//div[@class="space-y-6 group"]')
        for fac in faculty:
            item = {}  # Create an empty dictionary to store the item

            url = fac.xpath('.//a/@href').get('')
            text = fac.xpath('.//div[@class="font-serif font-normal text-lg md:text-xl text-almost-black leading-tight"]/div/text()').extract_first()
            faculty_name, degrees = (text.split(', ', 1) if text else (None, []))
            faculty_rank = fac.xpath('.//div[@class="text-sm mt-2 line-clamp-2"]/text()').extract_first()
            
            item['Faculty'] = {
                'Hospital Name':'uclahealth',
                'Website URL':'https://www.uclahealth.org/',
                'Faculty Name': faculty_name,
                'Faculty Degrees': degrees,
                'Faculty Training/Education History':'',
                'Faculty Rank': faculty_rank,
            }
            yield item
        
        # #another webiste
        # url = 'https://www.westchestermedicalcenter.org/neurosurgery2'
        # yield scrapy.Request(url, callback=self.parse_westchestermedicalcenter, dont_filter=True)
        
        
        
            
        url = 'https://www.uclahealth.org/departments/neurosurgery/education/residency-training/our-residents'
        yield scrapy.Request(url, callback=self.parse_residents, dont_filter=True)
        next_url = 'https://www.uclahealth.org{}'.format(url)
    
    def parse_westchestermedicalcenter(self, response):
        tables = response.xpath('//table[@class = "cpsys_Table"]')
        for table in tables:
            tds = table.xpath('.//tbody/tr/td')
            for td in tds:
                item = {}
                url = td.xpath('.//a/@href').extract_first()
                text = td.xpath('.//a//text()').extract_first()
                # faculty_name, faculty_degrees, faculty_rank = [None, None, None]  # Default values

                # if text:
                #     parts = text.split(', ')
                #     faculty_name  = parts[0]
                #     faculty_rank = parts[-1]
                    
                # item['Faculty'] = {
                #     'Hospital Name':'Westchester Medical Center',
                #     'Website URL':'https://www.uclahealth.org/',
                #     'Faculty Name': faculty_name,
                #     'Faculty Degrees': 'MD',
                #     'Faculty Training/Education History':','.join(td.xpath('.//span//text()').extract()),
                #     'Faculty Rank': faculty_rank if not 'MD' in faculty_rank else 'NA',
                # }
                
                # yield item
            
            # residents = response.xpath('//div[@id="cpsys_DynamicTab_d64c8276-3907-45fc-a37f-84f033d06d95_3"]/p')
            # for resident in residents:
            #     item = {}
            #     name = resident.xpath('.//strong/span/text()').extract_first()
            #     if  name:
            #         print(name)
            #     else:
            #         name = resident.xpath('.//strong/text()').extract_first()
            #         print(name)
                    
                    
                # if not name:
                #     name = resident.xpath('.//strong/span/span/text()').extract_first()
                    
                # if name:
                #     school_name = resident.xpath('.//span/span/text()').extract_first()
                    
                #     item['Resident'] = {
                #         'Name': name,
                #         "School Name": school_name,
                #         "post-graduate year": 'NA'
                #     }
                    
                #     yield item
                
                
                
    # def parse_faculty_details(self, response):
        # faculty_data = response.meta['faculty_data']
        
        # faculty_degrees = response.xpath('//div[@itemtype="educationalCredentialAwarded" and @itemprop="hasCredential"]/text()').extract()
        # faculty_degrees = ','.join(faculty_degrees)
        # fellowship_name = response.xpath('//div[@itemtype="educationalCredentialAwarded" and @itemprop="hasCredential"]/text()').extract()
        
        # faculty_data.update({'Fellow Fellowship Name': ','.join(fellowship_name)})
        
        # yield faculty_data
            
        
        
        
    def parse_residents(self, response):
        # Residents
        residents = response.xpath('//div[@class="space-y-8 order-2 lg:order-2 lg:row-span-1 lg:space-y-8 lg:mt-0"]/div')
        for resident in residents:
            
            # sentence = resident.xpath('h2/text()').extract_first().strip()
            sentence = resident.xpath('h2/text()').extract_first().strip() if resident.xpath('h2/text()').extract_first() is not None else None

            tags = resident.xpath('.//div[@class="space-y-6 group"]')
            
            for tag in tags:
                item = {}
                school_name = tag.xpath('.//div[@class="text-sm mt-2 line-clamp-2"]/text()').extract_first()
                name = tag.xpath('.//div[@class="font-serif font-normal text-lg md:text-xl text-almost-black leading-tight"]/div/text()').extract_first()
                item['Resident'] = {
                    'Name': name,
                    "School Name": school_name,
                    "post-graduate year": sentence
                }
                yield item
        
                
            
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
