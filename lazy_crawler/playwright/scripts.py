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
        sections = ['economics']

        for section in sections:
            
            res = await page.goto("https://www.bloomberg.com/lineup-next/api/paginate?id=story_list_2&page={}-v2&offset=0".format(section))
            # print(dir(res))
            print(res.all_headers)
            print(res.status)
            print(res.status_text)
            print(res.text())
            
        await browser.close()

def browse():
    asyncio.run(main())

if __name__ =='__main__':
    browse()
