import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent
from scrapy.shell import inspect_response
from scrapy import FormRequest
import datetime
import urllib.parse

# from lazy_crawler.crawler.pipelines import JsonWriterPipeline
class LazyCrawler(scrapy.Spider):

    name = "odresidents"
    #this is get url" https://odresidents.com/search_results

    allowed_domains = ['odresidents.com']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_IP': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'RETRY_TIMES': 2,
        'COOKIES_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 180,
        'COOKIES_DEBUG': True,
        # 'REDIRECT_ENABLED' : False,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': None
        }
    }
    
    def start_requests(self):
        url = "https://odresidents.com/search_results"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response): 
        print(response.text)
        # Define the path for the output file
        output_file_path = 'response_text.txt'

        # Save the response text to a file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        formdata = {
            "dc_id": "1",
            "header_type": "html",
            "request_type": "POST",  # This may need to be changed based on the correct request type
            "currentPage": "1",
            "dataType": "10",
            "queryString": '',
            "profId": '',
            "servId": 'null',
            "countryId": '',
            "stateId": '',
            "cityId": '',
            "levId": '',
            "profsPost": '{"new_filename":"search_results"}',
            "widget_name": "Add-On - Bootstrap Theme - Search - Lazy Loader",  # Ensure this is correct
        }   

        yield FormRequest.from_response(
            response,
            formdata=formdata,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            callback=self.parse_doctors_urls,
        )

    def parse_doctors_urls(self, response):

        # Extract the required data using XPath or CSS selectors
        doctors = response.xpath('//div[@class="row-fluid member_results level_6 search_result clearfix"]')
        
        for doctor in doctors:
            name = doctor.xpath('.//span[@class="h3 bold inline-block rmargin member-search-full-name"]/text()').get().strip()
            specialties = doctor.xpath('.//p[@class="small"]/b[contains(text(), "Specialties:")]/following-sibling::text()').get().strip()
            url = doctor.xpath('.//a[@class="center-block"]/@href').get()
            view_listing_url = doctor.xpath('.//a[contains(text(), "View Listing")]/@href').get()
            profile_url = doctor.xpath('.//a[@class="center-block"]/@href').get()
            # profile_url = self.clean_url(response.urljoin(profile_url))

            # Here you can yield the data or follow the URL to extract more details
            yield {
                'name': name,
                'specialties': specialties,
                'view_listing_url': view_listing_url,
                'url': url,
                'profile_url':profile_url
            }
            # # yield response.follow(url, self.parse_doctor_details)

    def clean_url(self, url):
        # Remove BOM character
        cleaned_url = url.replace('\ufeff', '')

        # Decode percent-encoded characters
        decoded_url = urllib.parse.unquote(cleaned_url)

        return decoded_url
    # def parse_doctor_details(self, response):
    #     # Extract additional details from the individual doctor's page
    #     email = response.xpath('//selector-for-email').get()
    #     phone = response.xpath('//selector-for-phone').get()
    #     school_graduated = response.xpath('//selector-for-school-graduated').get()
    #     year_graduated = response.xpath('//selector-for-year-graduated').get()

    #     # Print or save the additional details
    #     print(f"Email: {email}, Phone: {phone}, School Graduated: {school_graduated}, Year Graduated: {year_graduated}")

    #     # Yield the extracted details
    #     yield {
    #         'email': email,
    #         'phone': phone,
    #         'school_graduated': school_graduated,
    #         'year_graduated': year_graduated,
    #     }
        
        
            
    # start_urls = ['https://odresidents.com/wapi/widget']
    
    
    # def parse(self, response): 
    #     print("requesting the POST for readt for url........")  
    #     print(response)
    #     print(response.text)
    #     formdata = {
    #         "dc_id": "1",
    #         "header_type": "html",
    #         "request_type": "POST",
    #         "currentPage": "1",
    #         "dataType": "10",
    #         "queryString": '',
    #         "profId": '',
    #         "servId": 'null',
    #         "countryId": '',
    #         "stateId": '',
    #         "cityId": '',
    #         "levId": '',
    #         "profsPost": '{"new_filename":"search_results"}',
    #         "widget_name": "Add-On - Bootstrap Theme - Search - Lazy Loader",
    #     }   
    #     yield FormRequest.from_response(
    #         response,
    #         formdata=formdata,
    #         headers={
    #             "Content-Type":"application/x-www-form-urlencoded"
    #             },
    #         callback = self.parse_doctors_urls,
         
    #     )
    
    # def parse_doctors_urls(self, response):
    #     print(response.text)
        

            

 

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
