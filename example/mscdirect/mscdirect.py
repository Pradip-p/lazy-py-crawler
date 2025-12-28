
import base64
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.html import to_browser
from lazy_crawler.lib.user_agent import get_user_agent
import ipdb

class LazyCrawler(scrapy.Spider):

    name = "mscdirect"

    allowed_domains = ['mscdirect.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 2,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 180,
        'REDIRECT_ENABLED' : False,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': None
        }
    }

    HEADERS = {
        'Accept':' application/json, text/plain, */*',
        'Accept-Encoding':' gzip, deflate, br',
        'Accept-Language':' en-US,en;q=0.9',
        'trackingId':'',
        'brUid':'',
        'Connection': 'keep-alive',
        # 'Cookie': 'visid_incap_2587862=PDaFEYJERBmaHIlllA6DMvEOO2UAAAAAQUIPAAAAAABAWFV7Cjy0rTslA7nNzxBO; incap_ses_50_2587862=z2zqGXR6I2vyewVq/aKxAPEOO2UAAAAA0NmG2n/qwO4NkQEq4e9TMg==; dtCookie=v_4_srv_28_sn_0ABAA50E87E9C1C079852FFD8D532CF6_perc_100000_ol_0_mul_1_app-3A4933650768ea878a_1_rcs-3Acss_0; Mscdirect=3859290540.33588.0000; rxVisitor=1698369284565LNBN0T0VTAE8SSDUD3GVFDQR401IV91L; at_check=true; AMCVS_99591C8B53306B560A490D4D%40AdobeOrg=1; AMCV_99591C8B53306B560A490D4D%40AdobeOrg=-1124106680%7CMCIDTS%7C19658%7CMCMID%7C12943450803725019072851901685428099152%7CMCAAMLH-1698974086%7C3%7CMCAAMB-1698974086%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1698376487s%7CNONE%7CvVersion%7C5.2.0; mboxEdgeCluster=38; WCDE_XREFCONTACTNUMBERGUEST=; cj_channel=Direct_Navigation; s_vnum=1698776100413%26vn%3D1; s_invisit=true; s_cc=true; gig_canary=false; cjConsent=MHxOfDB8Tnww; cjUser=14d32b45-2a6a-4a32-81fd-299fab349732; _gcl_au=1.1.1577336414.1698369306; _gid=GA1.2.1298278360.1698369306; _blka_ruab=154; sa-user-id=s%253A0-43afeb23-8be3-561a-6914-0c737c6c8308.Y8f%252BRPPxnRHG5aE3gOkWqxPgz%252BtvsNLkRYcgRKdchJI; sa-user-id-v2=s%253AQ6_rI4vjVhppFAxzfGyDCBsiZHI.bvS8AFDXCza0ZMC45DNR3vx%252FYJQxNrxNrl5uO0PC1Fo; sa-user-id-v3=s%253AAQAKIDVpIORW7Vqngy1xAYpC_9lqBi7akSRRQNhWLBEet82FENYBGAQg9eieqAYwAToEY-o0A0IETYdSRQ.fk1k3J1skic71K%252FMOrCiBQZgM%252BCgkLyHoQPvDLJtLs8; _fbp=fb.1.1698369307676.81252574; _clck=zdztz|2|fg7|0|1395; gig_bootstrap_4_R0HZVTou0ajlxJ_Xco0l_w=identity_ver4; gig_canary_ver=15482-3-28306170; lastBrowseBookmark=L2Jyb3dzZS90bi9Qb3dlci1Ub29scy9FdGNoZXJzLUVuZ3JhdmVycy1BY2Nlc3Nvcmllcy9FdGNoZXJzLUVuZ3JhdmVycz9uYXZpZD0yMTA3MjQ3; lastViewedBeforeLogin=aHR0cHM6Ly93d3cubXNjZGlyZWN0LmNvbS9icm93c2UvdG4vUG93ZXItVG9vbHMvRXRjaGVycy1FbmdyYXZlcnMtQWNjZXNzb3JpZXMvRXRjaGVycy1FbmdyYXZlcnM/bmF2aWQ9MjEwNzI0Nw==; c4=guest; nlbi_2587862=KGtFEepAlW2nj3FXZ8kABQAAAAAKlN7VzNcTWqQ+37p3Y03S; dtSa=-; s_sq=%5B%5BB%5D%5D; pn=17; utag_main=v_id:018b6eb2dd7e0013ddc786c71faf05065007705d00bd0$_sn:1$_se:49$_ss:0$_st:1698372618610$ses_id:1698369297793%3Bexp-session$_pn:16%3Bexp-session$vapi_domain:mscdirect.com; cross_sell_id=%5B%5BB%5D%5D; c15=msc%3Aproducts%3A%3A; _br_uid_2=uid%3D8902830592928%3Av%3D12.0%3Ats%3D1698369305328%3Ahc%3D16; _uetsid=423ac5c0746611ee859183a3d8eeda88; _uetvid=423b09c0746611ee9af4995c941d2919; __blka_ts=1698372619825; _ga=GA1.1.2113955838.1698369306; fs_lua=1.1698370820959; fs_uid=#10Q6K5#d588560f-b9e9-4030-a706-ba95f0283730:79aec3b1-85ad-4926-a240-4b9c0b2f3553:1698369309366::15#/1729905305; s_ppvl=msc%253Aproducts%253A%253A%2C100%2C100%2C976%2C1850%2C976%2C1920%2C1080%2C1%2CP; _clsk=scdaug|1698370821619|16|1|z.clarity.ms/collect; reese84=3:ap6J9LAMX1MjQ9Al4tfdwg==:hZDoFTYxiQt/YLVBuqaufaJPHvkGtQ4+QvZjeFTBeXLb6cR5YfZYuHPO76aFQgHhVBVKp3N2NiAkq360bXWUUVWTi6tdq7UoUS7lo2Wc6HCFlYjP8THGp1rWnwq6qI0ltm9GBFNqP2nXja8vSiNi6P8XK807Wl5+p/fjOy+GiPD+AiURmGEYa1jOSbaHoDy0n/kxxsplreF2hl9fozmrWkNwABXuY6YrMqu40TDzXbbVm9OPEOOoqyhFUmWTB1d6RipCelAAqHx2eqgj2v3GM9a1vLsK6/X43MDkK26kh9LUPjmnZCjhcmabWLDhm+17WbIoceaxTKhf3DPgdsjT9XhahLAAIOU9otPyT7MLx1N/syR3cpA3Q/SSQikZSqs6ibtPvAxSvf9tIbSbz0SWidiCqLKhVCY3LieLpNIXWik4mUei6K1xdpmD2hcCUyUo7lWPcIu9pAUCy2xmeQVZDQ==:oqgpTQasiPargGPR+gv9/NyvFg/63nkUgD1KavRt5J0=; s_ppv=msc%253Aproducts%253A%253A%2C90%2C30%2C2896%2C888%2C976%2C1920%2C1080%2C1%2CL; _ga_KG0FCGTKBP=GS1.1.1698369306.1.1.1698371063.44.0.0; _ga_CM5B4R0KX7=GS1.1.1698369306.1.1.1698371063.44.0.0; nlbi_2587862_2147483392=Jr9rFGn64B02i6AlZ8kABQAAAACZOFEkzSMiJPoAHCxrhuQ9; mbox=session#9a72b41602e7483dbd76ad3b6d12bf7d#1698372925|PC#9a72b41602e7483dbd76ad3b6d12bf7d.38_0#1761615865; rxvt=1698372866990|1698369284571; dtPC=28$371063488_541h12vAFOWJOKWIFHLGVCTAAUKALHUDGNQUDIL-0e0',
        "Host": "www.mscdirect.com",
        "X-Dtpc": "28$371063488_541h12vAFOWJOKWIFHLGVCTAAUKALHUDGNQUDIL-0e0",
        "X-Mscqa-Test": 1
    }


    def start_requests(self):

        url = 'https://www.mscdirect.com/categories/'

        headers = {
            'User-Agent': get_user_agent('random'),
            **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
            }

        yield scrapy.Request(url, callback=self.parse_product_urls,
                            headers= headers,
                            dont_filter=True)


    def parse_product_urls(self, response):
        # response_data = response.json()
        # for category in response_data['availableRefinements']:
        #     for cat in category['refinementValues']:
        #         id_ = cat['id']
        #         category_name = cat.get('value')


        headers_data = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": 'visid_incap_2587862=tNDYOB4sQUCJRyDF3/lguaxSO2UAAAAAQUIPAAAAAACdD8p52qHeEXn9OaGePnOU; cj_channel=Direct_Navigation; cjConsent=MHxOfDB8Tnww; cjUser=81d9b193-42f7-4fe9-8914-d0412303eeae; WCDE_XREFCONTACTNUMBERGUEST=; _gcl_au=1.1.711734735.1698386612; _gid=GA1.2.29800666.1698386612; _blka_ruab=159; sa-user-id=s%253A0-43afeb23-8be3-561a-6914-0c737c6c8308.Y8f%252BRPPxnRHG5aE3gOkWqxPgz%252BtvsNLkRYcgRKdchJI; sa-user-id-v2=s%253AQ6_rI4vjVhppFAxzfGyDCBsiZHI.bvS8AFDXCza0ZMC45DNR3vx%252FYJQxNrxNrl5uO0PC1Fo; sa-user-id-v3=s%253AAQAKIDVpIORW7Vqngy1xAYpC_9lqBi7akSRRQNhWLBEet82FENYBGAQg9eieqAYwAToEY-o0A0IETYdSRQ.fk1k3J1skic71K%252FMOrCiBQZgM%252BCgkLyHoQPvDLJtLs8; _fbp=fb.1.1698386612400.1470456857; _clck=h38bq5|2|fg7|0|1395; gig_bootstrap_4_R0HZVTou0ajlxJ_Xco0l_w=identity_ver4; incap_ses_50_2587862=DSxoTSKIfAf0g+Vq/aKxAOp7O2UAAAAAIZg6b/3km00GZCcPgazYdQ==; dtCookie=v_4_srv_24_sn_959726F527195983ABC7D9E83F5F8F8B_perc_100000_ol_0_mul_1_app-3A4933650768ea878a_1_rcs-3Acss_0; nlbi_2587862=v/dMCEYEh2052bc3Z8kABQAAAACpE1WM/5mJBSOOjaOezxOn; rxVisitor=1698397168914R3MLJD3G9HC5LBHJTI27ODGMJ24SL8I5; at_check=true; Mscdirect=3926399404.33588.0000; AMCVS_99591C8B53306B560A490D4D%40AdobeOrg=1; AMCV_99591C8B53306B560A490D4D%40AdobeOrg=-1124106680%7CMCIDTS%7C19658%7CMCMID%7C12943450803725019072851901685428099152%7CMCAAMLH-1699001975%7C3%7CMCAAMB-1699001975%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1698404375s%7CNONE%7CvVersion%7C5.2.0; c4=guest; c15=msc%3Acategory%3Aabrasives; s_vnum=1698776100367%26vn%3D2; s_invisit=true; s_cc=true; reese84=3:uvIx8r3mYsnmqGpkpeHPYA==:wIib0hqrWCoFk1vnxaLX2TAl9lXODwA+PY1AiOelfpDibQ8YgMta/ZCRJ+z8ScRz92SUIqaHdWgdsqWcYfdKSolmITvQqFDWRNxGtEfKoAHHzdOjzhev6vfarVOgp78qbgriSuOXphBwV6LfvzRCuRaJE9vSxQhdpux2mUjkLM8mdEx3wRueoFmdbY8rVk/TJxU3ePbX95U5xPBLK0TgJ3ZQ6Kodkn8WWn1Xa7verYQla3ZivcihMgskpktIeft3IsHmy0/ngOH6h1oKeFSnfR9ZV3J6YjYNxfOkB8xgKP05WIzMs7P3mr7Tukst5o8fO6sCd4zW9zAPuwJjmeAXDGPNJxDaDsaClGB91abV4ITOcjfwkfi53To9by7fFCULCNC1ndBLoz/vkczqsPvm6oWD937aHjqBhiz8bbT00fkz4DM2rD6GpyabYbM3Jvo6WckyxwfdFWDpXvZD45bbxdpqxxRrDblK1u6pVgY3mXY=:qFiyvXCVtD2jUF9y0jkiqg/aSjdo7rDizkUra8FwehI=; dtSa=-; mboxEdgeCluster=38; mbox=PC#b4382606bc3e480f9e0bdecc9a9dd527.38_0#1761643688|session#23028205d6b74263b47c7a4418d55b06#1698400748; nlbi_2587862_2147483392=jMv3SZWlawUuag95Z8kABQAAAAA1o0wDD4S37xWtQtIslI9S; gig_canary=false; gig_canary_ver=15482-3-28306635; _br_uid_2=uid%3D7604019146950%3Av%3D12.0%3Ats%3D1698386612017%3Ahc%3D10; _ga_KG0FCGTKBP=GS1.1.1698398893.2.0.1698398893.60.0.0; _ga=GA1.1.1254696081.1698386612; _uetsid=8e844c30748e11ee80dfcf6d98d00eb5; _uetvid=8e845f40748e11ee907ee53fa8463206; __blka_ts=1698400695104; fs_lua=1.169839889670',
            "Host": "www.mscdirect.com",
            "Sec-Fetch-Dest": "document",
            # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            'User-Agent': get_user_agent('random')
        }

        # url ='https://www.mscdirect.com/browse{}'.format(cat.get('link'))

        url = 'https://www.mscdirect.com/browse/Abrasives?navid=2100008'

        yield scrapy.Request(url, self.sub_category, dont_filter=True,
                        headers= headers_data)

        # yield scrapy.Request(url, callback=self.sub_category,headers= headers_data, dont_filter=True)

    def sub_category(self, response):
        # to_browser(response)
        print(response.text)
        pass


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
