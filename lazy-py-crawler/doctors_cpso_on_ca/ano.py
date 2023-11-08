import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import re
from selenium.common.exceptions import NoSuchElementException
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def save_doctor_info_to_google_sheet(doctor_info):
    # Define the scope and load credentials from a JSON key file
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    
    # Authorize the client with the loaded credentials
    client = gspread.authorize(creds)
    
    # Open the Google Sheets document by its name
    sheet = client.open('JobScrapeData')
    
    # Select a specific worksheet (e.g., the first one)
    sheet_instance = sheet.get_worksheet(0)
    
    # Add the item data to the sheet
    values = list(doctor_info.values())
    # append body to spreadsheet
    sheet_instance.append_row(values)
            
    
    print("Doctor information added to the Google Sheet.")


# Create a WebDriver (you need to have a compatible driver installed, e.g., ChromeDriver)
options = Options()
options.add_argument('--headless')  # use headless browser mode
# options.add_argument(f"user-agent:{get_user_agent('random')}")
driver = webdriver.Chrome(options=options)

# Navigate to the URL
url = 'https://doctors.cpso.on.ca/?search=general'

driver.get(url)

# Find and click the button
button_id = "p_lt_ctl01_pageplaceholder_p_lt_ctl02_CPSO_AllDoctorsSearch_btnSubmit1"
submit_button = driver.find_element(By.ID, button_id)
submit_button.click()

try:
    # Find and click the "Next 5" link
    for page in range(1,100):
        if page == 5:
            break
        formatted_page = str(page).zfill(2)
        next_link = driver.find_element(By.ID,'p_lt_ctl01_pageplaceholder_p_lt_ctl03_CPSO_DoctorSearchResults_rptPages_ctl{}_lnbPage'.format(formatted_page))
        # next_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "p_lt_ctl01_pageplaceholder_p_lt_ctl03_CPSO_DoctorSearchResults_lnbNextGroup")))
        next_link.click()

        # You may want to add additional code to wait for the page to load after clicking
        # Use WebDriverWait to wait for an element to be visible on the page (you can customize the condition as needed)
        wait = WebDriverWait(driver, 2)  # Adjust the timeout as needed
        doctor_links = driver.find_elements(By.XPATH,'//div[@class="doctor-search-results"]/article/h3/a')
        urls = [link.get_attribute("href") for link in doctor_links]
        
        
        for url in urls:
            try:
                options = Options()
                options.add_argument('--headless')  # use headless browser mode
                # options.add_argument(f"user-agent:{get_user_agent('random')}")
                detail_driver = webdriver.Chrome(options=options)
                detail_driver.get(url)
                print('*'*100, 'scraping started with', url)
                try:
                    full_name = detail_driver.find_element(By.XPATH,'//h1[@id="docTitle"]').text
                    first_name, last_name = full_name.split(maxsplit=1) if ' ' in full_name else (full_name, '')

                    cpso_text_element = detail_driver.find_element(By.XPATH, '//div[@class="name_cpso_num"]/h3')
                    cpso_text = cpso_text_element.text
                    cpso = ''.join([c for c in cpso_text if c.isdigit()])

                    member_status_element = detail_driver.find_element(By.XPATH, '//div[@class="doctor-info"]/div[@class="columns medium-6 text-align--right"]/strong')
                    member_status_text = member_status_element.text
                    status = "Active Member" if "Active" in member_status_text else "Inactive Member"
                    
                    specialty = ''
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

                    summary_info_key_elements = detail_driver.find_elements(By.XPATH, '//section[@id="summary"]/div[@class="info"]/p/strong')
                    summary_info_key = [element.text for element in summary_info_key_elements]
                    
                    locations_details = detail_driver.find_element(By.XPATH, '//div[@class="location_details"]')
                    # Split the text content into a list using line breaks or any other suitable delimiter
                    data = locations_details.text.split('\n')  # Split by line breaks
                    independent_date = detail_driver.find_element(By.XPATH,'//div[@class="doctor-info"]/div[@class="columns medium-6 text-align--right"]').text.split(' ')
                except NoSuchElementException:
                    print('')

                # Create a dictionary to store the extracted information
                doctor_info = {}

                # Extract and add the information to the dictionary
                doctor_info['url'] = detail_driver.current_url
                doctor_info['first_name'] = first_name
                doctor_info['last_name'] = last_name
                doctor_info['cpso'] = cpso
                doctor_info['status'] = status
                doctor_info['specialty'] = ','.join(specialties_list)
                if len(summary_info_key) == len(filtered_list):
                    summary_dict = {}

                    for key, val in zip(summary_info_key, filtered_list):
                        key = key.strip()
                        val = val.strip()
                        doctor_info[key] = val
                    
                # Extract and add location information to the dictionary
                doctor_info["Postal Code"] = "",
                doctor_info['phone_number'] = next((re.search(r'\(\d{3}\)\s\d{3}-\d{4}', item).group() for item in data if re.search(r'\(\d{3}\)\s\d{3}-\d{4}', item)), None)
                doctor_info['fax_number'] = next((re.search(r'\(\d{3}\)\s\d{3}-\d{4}', item).group() for item in data if re.search(r'\(\d{3}\)\s\d{3}-\d{4}', item) and "Fax:" in data[data.index(item) - 1]), None)
                doctor_info['address'] = ','.join(data[2:3])
                
                doctor_info['Independent Practice as of'] = ' '.join(independent_date[-3:])
                doctor_info["Date of Entry"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,
                doctor_info = {key: str(value) for key, value in doctor_info.items()}
                save_doctor_info_to_google_sheet(doctor_info)
                
                detail_driver.quit()
            except Exception as e:
                print('Error loading details page:', url, e)

        
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Close the browser
driver.quit()