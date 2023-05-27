import asyncio
from playwright.async_api import async_playwright
from lazy_crawler.lib.user_agent import get_user_agent
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            user_agent= get_user_agent('random'),
            # proxy={
            #     "server": "your_proxy_server",
            #     "username": "your_proxy_username",
            #     "password": "your_proxy_password",
            #     "bypass": "<-loopback>",  # Optional: bypass the proxy for localhost
            # },
        )
        page = await context.new_page()
        await page.goto("https://www.rent.com/")
        # Using XPath to select an element
        element = await page.wait_for_selector('//h1')
        # Interacting with the element
        text = await element.text_content()
        print(text)
        
        print(await page.title())
        
        await browser.close()

def browse():
    asyncio.run(main())

if __name__ =='__main__':
    browse()
