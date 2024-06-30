# from playwright.sync import sync_playwright

# def scrape_website(url):
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         page.goto(url)

#         # Replace this with your specific scraping logic.
#         title = page.title()
        
#         print(f'Title of the page: {title}')

#         browser.close()

from playwright.async_api import async_playwright
import asyncio

async def main():
 async with async_playwright() as p:
   browser = await p.chromium.launch(headless=False)
   page = await browser.new_page()
   await page.goto('https://www.mscdirect.com/browse/Abrasives?navid=2100008')
   await page.wait_for_timeout(1000)
   await browser.close()
   
if __name__ == '__main__':
    asyncio.run(main())

#     # Replace 'https://example.com' with the URL of the website you want to scrape.
#     scrape_website('https://www.mscdirect.com/browse/Abrasives?navid=2100008')
