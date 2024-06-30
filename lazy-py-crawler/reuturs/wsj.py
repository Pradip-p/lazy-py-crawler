import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
from urllib.parse import quote
from lazy_crawler.lib.user_agent import get_user_agent

class LazyCrawler(scrapy.Spider):

    name = "wsj"

    start_urls = ["https://www.wsj.com/"]

    custom_settings = {
        'ITEM_PIPELINES' : {
        'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }

    base_url = "https://www.wsj.com/news/economy"

    def start_requests(self):
        url = self.get_url()
        print(url)
        # yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.body)
        collection = data["collection"]
        for item in collection:
            arctile_id = item.get('id')
            type_ = item.get('type')
            url = 'https://www.wsj.com/news/economy?id={}&type={}'.format(arctile_id, type_)
            yield scrapy.Request(url, self.parse_article, dont_filter=True)
        

    def parse_article(self, response):
        res = json.loads(response.body)
        data = res['data']
        canonical_url = data['canonical_url']
        headline = data['headline']
        summary = data['summary']
        url = data['url']
        yield scrapy.Request(url, self.details, dont_filter=True, meta={'title':headline,'summary':summary})

    def details(self, response):
        
        author = response.xpath('//a[@class="css-mbn33i-AuthorLink e10pnb9y0"]/text()').extract_first()
        time = response.xpath('//time[@class="css-a8mttu-Timestamp-Timestamp emlnvus0"]/text()').extract_first()
        desc = response.xpath('//section[@class="ef4qpkp0 css-1h33ts-Container e1of74uw17"]/p//text()').extract()
        
        yield{
            'title' : response.meta['title'],
            'author':author,
            'date':time,
            'url': response.url,
            'summary':response.meta['summary'],
            'description': desc
        }

    def get_url(self):
        query_param = {
            "count": 10,
            "query": {
                "and": [
                    {
                        "terms": {
                            "key": "Product",
                            "value": ["WSJ.com", "WSJ Blogs"]
                        }
                    }
                ],
                "or": [
                    {
                        "term": {
                            "key": "KeyWord",
                            "value": "markets"
                        }
                    },
                    {
                        "terms": {
                            "key": "SectionName",
                            "value": ["markets", "Real Time markets"]
                        }
                    }
                ],
                "not": [
                    {
                        "term": {
                            "key": "SectionName",
                            "value": "Opinion"
                        }
                    }
                ]
            },
            "sort": [
                {
                    "key": "LiveDate",
                    "order": "desc"
                }
            ]
        }

        query_param_str = quote(json.dumps(query_param))
        return f"{self.base_url}?id={query_param_str}&type=allesseh_content_full"
    

# class LazyCrawler(scrapy.Spider):

#     name = "wsj"


#     custom_settings = {
#         'ITEM_PIPELINES' : {
#         'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
#         }
#     }

#     def start_requests(self):
#         url = 'https://www.wsj.com/search?query=Economy&page=3'
#         yield scrapy.Request(url, self.parse_urls, dont_filter=True, headers={'User-Agent': get_user_agent('random')}
#                 )

#     def parse_urls(self, response):
#         urls = response.xpath('//div[@class="WSJTheme--headline--7VCzo7Ay"]')
#         print(urls)
#         # urls = response.xpath('//div[@class="WSJTheme--headline--unZqjb45 undefined WSJTheme--heading-3--2z_phq5h typography--serif-display--ZXeuhS5E "]/a/@href').extract()

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start()
