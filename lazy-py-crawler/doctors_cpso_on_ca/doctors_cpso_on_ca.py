import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent
import ipdb
import re
import datetime


class LazyCrawler(scrapy.Spider):

    name = "doctors"
    
    allowed_domains = ['doctors.cpso.on.ca']
    
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
            'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': None
        }
    }
    
    headers = {
        "Host": "doctors.cpso.on.ca",
        'User-Agent': get_user_agent('random'),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "2439",
        "Origin": "https://doctors.cpso.on.ca",
        "Connection": "keep-alive",
        "Cookie": "CMSPreferredCulture=en-CA; CMSCsrfCookie=mLUnpeXTnvLtBsuesykRaSqvMsgxPxJQ50IZywkw; ASP.NET_SessionId=qcrtee14k1hpqsq4ysvgxtxe; _ga_04KQWSX9S4=GS1.1.1698910795.1.1.1698910869.0.0.0; _ga=GA1.1.1065468384.1698910796; cusid=1698910796547; cuvon=1698910841317; cusid=1698910796547; cuvid=c5dc450e62f74057a39f3af80d91a54b"
        
    }
    formdata = {
            "__CMSCsrfToken":"kYk197Q8HhWfqqaUtcyt8Rv9d588b4jh8bstXhklwjvxIkwWOQOsWbsTArqPbXY4SUE8Nn9fcgVGhfjgEoFSB0Jnbhb3e7e0O6FgnnFajhA=",
            "__EVENTTARGET":	"p$lt$ctl01$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$lnbNextGroup",
            "__EVENTARGUMENT"	:"",
            "__VIEWSTATE"	: "g8IIMCAyz9hD0CF0A0UsfvUI9bSyxRCO9jokLqP+/a6S7yKgS5iJmumov4fVFvRGUBgq4OkV5wyorlWqr4YCbWMcYFR9SJkjNT/T9UftGKEBoZ4WZwNC03i6Bj+hIswdId2FVur+OXLvybLYlK+POy9k6OD/jDydb7E4IIEPlS2Lfw25EmJ8RfOl4x9tPndi7b9ZpW6QynwhxHfVJi9UQcngYDb9lbcqP8vSEXi0Y5PP9lGBb1dZhxKw2JGeadUs5zvxb8pJqjTqgebV+o3XcnRM5Kx8m271QUSaaeVEXqyjU/t8CGTHJR5vSYJIo2d+sIHkSUtjjP4pEc9+DVufWScYzMVBSH+C0R9pzbEkTmD050GebwJoDnIgDjQPRNYcCRTaT9phyWvouoPLjnMHhgCh0sob4P8lx9Dq7OU9heD3LhEHh90GaYkywkEXC4bRiycRaeUAPq0b+xuoAqTH8f+KZfLEU6oHyxv8kgf19J0vOteANIlIDsgjoHk5Uxs…KwMdVSwWFX0J9bRB0tmG2bA66knLmhV+QJhswIsathe29sPeuWO2E7CqAHngdjoCfGiMV1UPLzrGcUxbozg8hCvTh/K7f2aIbJ1/qn6hkGRBwz/Ahp9gB55USD9wNxL1lvEpynPaWlIKN0HxjmxyecEIB5/YZ4zfWk3g9qziJw7Va7YKvzlzgkSF2XDpWuNMmwXKxcIelPG2eEs5jt0AcOFuF9YQJO26eqxn7DkeGJ46Hk8a8G67iqEiWUxAduTlT1NkTjwGo9hwL4Fq+rEsIjCurdvP2g9Kb5SoaMCxZJ+ABSJ6f9421qCKyGajwVDjm2HVhy2yrLQSoUDDbmVoMBTbBXE9LLrLWkYAmlzFWFWiYcznIV9apfJU3tzmYHiZasJMH0DalMx5OvJM5D8K4hMFNBFghwHM99DcBXMlSMMaETkeobp2tl80t8lW5clfHwuVa4xKzm9P4iu6+I2giZZhRqXZHXPRWpRCYjV1w28hvbl1gBBLLx6MaqaLg=",
            "lng":	"en-CA",
            "__VIEWSTATEGENERATOR"	:"A5343185",
            "p$lt$ctl01$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$hdnCurrentPage"	:"1"
        }
    
    def start_requests(self):

        # url = 'https://doctors.cpso.on.ca//Doctor-Search-Results'
        # url = 'https://doctors.cpso.on.ca//Doctor-Search-Results?type=name&term='
        url = 'https://doctors.cpso.on.ca/Doctor-Search-Results?type=name&term='
        yield scrapy.FormRequest(url, callback=self.parse_doctor_urls,
                            method = 'POST',
                            headers= self.headers, 
                            formdata=self.formdata,
                            dont_filter=True)

    def parse_doctor_urls(self, response):
        doctors_urls = response.xpath('//div[@class="doctor-search-results"]/article/h3/a/@href').extract()
        for url in doctors_urls:
            yield scrapy.Request(url, callback=self.parse_doctor_details,
                            headers= self.headers, 
                            dont_filter=True)
        
    def parse_doctor_details(self, response):
        full_name = response.xpath('//h1[@id="docTitle"]/text()').extract_first()
        first_name, last_name = full_name.split(maxsplit=1) if ' ' in full_name else (full_name, '')
        cpso_text = response.xpath('//div[@class="name_cpso_num"]/h3/text()').extract_first()
        cpso = ''.join([c for c in cpso_text if c.isdigit()])
        member_status_text = response.xpath('//div[@class="doctor-info"]/div[@class="columns medium-6 text-align--right"]/strong/text()').extract_first()
        status = "Active Member" if "Active" in member_status_text else "Inactive Member"
        specialty = response.xpath('//section[@id="specialties"]/table[@class="stack"]/tr/td/text()').extract_first()
        # Assuming you have a response object containing the HTML content
        summary_info_val = response.xpath('//section[@id="summary"]/div[@class="info"]/p/text()').extract()
        filtered_list = [text.strip() for text in summary_info_val if text.strip() != '']

        summary_info_key = response.xpath('//section[@id="summary"]/div[@class="info"]/p/strong/text()').extract()
        
        if len(summary_info_key) == len(filtered_list):
            summary_dict = {}

            for key, val in zip(summary_info_key, filtered_list):
                key = key.strip()
                val = val.strip()
                summary_dict[key] = val
        locations_details = response.xpath('//div[@class="location_details"]//text()').extract()

        data = [text.strip() for text in locations_details if text.strip() != '']
        print(data)
        phone_number = next((re.search(r'\(\d{3}\)\s\d{3}-\d{4}', item).group() for item in data if re.search(r'\(\d{3}\)\s\d{3}-\d{4}', item)), None)
        fax_number = next((re.search(r'\(\d{3}\)\s\d{3}-\d{4}', item).group() for item in data if re.search(r'\(\d{3}\)\s\d{3}-\d{4}', item) and "Fax:" in data[data.index(item) - 1]), None)
        address = ','.join(data[2:3])

        
        yield{
            "Link": response.url,
            "Last Name": last_name,
            "First Name": first_name,
            "CPSO": cpso,
            "Member Status":status,
            "Current or Past CPSO Registration Class": "",
            "Former Name": summary_dict.get('Former Name:'),
            "Gender": summary_dict.get('Gender:') if summary_dict.get('Gender:') else '',
            "Education":summary_dict.get('Education:') if summary_dict.get('Education:') else '',
            "Specialty":specialty,
            "City": "",
            "Address": address if address else '' ,
            "Postal Code":"",
            "Phone": phone_number if phone_number else '' ,
            "Fax": fax_number if fax_number else '',
            "Date of Entry": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,
            "Notes":""
        }
        
        # # Save the content of the current page as a text file
        # with open(f'response.txt', 'w', encoding='utf-8') as file:
        #     file.write(response.text)
                    
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
