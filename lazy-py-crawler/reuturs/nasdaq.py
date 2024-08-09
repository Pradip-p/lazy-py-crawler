import scrapy
import json
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

class LazyCrawler(scrapy.Spider):
    name = "nasdaq"
    total_count = 0
    sections_lst = ['business','techonology','markets']
    start_urls = ["https://api.nasdaq.com/api/news/topic/article?q=field_primary_topic:&limit=1000&offset=0"]

    custom_settings = {
        'ITEM_PIPELINES' : {
        'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }

    def parse(self, response):
        res = response.json()
        data = res['data']
        articles = data['rows']

        for article in articles:
            created_time_str = article['created']
            created_time = datetime.strptime(created_time_str, '%b %d, %Y')
            if created_time < datetime(2021, 1, 1) or created_time > datetime(2023, 4, 30):
                continue

            url= f"https://www.nasdaq.com{article['url']}"

            pass_data =  {
                'title': article['title'],
                'date': created_time.strftime('%Y-%m-%d'),
                'display_time': article['ago'],
                'authors': article['publisher'],
            }
            yield scrapy.Request(url, self.parse_article, meta={'pass_data':pass_data}, dont_filter=True)

        total_records = data['totalrecords']

        page_size = len(articles)
        current_offset = int(response.request.url.split('&offset=')[-1])
        if current_offset + page_size < total_records:
            next_offset = current_offset + page_size
            next_url = f"https://api.nasdaq.com/api/news/topic/article?q=field_primary_topic:&limit=1000&offset={next_offset}"
            yield scrapy.Request(next_url, self.parse, dont_filter=True)


    def parse_article(self, response):
        pass_data = response.meta['pass_data']
        title = pass_data['title']
        date = pass_data['date']
        display_time = pass_data['display_time']
        authors = pass_data['authors']
        description =  ' '.join(response.xpath('//div[@class="body__content"]/p//text()').extract())

        yield {
            'title': title,
            'date': date,
            'display_time':display_time,
            'author':authors,
            'url': response.url,
            'article_text': description
        }
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start()
