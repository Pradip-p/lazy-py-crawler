#!/usr/bin/env python
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
import gc
import time
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy import FormRequest
import json


class LazyCrawler(LazyBaseCrawler):
    def errback_http_ignored(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 430:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                time.sleep(240)  # Wait for 4 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

            if response.status == 503:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                time.sleep(480)  # Wait for 8 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

    def _retry_request(self, request, reason, spider):
        retryreq = request.copy()
        retryreq.meta['retry_times'] = request.meta.get('retry_times', 0) + 1
        retryreq.dont_filter = True
        return retryreq

    name = "chewy"

    allowed_domains = ['chewy.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,'LOG_LEVEL': 'DEBUG',

        'CONCURRENT_REQUESTS' : 32,'CONCURRENT_REQUESTS_PER_IP': 32,

        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,'RETRY_TIMES': 1,

        # "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,

        'ITEM_PIPELINES' :  {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': None
        }
    }

    HEADERS = {
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        'Content-Type': 'application/json',

    }
    HEADERS = {
        :Authority:
www.chewy.com
:Method:
POST
:Path:
/api/pdp/graphql
:Scheme:
https
Accept:
*/*
Accept-Encoding:
gzip, deflate, br
Accept-Language:
en-US,en;q=0.9
Content-Length:
1310
Content-Type:
application/json
Cookie:
bm_sz=1950372AB90CE02DA6B251B913A50384~YAAQlJbTZ51eiwGJAQAAXKucDxS41o80Sg2DuimspojRDb0LWXHysvKucxC0uyjCMOGRruoLSMFPMQhQ2s6i+7eDbm2jcVJ1b+fpGYLfiAsrP3Rh1NJ+giOg1XKGus89vqsPVPs+evGTe/hn5UTNvTu2Aet20nihLdy2guBBgYeOCKMRS2Wf5bg3kmN0sI+OMihFy3tjJpr30QkWQSsWh6BsqolRphZWTd3uUHwaIngFgvx521+wmwnAulGUoHPvPm21CFLARQsrnnvYvPeGuARPpCXY2u9Nm4TSl630CksKLw==~4404279~4535352; hpNext=true; experiment_=; pid=UxWuv7xBQdO6nALG3S8C6Q_; abTestingAnonymousPID=UxWuv7xBQdO6nALG3S8C6Q_; _abck=E8AC601C48BF48D230069E2E1F4BE830~0~YAAQlJbTZyJfiwGJAQAAz8GcDwrVAD2iMx3JRqRiBCs8JCI5+SITdNhfe/FZDWxBU24d0sOagkX/hED+/H1c2ckUfr3tkme7KSIsjLvaMA6sciUdQVIVGVGgXw1gdnzT/HZpOsQBRUSK1UtFbMDgAJVqTrFeaO45wn+Fvg+nmr7LyDhB1XuX/d6t0lPv8T2ArhBxicLF+EdifU1nwM7GJVspRW2+shUsANU1JJkfgDPZIihYkVGxevEfQBVYzqEaH8TQNRmlyUU82eqDG4zd0X2Ngd2p52ncSvzR/Z4cwKUYzoyFEbYAV4AIA0R9F+dgflDQx2TtuZTxm9cRozwhuOZOU8zJDvPLfEnEX6YZmKl7TGxwRMYTXuJ925l1/8WOBUEzjP2Na+AoYa3mCeBaTJKFi/InKg==~-1~||-1||~-1; _gcl_au=1.1.159745078.1688184080; _gid=GA1.2.1466779058.1688184081; experiment_2022_10_NAV_INGRESS_SUPERLATIVE=CONTROL; experiment_2023_02_NAV_IA_TEST=CONTROL; experiment_2023_05_NAV_UX_HAMBURGER=CONTROL; _mibhv=anon-1688184081704-3738703695_6593; _fbp=fb.1.1688184083479.335354260; _tt_enable_cookie=1; _ttp=EHPQ-flN4s3wIcn47sxb1mobL9g; FPLC=A%2FZADQQfZO213iFSHhM1I9irtFM0BGj3pR9H%2FJjaK%2FWrWn%2FvvjTaY%2BNnYLdIM9Ub%2BWwroMNKMxFdvygGtQSCEfUGtjPGrJcfrQD6JWFi%2Bwpu8lo7exAyHTF%2BYGxfog%3D%3D; FPID=FPID1.2.%2Fti5Nnkcq8HoWCx3hU2WZQA0rEHuTjr43v1L0RkNpns%3D.1688184081; ajs_anonymous_id=9bbe58c9-cd81-42c7-bc74-07ac89c4a7a6; sid=85da19c5-ac2d-4e89-aa1f-e2b40ff075f5; x-feature-preview=false; bm_mi=6E58518CB46B4FCC2B6E73E6B87C6DFD~YAAQp5bTZy9yyfqIAQAAJ+0LEBQQESdiykWW+sVSqFOXz7RPti+jN5cSkKAj7C+Q3dLOwc/Uf3Gw6FI8n0Y00KCbVS/eSIuFEL1q7qaCBSLiaYCkYYfqao2+QqCU97cnndrtl2aSv3RWLeXQ0+GFhGfHuZS3M02fTVqxTDz19jIJmhH/3LR281G6QUkl7K+ucPnNiepY/CW+JwHHGgICFvgWBAyfrM8S9Vt1yYAYsh9VurhXd7b6IS8UcenyFAxARQIEPzDxMjLCuUqpAkN2HBXLhHUVNaSFB6z0ONzjXiuzwk6D1H5yi9GCO2El2A==~1; ak_bmsc=8C5385AD1DFBFB1AE71546F74815A5E7~000000000000000000000000000000~YAAQp5bTZ0NyyfqIAQAAZf8LEBSmymdf9p2UAUEYsJKMjtVccY622yg9ULKIr2R75+QorqQA9uKga8gAsUN3KQ9vgsjkR+2wdIEZOTPXQBf/t2PjAh5PvUaTDtvJIHg6hRLEzBiyLaU8dCGZaj/ktrsBn0aJwFbfAm/3IC0ftSdkoybfoahM7np6mAPXd30ggRTWMUI+ijCTIViMfKb/Sb96j6dWXnsxE0ZZoHEcQr6t6xX4uSn2Nka9BKga8qwJx8yj+u9c8SyzYinUyunAphQX+mhhRaACUzDEM/NUyJP1fH6xn/Lg2GYGHJRGcB8RkuzqCPlAbR8MrMG/GZHazzLxC2NGV57GxILoiEYLgjvBzG451gF1H0WiBWZQajlulCTfqvcH6WduP9LQy45Y5SIikuv7FHQMu0iQ2VjSuEXoTpdPAWeaz4lKekVcIJ6yaci8Kiwh7NtrU7RZqV+E2WFUOtsZKBEgkGsGfsL5QpFc5GhBBRbMU8scHQa76SFKDa+8pEqnJBgjKJujTmp2X6IzvJmEcJ2KuWQ0Mn3/pnq2yfCKAcsT; lastRskxRun=1688192850758; rskxRunCookie=0; rCookie=hakjqzdqlh5v23mmcf0vbdljjmfoeh; session-id=df1pdfp4c7p5jdwvi0qakw41165977; AKA_A2=A; _dc_gtm_UA-23355215-1=1; _dc_gtm_UA-12345-6=1; _dc_gtm_UA-23355215-27=1; sbsd=0000000000240428c6d640404983167baff08ff41128ea627a4785ba1f2729cebfc5dfc881e225057d-dcb6-46a5-b2d2-abcf52c6d14a16908758321688196932; _dd_s=rum=2&id=684e8ec4-d65a-4608-9901-3e2173291666&created=1688193954851&expire=1688197834756; RT="z=1&dm=www.chewy.com&si=af2b5d8a-a97c-46ea-8570-73c7519430b6&ss=ljjje9e9&sl=z&tt=8obk&obo=f&rl=1"; AWSALB=gaOvixTVAHkTqiPIGeFjrjx9KJCLuJBnXy/MMvR8YpHEa8MYJ9EQsuZc5F2W3DZVY8O5OVD6B/W5Hrn+PXbuQgUNVg31HsCqyO6yhCXN+QdVMK9n4NHDSZ1M5lXK; pageviewCount=76; _uetsid=f0482ab017c311ee960da35d147ced24; _uetvid=f0490d1017c311eebc780b1b5fdfd482; _ga_GM4GWYGVKP=GS1.1.1688187739.2.1.1688196948.25.0.0; _ga=GA1.2.1516034868.1688184081; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Jul+01+2023+13%3A20%3A52+GMT%2B0545+(Nepal+Time)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG15%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false; akavpau_defaultvp=1688197252~id=c14de525423834cd3ba44e53ea7a9775; bm_sv=B28EDA0C4D0356CE3F5F4F71EB31CB29~YAAQlJbTZ8dMjQGJAQAAOjJhEBRvJV6Phf4JYjHqRDhMMkRSPE9WqH714FGvdhgaQIQZdwgBeDH572h4Jw1Hp5fr/t77TimtwF1lIFuE03p1ZhNYmVFXgZWn/0ySTirjNwcHlyIguOeBuP9Cv38tFQ7Ta4DJPPfiM0haU34b1/T/tLihDDLVGd1AkniyS8DExoIm/akcVyDjiux0NW9LYT+Sldd932GJk7Dn3X3g8d8jcGqf0nl9+T/3x4jgXDPgpA==~1; akaalb_chewy_ALB=1688197554~op=prd_chewy_plp:www-prd-plp-use1|prd_chewy_lando:www-prd-lando-use2|chewy_com_ALB:www-chewy-use2|~rv=39~m=www-prd-plp-use1:0|www-prd-lando-use2:0|www-chewy-use2:0|~os=43a06daff4514d805d02d3b6b5e79808~id=2bc7f15e2c290969c0a795ee9fb17207
Origin:
https://www.chewy.com
Referer:
https://www.chewy.com/pedigree-complete-nutrition-grilled/dp/141433
Sec-Ch-Ua:
"Not.A/Brand";v="8", "Chromium";v="114"
Sec-Ch-Ua-Mobile:
?0
Sec-Ch-Ua-Platform:
"Linux"
Sec-Fetch-Dest:
empty
Sec-Fetch-Mode:
cors
Sec-Fetch-Site:
same-origin
User-Agent:
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
    }

    def start_requests(self): #project start from here.
        headers = {
            'User-Agent': get_user_agent('random'),
            **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
            }

        url = 'https://www.chewy.com/api/pdp/graphql'
        payload = {
            "operationName": "Reviews",
            "variables": {
                "sort": "MOST_RELEVANT",
                "id": "141433",
                "after": "YXJyYXljb25uZWN0aW9uOjk="
            },
            "extensions": {},
            "query": "query Reviews($id: String!, $after: String, $feature: String, $filter: ReviewFilter, $sort: ReviewSort = MOST_RELEVANT, $hasPhoto: Boolean, $reviewText: String) {\n  product(id: $id) {\n    id\n    ...Reviews\n    ...ReviewFeatures\n    __typename\n  }\n}\n\nfragment Reviews on Product {\n  id\n  partNumber\n  name\n  reviews(\n    after: $after\n    feature: $feature\n    filter: $filter\n    first: 10\n    sort: $sort\n    hasPhoto: $hasPhoto\n    reviewText: $reviewText\n  ) {\n    totalCount\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    edges {\n      node {\n        id\n        ...Review\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Review on Review {\n  id\n  contentId\n  helpfulness\n  photos {\n    ...UserGeneratedPhoto\n    __typename\n  }\n  rating\n  submittedAt\n  submittedBy\n  contributorBadge\n  isIncentivized\n  text\n  title\n  __typename\n}\n\nfragment UserGeneratedPhoto on UserGeneratedPhoto {\n  __typename\n  caption\n  fullImage\n  thumbnail\n}\n\nfragment ReviewFeatures on Product {\n  id\n  partNumber\n  reviewFeatures\n  __typename\n}\n"
        }

        yield FormRequest(url, dont_filter=True, formdata={'json': json.dumps(payload)}, headers=headers, callback=self.parse_response )





    def parse_response(self, response):
        print(response.text)

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
