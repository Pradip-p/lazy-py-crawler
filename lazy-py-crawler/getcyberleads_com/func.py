import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
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
    driver = webdriver.Chrome(options=options)
    wait_time = 10
    timeout = 30

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
                driver.get(url)
            except:
                print('Error loading details page:', url)
                continue
            parse_details(driver)

        next_page = driver.find_elements(By.XPATH, '//div[@class="pagination"]/a[@class="next_page"]')
        if next_page:
            next_page_url = next_page[0].get_attribute("href")
            driver.get(next_page_url)
        else:
            break

    time.sleep(wait_time)  # wait for 10 seconds between requests

    try:
        if "Retry later" in driver.find_element(By.XPATH, '//body/pre').text:
            print("Received 'Retry later' message. Waiting for 30 seconds before retrying.")
            time.sleep(60)
            driver.get(driver.current_url)  # use the current URL instead of next_page_url
            parse_url(driver, wait_time, timeout)  # call the same function again to retry
    except NoSuchElementException:
        print("Could not find 'Retry later' message. Continuing with next page.", driver.current_url)

# def parse_url(driver, wait_time, timeout):
#     elements = driver.find_elements(By.XPATH, '//div[@class="company-post"]/div/ul/li/a')
#     urls = [elem.get_attribute("href") for elem in elements]
#     for url in urls:
#         time.sleep(wait_time)  # wait for 10 seconds between requests
#         try:
#             driver.get(url)
#         except:
#             print('Error loading details page:', url)
#             continue
#         parse_details(driver)

#     next_page = driver.find_elements(By.XPATH, '//div[@class="pagination"]/a[@class="next_page"]')
#     if next_page:
#         next_page_url = next_page[0].get_attribute("href")
        
#         driver.get(next_page_url)
#         parse_url(driver, wait_time, timeout)
#     else:
#         elements = driver.find_elements(By.XPATH, '//div[@class="company-post"]/div/ul/li/a')
#         urls = [elem.get_attribute("href") for elem in elements]
#         for url in urls:
#             time.sleep(wait_time)  # wait for 10 seconds between requests
#             print('detail url is', url)
#             try:
#                 driver.get(url)
#             except:
#                 print('Error loading details page:', url)
#                 continue
#             parse_details(driver)

#     time.sleep(wait_time)  # wait for 10 seconds between requests

#     try:
#         if "Retry later" in driver.find_element(By.XPATH, '//body/pre').text:
#             print("Received 'Retry later' message. Waiting for 30 seconds before retrying.")
#             time.sleep(60)
#             print('curent url is',  driver.current_url)
#             driver.get(driver.current_url)  # use the current URL instead of next_page_url
#             parse_url(driver, wait_time, timeout)  # call the same function again to retry
#     except NoSuchElementException:
#         print("Could not find 'Retry later' message. Continuing with next page.", driver.current_url)


def parse_details(driver):
    # Get website URL
    dict_val = []
    keys = driver.find_elements(By.XPATH,'//p[@class="data-point-title"]/b')
    values = driver.find_elements(By.XPATH,'//p[@class="data-point-subtitle"]')
    for val in values:
        dict_val.append(val.text)
    details = dict(zip([key.text for key in keys], dict_val))
    print('*'*100)
    print('Current URL:', driver.current_url)
    print(details)


if __name__ == '__main__':
    start_crawl()
