import csv
import time
from playwright.sync_api import sync_playwright
import random
from lazy_crawler.lib.user_agent import get_user_agent
class LazyCrawler:
    def __init__(self):
        self.proxy_file = "proxy_list.csv"  # Replace with the actual path to your CSV file

    def write_data_to_csv(self, filename, data):
        col_name = list(data.keys())
        col_value = [data]

        with open(filename, 'a', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=col_name)
            if csvFile.tell() == 0:  # Check if the file is empty
                writer.writeheader()
            writer.writerow(data)
            
    def read_proxy_list_from_csv(self, filename):
        proxy_list = []
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    proxy_parts = row[0].split(':')
                    proxy = {
                        'host': proxy_parts[0],
                        'port': proxy_parts[1],
                        'user': proxy_parts[2],
                        'pass': proxy_parts[3]
                    }
                    proxy_list.append(proxy)
        except FileNotFoundError:
            print(f"CSV file '{filename}' not found.")
        except Exception as e:
            print(f"Error reading proxy list from CSV: {e}")

        return proxy_list

    def start_crawl(self):
        with sync_playwright() as playwright:
            proxy_list = self.read_proxy_list_from_csv(self.proxy_file)
            if not proxy_list:
                print('No proxies found in the CSV file.')
                return

            for page_num in range(1, 3):
                url = f"https://www.yellowpages.com.au/search/listings?clue=massage&locationClue=All+States&pageNumber={page_num}"
                
                # Choose a random proxy
                proxy = random.choice(proxy_list)
                
                print(proxy)

                proxy_url = f"http://{proxy['host']}:{proxy['port']}"
                browser = playwright.chromium.launch(proxy={
                    "server": proxy_url,
                    "username": proxy['user'],
                    "password": proxy['pass']
                }, headless=True)

                context = browser.new_context(
                    user_agent=get_user_agent('random'),
                )
                page = context.new_page()                
                print('*' * 10, url)
                page.goto(url, timeout=600000)
                time.sleep(20)

                # main_div = page.query_selector_all('.Box__Div-sc-dws99b-0.iOfhmk.MuiPaper-root.MuiCard-root.PaidListing.MuiPaper-elevation1.MuiPaper-rounded')
                # for res in main_div:
                #     name_elem = res.query_selector('h3.MuiTypography-root.jss288.MuiTypography-h3.MuiTypography-displayBlock')
                #     name = name_elem.inner_text() if name_elem else ''
                #     addr_elem = res.query_selector('p.MuiTypography-root.jss289.MuiTypography-body2.MuiTypography-colorTextSecondary')
                #     addr = addr_elem.inner_text() if addr_elem else ''
                #     ph_num_elem = res.query_selector('button.MuiButtonBase-root.MuiButton-root.MuiButton-text.ButtonPhone.MuiButton-textPrimary.MuiButton-fullWidth span.MuiButton-label')
                #     ph_num = ph_num_elem.inner_text() if ph_num_elem else ''
                #     short_desc_elem = res.query_selector('p.MuiTypography-root.jss302.MuiTypography-subtitle2')
                #     short_desc = short_desc_elem.inner_text() if short_desc_elem else ''
                #     desc = res.query_selector('div.Box__Div-sc-dws99b-0.iswkLA') 
                #     desc = desc.inner_text() if desc else ''
                # main_div = page.locator('//div[contains(@class, "Box__Div-sc-dws99b-0") and contains(@class, "iOfhmk") and contains(@class, "MuiPaper-root") and contains(@class, "MuiCard-root") and contains(@class, "PaidListing") and contains(@class, "MuiPaper-elevation1") and contains(@class, "MuiPaper-rounded")]')
                main_div = page.locator('//div[@class="Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded"]')
                # for res in main_div:
                #     name_elem = res.query_selector('//h3[@class="MuiTypography-root jss288 MuiTypography-h3 MuiTypography-displayBlock"]/text()')
                    # name = name_elem.inner_text() if name_elem else ''
                    # addr_elem = res.query_selector('//p[@class="MuiTypography-root jss289 MuiTypography-body2 MuiTypography-colorTextSecondary"]')
                    # addr = addr_elem.inner_text() if addr_elem else ''
                    # ph_num_elem = res.query_selector('//button[@class="MuiButtonBase-root MuiButton-root MuiButton-text ButtonPhone MuiButton-textPrimary MuiButton-fullWidth"]/span[@class="MuiButton-label"]')
                    # ph_num = ph_num_elem.inner_text() if ph_num_elem else ''
                    # short_desc_elem = res.query_selector('//p[@class="MuiTypography-root jss302 MuiTypography-subtitle2"]')
                    # short_desc = short_desc_elem.inner_text() if short_desc_elem else ''
                    # desc = res.query_selector('//div[@class="Box__Div-sc-dws99b-0 iswkLA"]') 
                    # desc = desc.inner_text() if desc else ''

                    # data = {
                    #     "Name": name,
                    #     "Address": addr,
                    #     "Phone Number": ph_num,
                    #     "Short Desc": short_desc,
                    #     "Description": desc
                    # }
                    # print(data)
                    # self.write_data_to_csv("output.csv", data)
                print(main_div)
                context.close()
                browser.close()
                time.sleep(60)

if __name__ == '__main__':
    crawler = LazyCrawler()
    crawler.start_crawl()
