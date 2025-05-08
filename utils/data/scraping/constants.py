from typing import Any

# URLs:
BASE_URL: str = "https://en.wiktionary.org"

# XPaths:
LIST_XPATH_QUERY: str = "//div[@id='mw-pages']/div[@class='mw-content-ltr']/descendant::a"
NEXT_PAGE_XPATH_QUERY: str = "//div[@id='mw-pages']/child::a[contains(text(), 'next page')]/@href"

# Spider Settings:
DEFAULT_SPIDER_SETTINGS: dict[str, Any] = {
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "CONCURRENT_REQUESTS": 8,
    "DOWNLOAD_DELAY": .5,
    "DOWNLOAD_TIMEOUT": 600,
    "AUTOTHROTTLE_ENABLED": True,
    "AUTOTHROTTLE_TARGET_CONCURRENCY": 0.75
}
