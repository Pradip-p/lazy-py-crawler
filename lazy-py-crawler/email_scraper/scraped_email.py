import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import csv


def remove_duplicate_emails(email_list):
    unique_emails = list(set(email_list))
    return unique_emails


def find_emails(text):
    """
    It will parse the given string and return a list of emails if found

    Example:
    >>find_emails('hello\n find me here\nemail@gmail.com')
    ['email@gmail.com']

    :param text: string
    :return: list
    """
    return re.findall(r"([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", text)


def start_request():
    # GET request
    urls = []

    if not os.path.isfile('urls.csv'):
        print("Error: 'urls.csv' file not found.")
        return

    with open('urls.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:
                url = row[0].strip()
                urls.append(url)

    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")  # Run in headless mode without opening a browser window

    for url in urls:
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)

            # Process the page and extract data
            emails = find_emails(driver.page_source)
            if emails:
                emails = remove_duplicate_emails(emails)
            data = {'URL': driver.current_url, 'Email': ','.join(emails)}
            write_data_to_csv("export.csv", data)
            print('Success: URL', driver.current_url)

        finally:
            driver.quit()


def write_data_to_csv(filename, data):
    col_name = list(data.keys())
    col_value = [data]

    with open(filename, 'a', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=col_name)
        if csvFile.tell() == 0:  # Check if the file is empty
            writer.writeheader()
        writer.writerow(data)


if __name__ == '__main__':
    print('Scraping started....')
    start_request()
