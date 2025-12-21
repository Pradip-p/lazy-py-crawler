<div align="center">
    <h1>🚀 Crawlio Intelligence</h1>
    <p><strong>Institutional-grade market intelligence powered by AI.</strong></p>
    <p>Transform the web into a structured source of truth for strategic decision-making.</p>
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

**Crawlio Intelligence** is a premium market intelligence platform designed to democratize access to institutional-grade data. Built on a robust foundation of **Scrapy** and **Playwright**, it transforms complex web ecosystems into actionable strategic insights with precision and scale.

## ✨ Key Features

- **⚡ Strategic Automation**: Deploy production-ready intelligence pipelines in minutes, not days.
- **🧠 AI-Powered Synthesis**: Directly extract actionable insights without the overhead of manual data mapping.
- **🎮 Dynamic Intelligence**: seamless handling of JavaScript-heavy environments (React, Vue, Angular) via advanced Playwright integration.
- **💾 Unified Data Ecosystem**: Automated delivery to **MongoDB, PostgreSQL, CSV, JSON, and Google Sheets**.
- **�️ Enterprise Reliability**: Built-in anti-detection, proxy rotation, and robust infrastructure scaling.

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

### 2. Basic Intelligence Node (Static Sites)

Create a file named `my_agent.py`:

```python
import scrapy
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from scrapy.crawler import CrawlerProcess

class MyAgent(LazyBaseCrawler):
    name = "my_agent"

    def start_requests(self):
        yield scrapy.Request("https://example.com", self.parse)

    def parse(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "url": response.url
        }

process = CrawlerProcess()
process.crawl(MyAgent)
process.start()
```

### 3. Dynamic Intelligence Node (JavaScript-heavy Sites)

With Playwright integration, handling dynamic environments is trivial:

```python
class DynamicAgent(LazyBaseCrawler):
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

Crawlio Intelligence includes specialized modules for high-fidelity data extraction:

```python
from lazy_crawler.lib.extractors import find_emails, find_phone_numbers

def parse(self, response):
    text = response.text
    emails = find_emails(text)
    phones = find_phone_numbers(text)
    yield {"emails": emails, "phones": phones}
```

## 💾 Data Management

Crawlio Intelligence supports institutional-grade storage backends.

### 1. 🍃 MongoDB Integration

Directly store your intelligence datasets into MongoDB for high-performance retrieval.

**Configuration in `.env`**:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=crawlio_intelligence_db
```

**Usage**:
Enable the pipeline in your settings:

```python
ITEM_PIPELINES = {
    "lazy_crawler.crawler.pipelines.MongoPipeline": 400,
}
```

### 2. 📊 Google Sheets Delivery

Stream market data directly to shared Google Sheets for collaborative strategy.

**Configuration in `.env`**:

```env
GOOGLE_SHEETS_CREDS_FILE=creds.json
GOOGLE_SHEETS_SPREADSHEET_NAME=MarketIntelligenceData
GOOGLE_SHEETS_WORKSHEET_NAME=LatestInsights
```

## 🚀 Live Intelligence Dashboard

Crawlio Intelligence comes with a premium, decision-centric dashboard to visualize your data streams in real-time.

**Start the Dashboard**:

```bash
uv run python -m lazy_crawler.api.main
```

Then visit:

- **Dashboard UI**: `http://localhost:8000/`
- **Market Intelligence API Docs**: `http://localhost:8000/docs`

### Features

- 📊 **Real-time Visualization**: Monitor data ingress as it happens.
- 🎨 **Premium Aesthetics**: modern Slack-like design with high-fidelity UI components.
- 🔍 **Global Intelligence Search**: Quickly filter through millions of records with ease.
- 📄 **Advanced Data Exploration**: Efficiently navigate large datasets via intuitive pagination.

## 🐳 Enterprise Deployment (Docker)

Deploy Crawlio Intelligence at scale using our production-grade Docker orchestration, including Nginx for secure, high-performance delivery.

### Quick Deployment

```bash
# Automated deployment with health checks
./deploy.sh
```

### Manual Orchestration

#### 1. Initialize Stack

```bash
docker compose up --build -d
```

#### 2. Access the Platform

- **Dashboard UI**: `http://localhost/` (via Nginx)
- **API Documentation**: `http://localhost/docs`
- **Health Monitoring**: `http://localhost/health`

#### 3. Execute Intelligence Agents

Run your agents directly within the containerized environment:

```bash
docker compose exec app scrapy crawl my_agent
```

### Production Security (SSL)

```bash
# Automated SSL setup with Let's Encrypt
./setup-ssl.sh your-domain.com
```

See [QUICKSTART.md](QUICKSTART.md) for quick commands and [README_NGINX.md](README_NGINX.md) for detailed configuration.

## 🛠️ Customization

Crawlio Intelligence is highly extensible, allowing you to override core logic to suit specific strategic needs while maintaining high-performance defaults.

## 🤝 Collaboration

We welcome contributions to the advancement of market intelligence! Please check our [Contributing Guide](CONTRIBUTING.md).

## 📜 License

Crawlio Intelligence is licensed under the [MIT License](LICENSE).

---

<div align="center">
    Created with ❤️ by <a href="https://github.com/pradip-p">Pradip P.</a>
</div>
