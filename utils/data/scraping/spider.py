from pathlib import Path
from typing import Sequence

from scrapy import Request, Spider
from scrapy.http import Response

from .constants import BASE_URL, LIST_XPATH_QUERY, NEXT_PAGE_XPATH_QUERY
from .filters import FilterFunction


class WiktionarySpider(Spider):
    SPIDER_NAME: str = "wiktionary-spider"
    FILENAME_TEMPLATE: str = "{0}.html"

    def __init__(self, start_urls: list[str], output_location: Path, filters: Sequence[FilterFunction], **kwargs):
        super(WiktionarySpider, self).__init__(name=self.SPIDER_NAME, start_urls=start_urls, kwargs=kwargs)
        self.output_location: Path = output_location
        self.filters = filters

    # This method scrapes the initial page to retrieve other webpages.
    # It can also proceed to other webpages of the same type.
    def parse(self, response: Response, **kwargs) -> Request:
        for selector in response.xpath(LIST_XPATH_QUERY):
            text: str = selector.xpath("text()").get()
            if any([filter_function(text) for filter_function in self.filters]):
                continue
            else:
                link: str = selector.attrib["href"]
                yield Request(f"{BASE_URL}{link}", self.parse_headword_page, cb_kwargs={"headword": text})
        else:
            next_page_link: str = response.xpath(NEXT_PAGE_XPATH_QUERY).get()
            if next_page_link:
                yield Request(f"{BASE_URL}/{next_page_link}", self.parse)

    def parse_headword_page(self, response: Response, **kwargs):
        filename: str = self.FILENAME_TEMPLATE.format(kwargs['headword'])
        headword_filepath: Path = self.output_location / filename
        headword_filepath.write_bytes(response.body)
