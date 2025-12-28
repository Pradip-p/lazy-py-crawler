import os
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class LazyCrawler(scrapy.Spider):
    name = "jaxa"
    allowed_domains = ['eorc.jaxa.jp']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_IP': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'RETRY_TIMES': 1,
        'COOKIES_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 180,
        'COOKIES_DEBUG': True,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.JsonWriterPipeline': 300
        }
    }

    # List of coordinates
    coordinates = [
        "N080W030_N090E000",
        "N080E000_N090E030",
        "N080E030_N090E060",
        "N080E060_N090E090",
        "N080E090_N090E120",
        "N080W120_N090W090",
        "N080W090_N090W060",
        "N080W060_N090W030",
        "N050W030_N080E000",
        "N050E000_N080E030",
        "N050E030_N080E060",
        "N050E060_N080E090",
        "N050E090_N080E120",
        "N050E120_N080E150",
        "N050E150_N080E180",
        "N050W180_N080W150",
        "N050W150_N080W120",
        "N050W120_N080W090",
        "N050W090_N080W060",
        "N050W060_N080W030",
        "N020W030_N050E000",
        "N020E000_N050E030",
        "N020E030_N050E060",
        "N020E060_N050E090",
        "N020E090_N050E120",
        "N020E120_N050E150",
        "N020E150_N050E180",
        "N020W180_N050W150",
        "N020W150_N050W120",
        "N020W120_N050W090",
        "N020W090_N050W060",
        "N020W060_N050W030",
        "S010W030_N020E000",
        "S010E000_N020E030",
        "S010E030_N020E060",
        "S010E060_N020E090",
        "S010E090_N020E120",
        "S010E120_N020E150",
        "S010E150_N020E180",
        "S010W180_N020W150",
        "S010W150_N020W120",
        "S010W120_N020W090",
        "S010W090_N020W060",
        "S010W060_N020W030",
        "S040W030_S010E000",
        "S040E000_S010E030",
        "S040E030_S010E060",
        "S040E060_S010E090",
        "S040E090_S010E120",
        "S040E120_S010E150",
        "S040E150_S010E180",
        "S040W180_S010W150",
        "S040W150_S010W120",
        "S040W120_S010W090",
        "S040W090_S010W060",
        "S040W060_S010W030",
        "S070W030_S040E000",
        "S070E000_S040E030",
        "S070E030_S040E060",
        "S070E060_S040E090",
        "S070E090_S040E120",
        "S070E120_S040E150",
        "S070E150_S040E180",
        "S070W180_S040W150",
        "S070W150_S040W120",
        "S070W120_S040W090",
        "S070W090_S040W060",
        "S070W060_S040W030",
        "S090W030_S070E000",
        "S090E000_S070E030",
        "S090E030_S070E060",
        "S090E060_S070E090",
        "S090E090_S070E120",
        "S090E120_S070E150",
        "S090E150_S070E180",
        "S090W180_S070W150",
        "S090W150_S070W120",
        "S090W120_S070W090",
        "S090W090_S070W060",
        "S090W060_S070W030"
    ]


    def start_requests(self):
        for coord in self.coordinates:
            # Define the URL for each coordinate
            url = f"https://www.eorc.jaxa.jp/ALOS/en/aw3d30/data/html_v2404/{coord.lower()}.htm"

            # Set headers dynamically for each request
            headers = {
                'authority': 'www.eorc.jaxa.jp',
                'method': 'GET',
                'path': f'/ALOS/en/aw3d30/data/html_v2404/xml/{coord}.xml',
                'scheme': 'https',
                'accept': 'application/xml, text/xml, */*; q=0.01',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': 'Basic cHJhZGlwdGhhcGEubmF4YUBnbWFpbC5jb206YXczZDMw',
                'cache-control': 'no-cache',
                'cookie': '7d2b03=iutDIdJpS5k77JRGglJndfc5ILQy/jnhLhSI1SsqpFJpAjIXYdRUn8kPTqp8yYgq3xfUJOqBDHVo5hYJqVhapiJn+evMip0u6///PQFgAwMhJCQD3zb1odf2zW6N0BXFlRwQyFLiHJpuWT5+LfwekcgK8zcisJTae3yJ+BxkKFO2QgLy',
                'pragma': 'no-cache',
                'referer': f'https://www.eorc.jaxa.jp/ALOS/en/aw3d30/data/html_v2404/{coord.lower()}.htm',
                'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Extract the caption text from the response
        caption = response.xpath('//caption/text()').extract_first()

        # Construct the next URL using the extracted caption
        next_url = f'https://www.eorc.jaxa.jp/ALOS/en/aw3d30/data/html_v2404/xml/{caption}_5_5.xml'

        # Define the headers to be passed in the request
        headers = {
            'authority': 'www.eorc.jaxa.jp',
            'path': '/ALOS/en/aw3d30/data/html_v2404/xml/{caption}_5_5.xml',
            'method': 'GET',
            'accept': 'application/xml, text/xml, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'Basic cHJhZGlwdGhhcGEubmF4YUBnbWFpbC5jb206YXczZDMw',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': f'https://www.eorc.jaxa.jp/ALOS/en/aw3d30/data/html_v2404/xml/{caption}_5_5.xml',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        yield scrapy.Request(next_url, headers=headers, callback=self.parse_coords)

    def parse_coords(self, response):
        # Extract the CDATA content
        cdata_text = response.xpath('//text/text()').get()

        # Use regular expression to find all occurrences of the coordinate blocks
        pattern = r'class="list_5deg">(.*?)<'
        coords = re.findall(pattern, cdata_text)
        pattern = r"location.href='(https:\/\/www\.eorc\.jaxa\.jp\/ALOS\/aw3d30\/data\/release_v2404\/[^']+\.zip)'"
        zip_urls = re.findall(pattern, response.text)

        # Iterate over the extracted coordinates #this are 5 * 5 dig.....
        for coord in coords:
            # url = "https://www.eorc.jaxa.jp/ALOS/en/aw3d30/data/html_v2404/dl/download_v2404.htm?N045E060_N049E060"
            lst_coord = coord.split('_')
            yield {
                'url': response.url,
                'coordinate': coord,
                'download_url': f'https://www.eorc.jaxa.jp/ALOS/aw3d30/data/release_v2404/{lst_coord[0]}/{lst_coord[-1]}.zip'
            }



# Set the Scrapy settings module
settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

# Start the crawler process
process = CrawlerProcess(get_project_settings())
process.crawl(LazyCrawler)
process.start()  # The script will block here until the crawling is finished
