import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.common.exceptions import NoSuchElementException
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def create_google_sheets_client(creds_json_file):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_file, scope)
    client = gspread.authorize(creds)
    return client

def open_google_sheet(client, sheet_name, worksheet_index=1):
    sheet = client.open(sheet_name)
    sheet_instance = sheet.get_worksheet(worksheet_index)
    return sheet_instance

def save_data_to_google_sheet(sheet_instance, data):

    values = list(data.values())

    # append body to spreadsheet
    sheet_instance.append_row(values)
    
    print("Doctor information added to the Google Sheet.")

def scrape_doctor_info(detail_driver, url, sheet_instance):
    # Your scraping logic here
    try:
        options = Options()
        options.add_argument('--headless')  # use headless browser mode
        detail_driver = webdriver.Chrome(options=options)
        detail_driver.get(url)
        print('*'*100, 'scraping started with', url)
        try:
            full_name = detail_driver.find_element(By.XPATH,'//h1[@id="docTitle"]').text
            last_name, first_name = full_name.split(maxsplit=1) if ' ' in full_name else (full_name, '')
            last_name = last_name.replace(',', '')

            cpso_text_element = detail_driver.find_element(By.XPATH, '//div[@class="name_cpso_num"]/h3')
            cpso_text = cpso_text_element.text
            cpso = ''.join([c for c in cpso_text if c.isdigit()])

            member_status_element = detail_driver.find_element(By.XPATH, '//div[@class="doctor-info"]/div[@class="columns medium-6 text-align--right"]/strong')
            member_status_text = member_status_element.text
            status = "Active Member" if "Active" in member_status_text else "Inactive Member"
            
            tr_elements = detail_driver.find_elements(By.XPATH, '//section[@id="specialties"]/table[@class="stack"]/tbody//tr')
            # Initialize a list to store the first <td> text from each <tr>
            specialties_list = []
            # Extract the text from the first <td> element in each <tr>
            for tr in tr_elements:
                td_elements = tr.find_elements(By.XPATH, './/td[1]')
                if td_elements:
                    first_td_text = td_elements[0].text
                    specialties_list.append(first_td_text)

            summary_info_val_elements = detail_driver.find_elements(By.XPATH, '//section[@id="summary"]/div[@class="info"]/p')
            
            summary_info_val = [element.text for element in summary_info_val_elements]
            filtered_list = [text.strip() for text in summary_info_val if text.strip() != '']
            results = {key.strip(): value.strip() for key, value in (item.split(':') for item in filtered_list)}

            locations_details = detail_driver.find_element(By.XPATH, '//div[@class="location_details"]')
            # Split the text content into a list using line breaks or any other suitable delimiter
            data = locations_details.text.split('\n')  # Split by line breaks
            if len(data) == 1:
                pass
            else:
                fax_number = next((re.search(r'Fax: [\d() -]+', item).group(0) for item in data if re.search(r'Fax: [\d() -]+', item)), None)
                if fax_number:
                    fax = fax_number.replace('Fax: ', '')
                else:
                    fax = ''
                
                phone_number_match = re.search(r'Phone: [\d() -]+', str(data))
                
                if phone_number_match:
                    phone = phone_number_match.group(0).replace('Phone: ', '')
                else:
                    phone = ''

                city = ''
                postal_code = ''
                address = ''
                if not phone and not fax:
                    address = ' '.join(data)
                    city_code = data[-1].split()
                    city = city_code[0]
                    postal_code = re.search(r'\b[A-Z0-9]+\b', str(city_code[2:4])).group() if re.search(r'\b[A-Z0-9]+\b', str(city_code[2:4])) else None

                
                elif phone and fax:
                    data.pop()
                    data.pop()
                    city_postal_code = data[-1]
                    address = ' '.join(data)
                    city_and_postal_code = city_postal_code.split()
                    city = city_and_postal_code[0]
                    postal_code = city_and_postal_code[-2:]
                    
                elif phone or fax:
                    data.pop()
                    city_postal_code = data[-1]
                    address = ' '.join(data)
                    city_and_postal_code = city_postal_code.split()
                    city = city_and_postal_code[0]
                    postal_code = city_and_postal_code[-2:]
                
            independent_date = detail_driver.find_element(By.XPATH,'//div[@class="doctor-info"]/div[@class="columns medium-6 text-align--right"]').text.split(' ')
        except NoSuchElementException:
            print('')
        
        # Create a dictionary to store the extracted information
        doctor_info = {}

        # Extract and add the information to the dictionary
        doctor_info['Link'] = detail_driver.current_url
        doctor_info['First Name'] = first_name
        doctor_info['Last Name'] = last_name
        doctor_info['CPSO'] = cpso
        doctor_info['Member Status'] = status
        doctor_info['Current or Past CPSO Registration Class'] = ''
        doctor_info['Independent Practice as of'] = ' '.join(independent_date[-3:])
        doctor_info['Former Name'] = results.get('Former Name')  
        doctor_info['Gender'] = results.get('Gender')  
        doctor_info['Education'] = results.get('Education')
        doctor_info['Graduating Year'] = re.search(r'\d{4}', results.get('Education')).group() if re.search(r'\d{4}', results.get('Education')).group() else ''
        doctor_info['Specialty'] = ','.join(specialties_list)
        doctor_info['City'] =  city if city else '' #
        doctor_info['Address'] = address
        
        # Extract and add location information to the dictionary
        doctor_info["Postal Code"] =  ' '.join(postal_code) if postal_code else '' 
        doctor_info['Phone'] = phone
        doctor_info['Fax'] = fax
        doctor_info["Date of Entry"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doctor_info = {key: str(value) for key, value in doctor_info.items()}
        save_data_to_google_sheet(sheet_instance, doctor_info)
        detail_driver.quit()
        
    except Exception as e:
        print('Error loading details page:', url, e)


def main():
    # Create a WebDriver (you need to have a compatible driver installed, e.g., ChromeDriver)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Google Sheets configuration
    creds_json_file = 'creds.json'
    sheet_name = 'CPSO'
    worksheet_index = 1

    # Google Sheets client and worksheet
    client = create_google_sheets_client(creds_json_file)
    sheet_instance = open_google_sheet(client, sheet_name, worksheet_index)

    # Navigate to the URL
    url = 'https://doctors.cpso.on.ca/?search=general'
    driver.get(url)

    # Find and click the button
    button_id = "p_lt_ctl01_pageplaceholder_p_lt_ctl02_CPSO_AllDoctorsSearch_btnSubmit1"
    submit_button = driver.find_element(By.ID, button_id)
    submit_button.click()

    try:
        # Find and click the "Next 5" link
        for page in range(1, 100):
            if page == 5:
                break
            formatted_page = str(page).zfill(2)
            next_link_id = f'p_lt_ctl01_pageplaceholder_p_lt_ctl03_CPSO_DoctorSearchResults_rptPages_ctl{formatted_page}_lnbPage'
            next_link = driver.find_element(By.ID, next_link_id)
            next_link.click()

            # You may want to add additional code to wait for the page to load after clicking
            # Use WebDriverWait to wait for an element to be visible on the page (you can customize the condition as needed)
            wait = WebDriverWait(driver, 2)  # Adjust the timeout as needed
            doctor_links = driver.find_elements(By.XPATH, '//div[@class="doctor-search-results"]/article/h3/a')
            urls = [link.get_attribute("href") for link in doctor_links]

            for url in urls:
                scrape_doctor_info(driver, url, sheet_instance)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
