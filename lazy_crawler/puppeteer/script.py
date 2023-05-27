# from typing import List
# from pyppeteer import launch
# import asyncio

# async def amain(url: str, headless: bool, proxy: str = None, cookies: List[dict] = None, useragent: str = None,
#                headers: dict = None, timeout: int = 0, close: bool = True):
#     options = {}
#     if timeout:
#         timeout = 0
#     if headless:
#         options['headless'] = True
#     else:
#         options['headless'] = False
#     if proxy:
#         proxy = proxy.split('//')[-1]
#         options['args'] = ['--proxy-server={}'.format(proxy.split('@')[1])]
#     browser = await launch(options)
#     page = await browser.newPage()
#     if headers:
#         await page.setExtraHTTPHeaders(headers)
#     if useragent:
#         await page.setUserAgent(useragent)
#     if proxy:
#         await page.authenticate({'username': proxy.split('@')[0].split(':')[0], 'password': proxy.split('@')[0].split(':')[1]})
#     if cookies:
#         await page.setCookie(*cookies)
#     print('visiting url', url)
#     try:
#         response = await page.goto(url, timeout=timeout)
#     except TimeoutError:
#         print('Timeout')

#     if not close:
#         return {'page': page, 'response': response}

#     await page.waitForNavigation()

#     cookies = await page.cookies()
#     content = await page.content()
#     response_headers = response.headers
#     await browser.close()
#     return {'response_headers': response_headers, 'cookies': cookies, 'content': content}

# def browse(url: str, headless: bool = True, proxy: str = None, cookies: list = None, useragent: str = None,
#            headers: dict = None, timeout: int = 0, close: bool = True):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         loop.run_until_complete(amain(url, headless, proxy, cookies, useragent, headers, timeout, close))
#     except KeyboardInterrupt:
#         pass

# if __name__ == '__main__':
#     url = 'https://example.com'
#     res = browse(url, headless=False)
#     print(res)