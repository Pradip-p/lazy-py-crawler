import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LazyCrawler:
    def __init__(self):
        self.url = "https://odresidents.com/search_results"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-popup-blocking")  # Ensure popups are not blocked
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 20)  # Increased wait time to 20 seconds
        self.urls = []

    def start_requests(self):
        try:
            page_number = 1

            while True:
                print(f"Fetching URLs from page {page_number}...")
                # Wait until all "View Listing" buttons are present
                view_listing_buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "btn btn-success btn-block")]')))

                # Collect URLs for current page
                for button in view_listing_buttons:
                    try:
                        # Get the URL of the "View Listing" button
                        url = button.get_attribute("href")
                        self.urls.append(url)
                    except Exception as e:
                        print(f"An error occurred while processing doctor profile: {e}")

                # Check if there's a "Load More" button for the next page
                load_more_button = self.driver.find_element(By.XPATH, '//div[@id="btnToLoadMorePost"]')
                if "disabled" in load_more_button.get_attribute("class"):
                    print(f"No more pages to load. Exiting...")
                    break

                # Scroll the "Load More" button into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                time.sleep(2)  # Adjust sleep time as needed for the button to be clickable

                # Click the "Load More" button using JavaScript
                try:
                    self.driver.execute_script("arguments[0].click();", load_more_button)
                    page_number += 1
                    time.sleep(5)  # Adjust sleep time as needed after loading the next page
                except Exception as e:
                    print(f"Failed to click 'Load More' button: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def save_urls_to_json(self):
        with open('urls.json', 'w') as f:
            json.dump(self.urls, f, indent=4)
        print("URLs saved to 'urls.json'")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    crawler = LazyCrawler()
    try:
        crawler.start_requests()
        crawler.save_urls_to_json()
    finally:
        crawler.close()
