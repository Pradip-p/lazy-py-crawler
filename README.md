<div align="center">
    <h1>Lazy Py Crawler</h1>
    <p>Simplify your web scraping tasks with ease.</p>
    <p>Scrape smarter, not harder.</p>
    <a href="https://github.com/pradip-p/lazy-crawler/releases">
        <img src="https://img.shields.io/github/v/release/pradip-p/lazy-crawler?logo=github" alt="Release Version" />
    </a>
</div>

</br>

<!-- prettier-ignore-start -->
<div align="center">

| **CI/CD** | | N/A|
| :--- | :--- | :--- |
| **Tech Stack** | | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Scrapy](https://img.shields.io/badge/Scrapy-100000?style=for-the-badge&logo=scrapy&logoColor=white) |
| **Code Style** | | [![PEP8 Style](https://img.shields.io/badge/code%20style-pep8-blue)](https://www.python.org/dev/peps/pep-0008/) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com) |
| **Other Info** | | [![docs](https://img.shields.io/badge/docs-available-brightgreen)](https://pradip-p.github.io/lazy-crawler/) [![license](https://img.shields.io/github/license/pradip-p/lazy-crawler.svg)](https://github.com/pradip-p/lazy-crawler/blob/main/LICENSE.md) |

</div>

---

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

**Lazy Crawler** is a Python package that simplifies web scraping tasks. Built upon the powerful Scrapy framework, it provides additional utilities and features for easier data extraction. With Lazy Crawler, you can quickly set up and deploy web scraping projects, saving time and effort.

## Features

- **Simplified Setup**: Streamlines the process of setting up and configuring web scraping projects.
- **Predefined Library**: Comes with a library of functions and utilities for common web scraping tasks, reducing the need for manual coding.
- **Easy Data Extraction**: Simplifies extracting and processing data from websites, allowing you to focus on analysis and insights.
- **Versatile Utilities**: Includes tools for finding emails, numbers, mentions, hashtags, links, and more.
- **Flexible Data Storage**: Provides a pipeline for storing data in various formats such as CSV, JSON, Google Sheets, and Excel.

## Getting Started

To get started with Lazy Crawler:

1. **Install**: Ensure Python and Scrapy are installed. Then, install Lazy Crawler via pip:
   ```
   pip install lazy-crawler
   ```
2. **Create a Project**: Create a Python file for your project (e.g., `scrapy_example.py`) and start coding.

### Example Usage

Here's an example of how to use Lazy Crawler in a project:

```python
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent

class LazyCrawler(LazyBaseCrawler):
    name = "example"
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 32,
    }
    headers = get_user_agent('random')

    def start_requests(self):
        url = 'https://example.com'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        title = response.xpath('//title/text()').get()
        yield {'Title': title}

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess()
process.crawl(LazyCrawler)
process.start()
```

## Further Resources

For more information and examples of how to use Lazy Crawler, see the [project documentation](https://pradip-p.github.io/lazy-crawler/).

## Credits

Lazy Crawler was created by Pradip P.

## License

Lazy Crawler is released under the [MIT License](https://github.com/pradip-p/lazy-crawler/blob/main/LICENSE.md).