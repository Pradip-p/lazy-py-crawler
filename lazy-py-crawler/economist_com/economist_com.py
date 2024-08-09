
import os
import pytz
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
from scrapy.linkextractors import LinkExtractor
import scrapy
# from lazy_crawler.puppeteer.puppeteer import browse
class LazyCrawler(LazyBaseCrawler):

    custom_settings = {
        'DOWNLOAD_DELAY': 1,'LOG_LEVEL': 'DEBUG','CHANGE_PROXY_AFTER':1,'USE_PROXY':True,
        'CONCURRENT_REQUESTS' : 126,'CONCURRENT_REQUESTS_PER_IP': 26,'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'JOBDIR': './crawls', 'RETRY_TIMES': 2, "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 500,
        'ITEM_PIPELINES' : {
        'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }



    headers = get_user_agent('random')

    page_num = 1

    def start_requests(self):
        sections = ['business','science-and-technology','finance-and-economics']

        for section in sections:
            urls = ['https://www.economist.com/{}'.format(section)]
            for url in urls:
                yield scrapy.Request(url, self.parse_page, dont_filter=True, meta={'section':section})


    def parse_page(self, response):

        links = response.xpath('//h3[@class="css-juaghv eifj80y0"]/a/@href').extract()
        for link in links:
            link = 'https://www.economist.com{}'.format(link)
            yield scrapy.Request(link, self.article_details, dont_filter=True)

        self.page_num += 1
        next_url = response.xpath('//a[@class="ds-pagination__nav-link"]/@href').extract_first()
        # if self.page_num <= 918:
        if next_url:
            section = response.meta['section']
            url = 'https://www.economist.com/{}?page={}'.format(section, self.page_num)
            yield scrapy.Request(url, self.parse_page, dont_filter=True, meta={'section': section})

    def article_details(self, response):
        title = response.xpath('//h1[@class="css-1bo5zl0 e164j1a30"]/text()').extract_first()
        # author = response.xpath('//span[@class="css-1a0w51d e1bvn4wd0"]/text()').extract_first()
        desc = response.xpath('//div[@class="css-13gy2f5 e1prll3w0"]/p//text()').extract()
        published_time_str = response.xpath('//time[@class="css-j5ehde e1fl1tsy0"]/@datetime').extract_first()
        if published_time_str:
            published_time = datetime.fromisoformat(published_time_str.replace('Z', ''))
            # Convert the datetime to UTC timezone
            published_time_utc = pytz.utc.localize(published_time)
            if published_time_utc < datetime(2021, 1, 1, tzinfo=pytz.utc) or published_time_utc > datetime(2023, 4, 30, tzinfo=pytz.utc):
                return None

        else:
            published_time_str = ''

        yield {
            'title':title,
            'published_at': published_time_str,
            'url': response.url,
            'description':' '.join(desc)
        }





settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
