import scrapy
import os
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.lib.user_agent import get_user_agent
import json

class LazyCrawler(LazyBaseCrawler):
    name = 'login'

    custom_settings = {
        'ITEM_PIPELINES' : {
            'lazy_crawler.crawler.pipelines.ExcelWriterPipeline': 300
        }
    }
    
    def start_requests(self):
        url = "https://graphql.lickd.io/"  # Replace with the actual URL
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            # Add any other headers you need
        }
        
        data = {
            "query": "query ($query: String, $sortMode: FindSortMode, $sortOrder: FindSortOrder, $pagination: PaginationInput, $filters: FindFiltersInput) {\n  find(query: $query, filters: $filters) {\n    tracks(pagination: $pagination, sortOrder: $sortOrder, sortMode: $sortMode) {\n      pagination {\n        total\n        totalPages\n        from\n        size\n        page\n        __typename\n      }\n      results {\n        identity\n        highlight {\n          key\n          value\n          __typename\n        }\n        title\n        releases {\n          title\n          slug\n          artist {\n            slug\n            __typename\n          }\n          __typename\n        }\n        slug\n        duration\n        created_at\n        is_charting\n        is_featured\n        is_new_release\n        is_stock_music\n        mixes_count\n        brand_sponsored\n        branded_content\n        audio {\n          identity\n          __typename\n        }\n        images {\n          identity\n          __typename\n        }\n        artists {\n          highlight {\n            key\n            value\n            __typename\n          }\n          name\n          slug\n          identity\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables": {
                "query": "",
                "pagination": {
                    "size": 25,
                    "from": 25
                },
                "sortMode": "POPULAR_SPOTIFY",
                "sortOrder": None,
                "filters": {
                    "catalogueType": "ALL",
                    "identity": None,
                    "isrc": None,
                    "upc": None,
                    "track": None,
                    "artist": None,
                    "release": None,
                    "rightsholder": None,
                    "playlist": None,
                    "mood": None,
                    "theme": None,
                    "genre": None,
                    "bpmMin": None,
                    "bpmMax": None,
                    "durationMin": None,
                    "durationMax": None,
                    "releasedAfter": None,
                    "releasedBefore": None,
                    "letter": None,
                    "letters": None,
                    "language": None,
                    "brandSponsored": None,
                    "brandedContent": None,
                    "explicit": None,
                    "featured": None,
                    "instrumental": None,
                    "dailymotion": None,
                    "facebook": None,
                    "instagram": None,
                    "linkedin": None,
                    "snapchat": None,
                    "twitch": None,
                    "twitter": None,
                    "vimeo": None,
                    "youtube": None,
                    "TikTok": None,
                    "podcasting": None,
                    "matchArtistFallback": True
                }
            },
            "operationName": ""
        }

        json_data = json.dumps(data)  # Convert the dictionary to JSON

        yield scrapy.Request(
            url=url,
            method="POST",
            headers=headers,
            body=json_data,
            callback=self.parse,
            meta={'data': data}
        )

    
    def parse(self, response):
        data_load = json.loads(response.body)
        results = data_load['data']['find']['tracks']['results']
        
        for result in results:
            artists = result['artists'][0]
            articst_name  = artists['name']
            duration = result['duration']
            created_at = result['created_at']
            
            yield{
                'track name': result.get('title'),
                'articst_name': articst_name,
                'duration': duration,
                'created_at':created_at
            }
            
        # Extract pagination data from the response
        pagination = data_load['data']['find']['tracks']['pagination']
        total_pages = pagination['totalPages']
        current_page = pagination['page']
        data = response.meta['data']
        if current_page < total_pages:
            next_page = current_page + 1

            # Update the pagination values in the data payload
            data['variables']['pagination']['from'] = next_page * data['variables']['pagination']['size']
            yield scrapy.Request(
                url=response.url,
                method="POST",
                headers=response.request.headers,
                body=json.dumps(data),
                callback=self.parse,
                dont_filter=True,
                meta={'data': data}
            )


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished
