import re
from playwright.sync_api import Page, expect
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://quotes.toscrape.com/')
        page.wait_for_timeout(10000)
        
        quotes = page.query_selector_all('//div[@class="quote"]')
        for quote in quotes:
            text = quote.query_selector('//span[@class="text"]').inner_text()
            author = quote.query_selector('//small[@class="author"]').inner_text()
            tags = quote.query_selector_all('//div[@class="tags"]/a[@class="tag"]')
            tag_lst = []
            for tag in tags:
                tag_lst.append(tag.inner_text())
            tag_str = ','.join(tag_lst)
            
            data = {
                "Author": author,
                "Text": text,
                "Tags": tag_str
            }
            print(data)
                
            
        
        browser.close()

if __name__ == '__main__':
    main()