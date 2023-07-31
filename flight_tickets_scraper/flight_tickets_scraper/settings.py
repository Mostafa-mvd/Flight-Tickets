# Scrapy settings for flight_tickets_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import pathlib

BASE_PATH = pathlib.Path(__file__).parent.parent.parent

BOT_NAME = "flight_tickets_scraper"

SPIDER_MODULES = ["flight_tickets_scraper.spiders"]
NEWSPIDER_MODULE = "flight_tickets_scraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "TCH=8ktqu1bpqr7u74p2tb5kchrnls; _gcl_au=1.1.849212697.1690208445; _ga=GA1.2.1776701195.1690208446; _gid=GA1.2.2026748026.1690208446; GoReferer=Q2FrZQ%3D%3D.ZmZiOTljNGYzNzQ3NjI1MGRmYWVkYzA5ZTk4ZmExYWUzMzBmMzI0MzNmYzExNWNmYzQ1NTgxMzIwNmI1Y2RiZm%2FM%2FFOkD4jQWXnN8aWOIamkxmDFlfNLQsSJ1TEMiAr5rrwF10W6JUmjVjLZVW4RBLdf0T1a5iDpK5IFUKOV5puSILH36ld4ZUhr8KP7csFHvRsa%2FCeSqAPqe7MU9pYxK0vjMGJcq0sbVioImH%2FeHYSJJqoDse6ZJhuFUMXqb9VPGpFufY%2BN4UD%2BK9yx%2FJOiOCiAIungjXbNkomZY2cdLt0QV7cDsUTmJVdFW4ornQK005zt%2F42TrQMjD5s6HOpWaMeifvuFITe9vXcQJzONuYPegFGweJnLjuukpM3wyy28XU69o0qrW5cLnC1pDCt%2BAzMO%2F%2BIeolk%2BIaIdeL0tiWjICR658eCz%2BHXCjb13jx37tC1qLdspCFcdag%2BlfwKc6w%3D%3D; _ga_R30088QYSJ=GS1.2.1690484040.21.0.1690484040.60.0.0",
    "DNT": "1",
    "Origin": "https://www.tcharter.ir",
    "Referer": "https://www.tcharter.ir/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "'Not/A)Brand';v='99', 'Google Chrome';v='115', 'Chromium';v='115'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "'Linux'",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "flight_tickets_scraper.middlewares.FlightTicketsScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'flight_tickets_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#   "flight_tickets_scraper.pipelines.FlightTicketsScraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 6
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Sources ---

SOURCES = {
    "airport_city_codes_path": BASE_PATH.joinpath("source", "airport_city_codes.json"),
    "rotating_proxy_list_path": BASE_PATH.joinpath("source", "proxies.txt"),
}

#Development ---

DEVELOPMENT = {
    "docker_compose_yml_file_path": BASE_PATH.joinpath("development", "docker-compose.yml"),
}

# FAKE_USER_AGENT settings ---

SCRAPEOPS_API_KEY = '4f35d66f-c691-462b-aed5-d403df96367f'

SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True


# Proxy Settings ---

# ROTATING_PROXY_LIST = []

ROTATING_PROXY_LIST_PATH = SOURCES["rotating_proxy_list_path"]

ROTATING_PROXY_PAGE_RETRY_TIMES = 10
