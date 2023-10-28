# from seleniumwire import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# import base64

# proxy_server = 'p.webshare.io:80'
# proxy_username = "gkoffhkj-rotate"
# proxy_password = "9qsx6zrpagq6"


# # Define the headers data
# headers_data = {
#     "Host": "www.mscdirect.com",
#     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Connection": "keep-alive",
#     "Cookie": "visid_incap_2587862=9VEK7LwZTwWtBKDXoUgsJxUaO2UAAAAAQUIPAAAAAAAewHeeMuQp/yVQCcfMYhoX; AMCV_99591C8B53306B560A490D4D%40AdobeOrg=-1124106680%7CMCIDTS%7C19658%7CMCMID%7C79541320284579145004472388857864065288%7CMCAAMLH-1698982401%7C3%7CMCAAMB-1698982401%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1698384801s%7CNONE%7CMCSYNCSOP%7C411-19665%7CvVersion%7C5.2.0; mbox=PC#034559efac364e7a87f2629adb4005d3.38_0#1761627278|session#2b56cefdf66a4a739c53b902cd4d8f48#1698384338; WCDE_XREFCONTACTNUMBERGUEST=; utag_main=v_id:018b6ede24f200592d287ccefd7c0504e002a01100bd0$_sn:3$_se:6$_ss:0$_st:1698384279797$vapi_domain:mscdirect.com$ses_id:1698382380286%3Bexp-session$_pn:2%3Bexp-session; cj_channel=Direct_Navigation; s_vnum=1698776100112%26vn%3D3; cjConsent=MHxOfDB8Tnww; cjUser=7d85b130-655f-4fff-9591-261b24502abf; _br_uid_2=uid%3D7713763678562%3Av%3D12.0%3Ats%3D1698372142830%3Ahc%3D12; _blka_ruab=158; _gcl_au=1.1.1076560165.1698372145; reese84=3:42avnkiIbAjYJ/Muo1hHCA==:v/PHYWXZLOWxc7r8MoqDGOnBeVAtYC8A8FfoTx7N+/dmjl6UzM4qGqtFxIeA74oBrt8qLYw/bnz5ViJJpi1Yo3GJTJErxFAbTIZTOV5M2Ehpc+0g+SxMFmpgAdeGA1wtUOxnSqKaNbCwHj/1q+kXexG0sDIdNxOAcQgCdpXnbtz46NXGlgvwD+KcrvJkPu34zRuZcSUFQ53hn1W5H8l2GCyRg37sDm3ak3oVCVEJj6FtNT0V6wC5eE3FHoQqP6amPT/nY9WnwtgmnzY4PrXmwZ8R1JUWvJGS4sMG44gVA/E6tyt4u7g7hFAPMCBMg6ADh/W2I6WSjE/bjsAriOxdFDTw/vHH3LrhOT05T0wTUIP0sCOOA792HXE/x2je2LKsN/fjxAtMebb8xYFATmgGF/vHFiR206T0HfFKRciU4mgMeCmYB0NEao7sgoKPUQ4ABPC8Tf+LZQZHhlcAIVDRIw==:ZSGusuoCWUQJOvIrkTEwGSsvoWgLrVDoK8A1SrkzSD0=; _ga_KG0FCGTKBP=GS1.1.1698382360.3.1.1698382480.55.0.0; _ga=GA1.2.471579495.1698372145; _ga_CM5B4R0KX7=GS1.1.1698382360.3.1.1698382481.54.0.0; fs_uid=#10Q6K5#838e81ab-bb27-4d6a-91d5-91c701b1938d:1ff7a8ff-709e-4edf-ab5b-c0e032adf2af:1698382359162::3#/1729908142; _fbp=fb.1.1698372147589.232462260; sa-user-id=s%253A0-f67f2167-d5d1-58a2-73df-50100afc6ac0.ZoThbIDj1%252F7wOYdJ2pUHCVDWiOr7TIKzHyMtTHSCfYA; sa-user-id-v2=s%253A9n8hZ9XRWKJz31AQCvxqwBsiZHI.PDFghBIJihSZgIBCq8DQk3FOm4i8t67qn8ktxE5ZUuE; sa-user-id-v3=s%253AAQAKIN9eG0P9Xr84GpaSUsjYlrfxvrO3SjCeuFVjFahUToyVEHAYBCC0tOypBjABOgTWuvtmQgQ2SjBM.DX7S4HSqEQPxF%252FQOywL%252FAjLVCsFRIDwA0U0BP%252F%252FIkg4; _clck=2c7g4m|2|fg7|0|1395; _gid=GA1.2.1203062566.1698372150; _clsk=tkdrde|1698382489868|2|0|t.clarity.ms/collect; gig_bootstrap_4_R0HZVTou0ajlxJ_Xco0l_w=identity_ver4; pn=15; incap_ses_50_2587862=QyCkKeqB9yK7JlNq/aKxABVCO2UAAAAA8SZyJ0EuYmvO12dQk83eXg==; nlbi_2587862_2147483392=MFXeFSo/TmyCzOv0Z8kABQAAAAANqyUT3VUY9vQEGhJ47yMY; dtCookie=v_4_srv_26_sn_C094265D02DC3630881F45D24C539C48_perc_100000_ol_0_mul_1_app-3A4933650768ea878a_1_rcs-3Acss_0; nlbi_2587862=I8ivJh4gAA0LgtWuZ8kABQAAAAByqSLQqZtcq0mBTiVw/Sg7; Mscdirect=3876067756.33588.0000; rxVisitor=1698377594105VPHPTS7F14VMJGT4GLVDR4EENKJL5RE1; dtPC=26$382476272_437h-vCPHVMGRIUGHVOFGRAMQLGDKDEKLWBALN-0e0; rxvt=1698384292065|1698381265101; dtSa=-; at_check=true; AMCVS_99591C8B53306B560A490D4D%40AdobeOrg=1; s_cc=true; __blka_ts=1698384280556; s_sq=%5B%5BB%5D%5D; fs_lua=1.1698382485099; mboxEdgeCluster=38; c4=guest; c15=msc%3Acategory%3Aabrasives; s_invisit=true; s_ppvl=msc%253Acategory%253Aabrasives%2C58%2C42%2C1994%2C732%2C968%2C1920%2C1080%2C1%2CL; s_ppv=msc%253Acategory%253Aabrasives%2C33%2C33%2C1131%2C732%2C968%2C1920%2C1080%2C1%2CL; _uetsid=de35f150746c11ee9772ab950ff5fcb8; _uetvid=de361d90746c11eebe2775af01e2a037; _gat_gtag_UA_71253885_1=1",
#     "Upgrade-Insecure-Requests": "1",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-User": "?1",
# }

# # Set up Selenium options with the provided headers
# chrome_options = Options()


# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument("--disable-web-security")
# chrome_options.add_argument("--disable-xss-auditor")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--disable-software-rasterizer")
# chrome_options.add_argument("--disable-software-rasterizer")

# for key, value in headers_data.items():
#     chrome_options.add_argument(f"--header={key}:{value}")
    
# seleniumwire_options = {
#     'proxy': {
#         'http': f'http://{proxy_username}:{proxy_password}@p.webshare.io:80',
#         'verify_ssl': False,
#     },
# }
# # Create a WebDriver instance with the specified options
# # driver = webdriver.Chrome(seleniumwire_options)
# driver = webdriver.Chrome(
#     seleniumwire_options=seleniumwire_options
# )
# # Navigate to the URL
# url = 'https://www.mscdirect.com/browse/Abrasives?navid=2100008'

# driver.get(url)


# # Wait for a specific element to become visible (adjust the element selector as needed)
# wait = WebDriverWait(driver, 10)

# element = wait.until(EC.visibility_of_element_located((By.XPATH, "//Your/XPath/Selector/Here")))

# print(element)

# # Perform some interactions with the webpage (example: scrolling down)
# actions = ActionChains(driver)
# actions.send_keys(Keys.PAGE_DOWN)
# actions.perform()

# # You can continue interacting with the webpage using Selenium as needed.

# # Don't forget to close the WebDriver when you're done
# driver.quit()

# from bs4 import BeautifulSoup
# from selenium import webdriver
# from lazy_crawler.lib.user_agent import get_user_agent
# from selenium.webdriver.common.proxy import Proxy
# from selenium.webdriver.common.proxy import ProxyType

# proxy_server = 'p.webshare.io:80'
# proxy_username = "gkoffhkj-rotate"
# proxy_password = "9qsx6zrpagq6"

# # Create a Proxy object and set proxy type to HTTP
# proxy = Proxy()
# proxy.proxy_type = ProxyType.MANUAL

# # Set proxy server and credentials
# proxy.http_proxy = f"{proxy_username}:{proxy_password}@{proxy_server}"


# url = 'https://www.mscdirect.com/browse/Abrasives?navid=2100008'

# options = webdriver.ChromeOptions()

# user_agent = get_user_agent('random')

# options.add_argument(f"user-agent={user_agent}")
# # options.add_argument('--proxy-server=%s' % proxy.http_proxy)

# driver = webdriver.Chrome(options=options)

# # driver = webdriver.Chrome()

# driver.get(url)
# import time
# time.sleep(1000)
# soup = BeautifulSoup(driver.page_source, features='html.parser')
# driver.quit()

# print(soup.prettify())


import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--start-maximized")

# Create a new Chrome driver instance with the specified options
driver = uc.Chrome(options=options) 
website_url = "https://www.mscdirect.com/browse/Abrasives?navid=2100008"
# Navigate to the website URL

# create the Google cache URL by adding the prefix
google_cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{website_url}"

driver.get(google_cache_url)

# Wait for the page to load for 10 seconds
# time.sleep(10)

# Take a screenshot of the page and save it as "screenshot.png"
driver.save_screenshot("screenshot.png")

# Quit the browser instance
driver.quit()