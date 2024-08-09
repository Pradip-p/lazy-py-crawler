from datetime import datetime
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import pytz

class LazyCrawler(scrapy.Spider):

    name = "reuters"
    start_urls = ["https://www.reuters.com/"]
    page_size = 100
    page_number = 0
    max_pages = None
    total_items = 0  # Initialize counter variable

    custom_settings = {
        'ITEM_PIPELINES' : {
        'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }

    base_url = "https://www.reuters.com/pf/api/v3/content/fetch/recent-stories-by-sections-v1"

    def start_requests(self):
        sections = ['business', 'technology','markets']
        for section in sections:
            url = self.get_url(section)
            yield scrapy.Request(url, self.parse, dont_filter=True, meta={'section_id':section})

    def parse(self, response):
        res = response.json()
        data = res['result']
        articles = data['articles']

        for article in articles:
            published_time_str = article['published_time']
            # Parse the datetime string and remove the timezone information
            published_time = datetime.fromisoformat(published_time_str.replace('Z', ''))
            # Convert the datetime to UTC timezone
            published_time_utc = pytz.utc.localize(published_time)
            if published_time_utc < datetime(2021, 1, 1, tzinfo=pytz.utc) or published_time_utc > datetime(2023, 4, 30, tzinfo=pytz.utc):
                continue

            author_name = []
            authors = article.get('authors')
            if authors:
                for author in authors:
                    name = author.get('name') if author else 'None'
                    author_name.append(name)
            url = 'https://www.reuters.com{}'.format(article['canonical_url'])

            pass_data = {
                'title': article['title'],
                'date': published_time_str,
                'display_time': article['display_time'],
                'authors':' '.join(author_name),
                'short_description': article['description'],
                'url':'https://www.reuters.com{}'.format(article['canonical_url'])
            }
            yield scrapy.Request(url, self.parse_article, meta={'pass_data':pass_data}, dont_filter=True)


        if self.max_pages is None:
            self.max_pages = data['pagination'].get('total_size', 0) // self.page_size + 1

        if self.page_number < self.max_pages:
            self.page_number += 1
            section_id = response.meta['section_id']
            url = self.get_url(section_id)
            yield scrapy.Request(url, self.parse, dont_filter=True, meta={'section_id': section_id})

    def parse_article(self, response):
        pass_data = response.meta['pass_data']
        title = pass_data['title']
        date = pass_data['date']
        display_time = pass_data['display_time']
        authors = pass_data['authors']
        short_description = pass_data['short_description']
        article_text =  ' '.join(response.css('p.article-body__element__2p5pI::text').getall())

        yield {
            'title': title,
            'date': date,
            'display_time':display_time,
            'author':authors,
            'url': response.url,
            'short_description': short_description,
            'article_text': article_text
        }


    def get_url(self, section_id):
        return f"{self.base_url}?query={json.dumps({'section_ids': f'/{section_id}/', 'size': self.page_size, 'offset': self.page_number * self.page_size, 'website': 'reuters'})}"
        # return f"{self.base_url}?query={json.dumps({'section_ids': '/business/', 'size': self.page_size, 'offset': self.page_number * self.page_size, 'website': 'reuters'})}"

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start()
