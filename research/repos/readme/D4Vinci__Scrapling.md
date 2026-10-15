Effortless Web Scraping for the Modern Web 

 Selection methods 
 &middot;
 Fetchers 
 &middot;
 Spiders 
 &middot;
 Proxy Rotation 
 &middot;
 CLI 
 &middot;
 MCP 

Scrapling is an adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl.

Its parser learns from website changes and automatically relocates your elements when pages update. Its fetchers bypass anti-bot systems like Cloudflare Turnstile out of the box. And its spider framework lets you scale up to concurrent, multi-session crawls with pause/resume, automatic proxy rotation, and a crawl speed that adapts to how fast each website responds and backs off when it starts blocking you - all in a few lines of Python. One library, zero compromises.

Blazing fast crawls with real-time stats and streaming. Built by Web Scrapers for Web Scrapers and regular users, there's something for everyone.

```python
from scrapling.fetchers import Fetcher, AsyncFetcher, StealthyFetcher, DynamicFetcher
StealthyFetcher.adaptive = True
p = StealthyFetcher.fetch('https://example.com', headless=True, network_idle=True) # Fetch website under the radar!
products = p.css('.product', auto_save=True) # Scrape data that survives website design changes!
products = p.css('.product', adaptive=True) # Later, if the website structure changes, pass `adaptive=True` to find them!
```
Or scale up to full crawls
```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
 name = "demo"
 start_urls = ["https://example.com/"]

 async def parse(self, response: Response):
 for item in response.css('.product'):
 yield {"title": item.css('h2::text').get()}

MySpider().start()
```

# Platinum Sponsors

 NodeMaven - The most efficient proxy provider for Web Scraping and Automation with the Highest Quality IP on the market. Use code SCRAPLING35 for 35% discount.

 Scrapling handles Cloudflare Turnstile. For enterprise-grade protection, 
 Hyper Solutions 
 provides API endpoints that generate valid antibot tokens for Akamai , DataDome , Kasada , and Incapsula . Simple API calls, no browser automation required. 

 Evomi 
 : residential proxies from $0.49/GB. Scraping browser with fully spoofed Chromium, residential IPs, auto CAPTCHA solving, and anti-bot bypass. 
 Scraper API for hassle-free results. MCP and N8N integrations are available. 

 TikHub.io provides 900+ stable APIs across 16+ platforms including TikTok, X, YouTube & Instagram, with 40M+ datasets. Also offers DISCOUNTED AI models - Claude, GPT, GEMINI & more up to 71% off.

 Read a full review of Scrapling on The Web Scraping Club (Nov 2025), the #1 newsletter dedicated to Web Scraping.

 Swiftproxy provides scalable residential proxies with 80M+ IPs across 195+ countries, delivering fast, reliable connections, automatic rotation, and strong anti-block performance. Free trial available.

 Byteful supplies ethical residential, mobile, ISP, and datacenter proxies, plus scraping and AI automation tools. Use code SCRAPLING10: 10% off residential proxies.

 ProxyLane : Reduce blocks and CAPTCHAs by 90%. 28M Premium Residential IPs for Heavy Web Scraping. 195 countries. City/ISP/ZIP targeting. Sticky/rotating sessions. Non-expiring traffic from $2/GB. Code SCRAPEANDTAKE : 25% off .

 LundProxy : Stop paying per GB. Unlimited residential traffic, 100M+ IPs, 190+ countries. Pay by bandwidth. Request a free 50 Mbps residential proxies trial.

 $1/GB at DataImpulse . Ethical first-party proxies. 90M+ IPs, 195+ countries. Residential, datacenter, mobile. Pay-as-you-go = no subscription. Traffic never expires.

 Do you want to show your ad here? Click [here](https://github.com/sponsors/D4Vinci/sponsorships?tier_id=586646) 
# Sponsors 

 Do you want to show your ad here? Click [here](https://github.com/sponsors/D4Vinci) and choose the tier that suits you! 

---

## Key Features

### Spiders - A Full Crawling Framework
- 🕷️ **Scrapy-like Spider API**: Define spiders with `start_urls`, async `parse` callbacks, and `Request`/`Response` objects.
- ⚡ **Concurrent Crawling**: Configurable concurrency limits, per-domain throttling, and download delays.
- 🔄 **Multi-Session Support**: Unified interface for HTTP requests, and stealthy headless browsers in a single spider - route requests to different sessions by ID.
- 💾 **Pause & Resume**: Checkpoint-based crawl persistence. Press Ctrl+C for a graceful shutdown; restart to resume from where you left off.
- 📡 **Streaming Mode**: Stream scraped items as they arrive via `async for item in spider.stream()` with real-time stats - ideal for UI, pipelines, and long-running crawls.
- 🛡️ **Blocked Request Detection**: Automatic detection and retry of blocked requests with customizable logic.
- 🚦 **AutoThrottle**: Stop guessing delays. The spider tunes the delay of each domain on its own from how fast the website responds, then doubles it (or waits what `Retry-After` asks) whenever the website starts blocking or rate-limiting you, and speeds back up once it stops.
- 🤖 **Robots.txt Compliance**: Optional `robots_txt_obey` flag that respects `Disallow`, `Crawl-delay`, and `Request-rate` directives with per-domain caching.
- 🧪 **Development Mode**: Cache responses to disk on the first run and replay them on subsequent runs - iterate on your `parse()` logic without re-hitting the target servers.
- 🧩 **Ready-made Spider Templates**: Skip the boilerplate with `CrawlSpider` for rule-based link following, `SitemapSpider` for sitemap/robots.txt-driven crawls, `XMLFeedSpider`/`CSVFeedSpider` for iterating XML/RSS and CSV feeds, and `ShopifySpider` to pull every product out of any Shopify store through its JSON API, one item per variant.
- 🔗 **Link Extraction**: A standalone `LinkExtractor` primitive with allow/deny patterns, domain filters, CSS/XPath scoping, extension filtering, and canonicalization - use it inside the templates or on its own.
- 📦 **Built-in Export**: Export results through hooks and your own pipeline or the built-in JSON/JSON