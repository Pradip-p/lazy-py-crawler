<div align="center">
    <h1>🚀 Lazy Py Crawler</h1>
    <p><strong>The ultimate Swiss Army knife for modern web scraping.</strong></p>
    <p>Scrape smarter, not harder. Built on Scrapy, enhanced for developers.</p>
    <a href="https://github.com/pradip-p/lazy-crawler/releases">
        <img src="https://img.shields.io/github/v/release/pradip-p/lazy-crawler?logo=github" alt="Release Version" />
    </a>
</div>

<br/>

<div align="center">

| **Tech Stack** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Scrapy](https://img.shields.io/badge/Scrapy-100000?style=for-the-badge&logo=scrapy&logoColor=white) ![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white) |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Code Style** | [![PEP8 Style](https://img.shields.io/badge/code%20style-pep8-blue)](https://www.python.org/dev/peps/pep-0008/) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com)                                                                         |
| **Status**     | [![docs](https://img.shields.io/badge/docs-available-brightgreen)](https://pradip-p.github.io/lazy-crawler/) [![license](https://img.shields.io/github/license/pradip-p/lazy-crawler.svg)](https://github.com/pradip-p/lazy-crawler/blob/main/LICENSE.md)                                                                     |

</div>

---

**Lazy Crawler** is a high-level Python framework designed to eliminate the boilerplate of web scraping. Built on top of the industry-standard **Scrapy**, it adds powerful utilities, pre-configured pipelines, and now **Playwright integration** to handle even the most complex JavaScript-heavy websites with ease.

## ✨ Key Features

- **⚡ Instant Setup**: Skip the tedious configuration. Get a production-ready crawler running in minutes.
- **🎮 Dynamic Content**: Built-in support for **Playwright** to scrape React, Vue, and Angular applications seamlessly.
- **🛠️ Utility Toolbox**: Ready-to-use helpers for extracting emails, phone numbers, social media handles, and more.
- **💾 Battery-Included Storage**: Automated pipelines for exporting data directly to **CSV, JSON, Excel, and Google Sheets**.
- **🕵️ Anti-Detection**: Pre-integrated user-agent rotation and proxy handling out of the box.

## 🚀 Quick Start

### 1. Installation

This project is managed with **uv**. To get started, ensure you have [uv](https://github.com/astral-sh/uv) installed.

To install the project and its dependencies:

```bash
uv pip install .
```

For development:

```bash
uv init
uv pip install -e .
```

> [!NOTE]
> Don't forget to run `playwright install` after installation to set up the browser drivers.

### 2. Basic Scraper (Static Sites)

Create a file named `my_crawler.py`:

```python
import scrapy
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from scrapy.crawler import CrawlerProcess

class MyCrawler(LazyBaseCrawler):
    name = "my_crawler"

    def start_requests(self):
        yield scrapy.Request("https://example.com", self.parse)

    def parse(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "url": response.url
        }

process = CrawlerProcess()
process.crawl(MyCrawler)
process.start()
```

### 3. Dynamic Scraper (JavaScript-heavy Sites)

With Playwright integration, scraping dynamic sites is trivial:

```python
class DynamicCrawler(LazyBaseCrawler):
    name = "dynamic"

    def start_requests(self):
        yield scrapy.Request(
            "https://dynamic-site.com",
            meta={"playwright": True},
            callback=self.parse
        )

    def parse(self, response):
        # response now contains the fully rendered HTML
        data = response.css(".rendered-content::text").get()
        yield {"content": data}
```

## 📚 Advanced Usage

Lazy Crawler includes specialized libraries for advanced tasks:

```python
from lazy_crawler.lib.extractors import find_emails, find_phone_numbers

def parse(self, response):
    text = response.text
    emails = find_emails(text)
    phones = find_phone_numbers(text)
    yield {"emails": emails, "phones": phones}
```

## 💾 Data Storage

Lazy Crawler supports multiple storage backends.

### 1. 🍃 MongoDB Storage

Directly store your scraped data into a MongoDB collection named after your spider.

**Configuration in `.env`**:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=my_scraping_db
```

**Usage**:
Enable the pipeline in your `settings.py` or spider's `custom_settings`:

```python
ITEM_PIPELINES = {
    "lazy_crawler.crawler.pipelines.MongoPipeline": 400,
}
```

### 2. 📊 Google Sheets

Stream data directly to a Google Sheet.

**Configuration in `.env`**:

```env
GOOGLE_SHEETS_CREDS_FILE=creds.json
GOOGLE_SHEETS_SPREADSHEET_NAME=MyScrapeData
GOOGLE_SHEETS_WORKSHEET_NAME=Sheet1
```

## 🚀 Live Data Dashboard

Lazy Crawler comes with a built-in, premium dashboard to visualize your scraped data in real-time.

**Start the Dashboard**:

```bash
uv run python -m lazy_crawler.api.main
```

Then visit:

- **Dashboard UI**: `http://localhost:8000/`
- **Interactive API Docs**: `http://localhost:8000/docs`

### Features

- 📊 **Real-time Visualization**: See data as it arrives in MongoDB.
- 🎨 **Modern Design**: Glassmorphism theme with dark mode support.
- 🔍 **Live Search**: Quickly filter through thousands of records.
- 📄 **Pagination**: Efficiently browse through large datasets.

## 🐳 Running with Docker

The easiest way to run Lazy Crawler with a database and dashboard is using **Docker Compose**. The setup now includes **Nginx** as a reverse proxy for production-ready deployment.

### Quick Deployment

```bash
# Automated deployment with health checks
./deploy.sh
```

### Manual Deployment

#### 1. Launch everything

Run the following command in the root directory:

```bash
docker compose up --build -d
```

#### 2. Access the Application

Once the containers are up, visit:

- **Dashboard UI**: `http://localhost/` (via Nginx)
- **API Documentation**: `http://localhost/docs`
- **Health Check**: `http://localhost/health`
- **MongoDB**: `localhost:27017`

#### 3. Run a Crawler in Docker

You can execute your spiders inside the container:

```bash
docker compose exec app scrapy crawl my_spider
```

### Production Deployment with SSL

For production deployment with HTTPS:

```bash
# Automated SSL setup with Let's Encrypt
./setup-ssl.sh your-domain.com
```

See [QUICKSTART.md](QUICKSTART.md) for quick commands and [README_NGINX.md](README_NGINX.md) for detailed Nginx configuration.

## 🛠️ Configuration

Lazy Crawler reads from standard Scrapy settings but provides defaults that work for 90% of cases. You can easily override them in your spider's `custom_settings`.

## 🤝 Contributing

We welcome contributions! Please check out our [Contributing Guide](CONTRIBUTING.md) to get started.

## 📜 License

Lazy Crawler is licensed under the [MIT License](LICENSE).

---

<div align="center">
    Created with ❤️ by <a href="https://github.com/pradip-p">Pradip P.</a>
</div>
