import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lazy_crawler.lib.user_agent import get_user_agent
import os.path
from datetime import datetime


def start_crawl():
    start_url = 'https://www.getcyberleads.com/directories/companies/A'
    options = Options()
    options.add_argument('--headless')  # use headless browser mode
    options.add_argument(f"user-agent:{get_user_agent('random')}")
    wait_time = 10
    timeout = 30

    driver = webdriver.Chrome(options=options)
    driver.get(start_url)
    parse_url(driver, wait_time, timeout)

    driver.quit()

def parse_url(driver, wait_time, timeout):
    while True:
        elements = driver.find_elements(By.XPATH, '//div[@class="company-post"]/div/ul/li/a')
        urls = [elem.get_attribute("href") for elem in elements]
        for url in urls:
            time.sleep(wait_time)  # wait for 10 seconds between requests
            try:
                options = Options()
                options.add_argument('--headless')  # use headless browser mode
                options.add_argument(f"user-agent:{get_user_agent('random')}")
                detail_driver = webdriver.Chrome(options=options)
                detail_driver = detail_driver.get(url)
                parse_details(detail_driver)
                detail_driver.quit()
            except Exception as e:
                print('Error loading details page:', url, e)

        # next_page = driver.find_elements(By.XPATH, '//div[@class="pagination"]/a[@class="next_page"]')
        # if next_page:
        #     next_page_url = next_page[0].get_attribute("href")
        #     try:
        #         options = Options()
        #         options.add_argument('--headless')  # use headless browser mode
        #         options.add_argument(f"user-agent:{get_user_agent('random')}")
        #         next_driver = webdriver.Chrome(options=options)
        #         next_driver.get(next_page_url)
        #         driver.quit()
        #         driver = next_driver
        #     except:
        #         print('Error loading next page:', next_page_url)
        #         break
        # else:
        #     break

    time.sleep(wait_time)  # wait for 10 seconds between requests

    try:
        if "Retry later" in driver.find_element(By.XPATH, '//body/pre').text:
            print("Received 'Retry later' message. Waiting for 30 seconds before retrying.")
            time.sleep(60)
            driver.get(driver.current_url)  # use the current URL instead of next_page_url
            parse_url(driver, wait_time, timeout)  # call the same function again to retry
    except NoSuchElementException:
        print("Could not find 'Retry later' message. Continuing with next page.", driver.current_url)


def parse_details(driver):
    print('coming data from......')
    # Get website URL
    keys = driver.find_elements(By.XPATH, '//p[@class="data-point-title"]/b')
    values = driver.find_elements(By.XPATH, '//p[@class="data-point-subtitle"]')
    print(keys)
    print(values)
    # for val in values:
    #     dict_val.append(val.text)
    # a_tag = driver.find_elements(By.XPATH,'//div[@class="column field"]/a')
    # for a in a_tag:
    #     dict_val.append(a.text)

    # details = dict(zip([key.text for key in keys], dict_val))
    # details['url'] = driver.current_url
    # print(details)

    # print('*' * 100)

    # print('Current URL:', driver.current_url)
    # # Check if the JSON file exists
    # if os.path.exists('scraped_data.json'):
    #     # Load the existing data from the JSON file
    #     with open('scraped_data.json', 'r') as f:
    #         existing_data = json.load(f)
    # else:
    #     # Create an empty list if the JSON file doesn't exist
    #     existing_data = []

    # # Append the new data to the existing data list
    # existing_data.append(details)

    # # Save the merged data as a JSON file with the current timestamp
    # file_name = f'scraped_data.json'
    # with open(file_name, 'w', encoding='utf-8') as f:
    #     json.dump(existing_data, f, indent=2, ensure_ascii=False)

    # print(details)

if __name__ == '__main__':
    start_crawl()
