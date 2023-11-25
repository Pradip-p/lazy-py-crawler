import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent
from scrapy.shell import inspect_response
from scrapy import FormRequest
import datetime
import re

# from lazy_crawler.crawler.pipelines import JsonWriterPipeline
class LazyCrawler(scrapy.Spider):

    name = "doctors"
    
    allowed_domains = ['doctors.cpso.on.ca']
    
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
    

    start_urls = ['https://doctors.cpso.on.ca/?refine=true&search=general']
    
    event_target_val = -1
    
    page_number = 0
    
    def parse(self, response):   
        formdata = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS':'' ,
            '__VIEWSTATEGENERATOR': 'A5343185',
            'searchType': 'general',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$advancedState': 'closed',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$ConcernsState': 'closed',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtLastNameQuick': '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtCPSONumber': '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkActiveDoctors': 'on',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtCPSONumberGeneral': '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtLastName': '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$ddCity': '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtPostalCode': '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$grpGender':  '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$grpDocType': 'rdoDocTypeAll',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$ddHospitalCity': '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$ddHospitalName': '-1',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$ddLanguage': '08',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkPracticeRestrictions': 'on',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkPendingHearings': 'on',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkPastHearings': 'on',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkHospitalNotices': 'on',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkConcerns': 'on',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkNotices': 'on',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtExtraInfo': '',
            'p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$btnSubmit1': 'Submit',
        }   
        yield FormRequest.from_response(
            response,
            formdata=formdata,
            headers={
                "Content-Type":"application/x-www-form-urlencoded"
                },
            callback = self.parse_doctors_urls,
         
        )
    
    def parse_doctors_urls(self, response):
        # inspect_response(response, self)
        urls = response.xpath('//article[@class="doctor-search-results--result"]/h3/a/@href').extract()    
        print(urls)    
        # for url in urls:
        #     yield scrapy.Request(url, callback=self.doctor_details, dont_filter=True)
            
        # Extract the form data for the next page
        self.page_number += 1
        if self.page_number <= 3:
            # if self.event_target_val <= 5: 
                # print(self.event_target_val, self.page_number)
            formdata_next_page = {
                '__EVENTTARGET':'p$lt$ctl01$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$lnbNextGroup',
                # '__EVENTTARGET': 'p$lt$ctl01$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$rptPages$ctl0{}$lnbPage'.format(self.event_target_val),
                '__EVENTARGUMENT': '',
                '__VIEWSTATEGENERATOR': 'A5343185',
                'p$lt$ctl01$pageplaceholder$p$lt$ctl03$CPSO_DoctorSearchResults$hdnCurrentPage': str(self.page_number)
                
            }
            yield FormRequest.from_response(response,formdata=formdata_next_page,
                                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                                        callback=self.parse_doctors_urls,
                                    )
            

    def extract_postal_code(self,text):
        # pattern = re.compile(r'\b[A-Za-z]\d[A-Za-z]\s\d[A-Za-z]\d\b')#previous
        pattern = re.compile(r'\b[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d\b')
        postal_code_match = pattern.search(text)
        return postal_code_match.group(0) if postal_code_match else ''


    def doctor_details(self, response):    
        doctor_info = {}
        try:
            full_name = response.xpath('//h1[@id="docTitle"]/text()').get()
            last_name, first_name = full_name.split(maxsplit=1) if ' ' in full_name else (full_name, '')
            last_name = last_name.replace(',', '')

            cpso_text_element = response.xpath('//div[@class="name_cpso_num"]/h3/text()').get()
            cpso_text = cpso_text_element
            cpso = ''.join([c.strip() for c in cpso_text if c.isdigit()])

            member_status_element = response.xpath('//div[@class="doctor-info"]/div[@class="columns medium-6 text-align--right"]/strong/text()').get()
            status = "Active Member" if "Active" in member_status_element else "Inactive Member"

            independent_practice_as_of = response.xpath('(//div[@class="doctor-info"]/div[@class="columns medium-6 text-align--right"])[last()]/text()').get()
            independent_practice_as_of_text = independent_practice_as_of.split('as')[0]
            
            independent_parsed_date = ' '.join(independent_practice_as_of.split()[-3:])
            parsed_date = datetime.datetime.strptime(independent_parsed_date, "%d %b %Y")
            independent_parsed_date_formatted_date = parsed_date.strftime("%#m/%#d/%Y")

            tr_elements = response.xpath('//section[@id="specialties"]/table[@class="stack"]//tr')
            specialties_list = tr_elements.xpath('.//td[1]/text()').getall()

            summary_info_val_elements = response.xpath('//section[@id="summary"]/div[@class="info"]/p//text()').getall()
            filtered_list = [text.strip() for text in summary_info_val_elements if text.strip() != '']
            results = dict((filtered_list[i].strip(':'), filtered_list[i + 1].strip()) for i in range(0, len(filtered_list), 2)) if len(filtered_list) % 2 == 0 else None

            education = results.get('Education').split(',')
            education_year = education.pop()

            locations_details = response.xpath('//div[@class="location_details"]//text()').extract()
            # Split the text content into a list using line breaks or any other suitable delimiter
            data = [detail.replace('\xa0', '').strip() for detail in locations_details if detail.strip()]

            data = [detail.strip() for detail in locations_details if detail.strip()]
            city, postal_code, address, phone, fax = '', '', '', '', ''
            if len(data) == 1:
                address = ''.join(data)
            else:   
                for index, text in enumerate(data):
                    if text == 'Phone:' and index + 1 < len(data):
                        phone = data[index + 1].strip()
                        
                    elif text == 'Fax:' and index + 1 < len(data):
                        fax = data[index + 1].strip()  

            #         #i want to remove both index 
                
                provinces = ['ON','NL','SK','PE','NS','NB','QC','MB','AB','BC','YT','NT','NU']
                #remove Electoral District: from data
                if 'Electoral District:' in data:
                    data.pop()
                    data.pop()
                    
                if not phone and not fax:
                    address = ', '.join(data)
                    postal_code = self.extract_postal_code(address)
                    if postal_code:
                        #it's all about city
                        city_postal_code = data[-1]
                        for province in provinces:
                            if province in city_postal_code:
                                city_postal_code = city_postal_code.split(province)
                                if postal_code:
                                    city_postal_code.pop()
                                    city = ''.join(city_postal_code)
                        

                #posal code format: letter-number-letter-space-number-letter-number
                
                elif phone and fax:
                    address = ', '.join(data)
                    postal_code = self.extract_postal_code(address)
                    #it's all about city
                    city_postal_code = data[-1]
                    if postal_code:
                        for province in provinces:
                            if province in city_postal_code:
                                city_postal_code = city_postal_code.split(province)
                                if postal_code:
                                    city_postal_code.pop()
                                    city = ''.join(city_postal_code)

     
                elif phone or fax:
                    address = ', '.join(data)
                    postal_code = self.extract_postal_code(address)
                    #it's all about city
                    city_postal_code = data[-1]
                    if postal_code:
                        for province in provinces:
                            if province in city_postal_code:
                                city_postal_code = city_postal_code.split(province)
                                if postal_code:
                                    city_postal_code.pop()
                                    city = ''.join(city_postal_code)
                                    
        except Exception as e:
            self.log(f"Error: {e}")

        # # Create a dictionary to store the extracted information
        # doctor_info['Link'] = response.url
        # doctor_info['First Name'] = first_name.strip()
        # doctor_info['Last Name'] = last_name.strip()
        # doctor_info['CPSO'] = cpso.strip()
        # doctor_info['Member Status'] = status.strip()
        # doctor_info['Current or Past CPSO Registration Class'] = independent_practice_as_of_text.strip()
        # doctor_info['Independent Practice as of'] = independent_parsed_date_formatted_date
        # doctor_info['Former Name'] = results.get('Former Name')
        # doctor_info['Gender'] = results.get('Gender')
        # doctor_info['Education'] = ' '.join(education)
        # doctor_info['Graduating Year'] = education_year
        # doctor_info['Specialty'] = ','.join(specialties_list)
        # Add the rest of the fields to doctor_info
        doctor_info['City'] =  city.strip()
        doctor_info['Address'] = address.strip()
        
        # Extract and add location information to the dictionary
        doctor_info["Postal Code"] = postal_code
        doctor_info['Phone'] = phone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('Ext', 'ext')

        doctor_info['Fax'] = fax.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        doctor_info["Date of Entry"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doctor_info['Notes'] = ''
        yield doctor_info


# response.xpath('//article[@class="doctor-search-results--result"]/h3/a/@href').extract()
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
