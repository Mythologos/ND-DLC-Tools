from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Sequence

from scrapy.crawler import CrawlerProcess

from utils.common import WiktionaryScraperMessage
from utils.data.scraping import DEFAULT_SPIDER_SETTINGS, DEFAULT_FILTERS, FilterFunction, FilterType, \
    get_filter, get_urls, WiktionarySpider


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--filters", type=str, nargs='+', choices=[getattr(item, "value") for item in FilterType],
        default=DEFAULT_FILTERS, help=WiktionaryScraperMessage.FILTERS
    )
    parser.add_argument("--input-filepath", type=Path, required=True, help=WiktionaryScraperMessage.INPUT_FILEPATH)
    parser.add_argument("--output-directory", type=Path, required=True, help=WiktionaryScraperMessage.OUTPUT_DIRECTORY)
    args: Namespace = parser.parse_args()

    # We verify inputs.
    if not args.input_filepath.is_file():
        raise ValueError(f"The given input filepath, <{args.input_filepath}>, is not a valid filepath.")
    elif not args.output_directory.is_dir():
        raise ValueError(f"The given output filepath, <{args.output_directory}>, is not a valid directory path.")

    filter_functions: Sequence[FilterFunction] = tuple([get_filter(filter_name) for filter_name in args.filters])

    # Read in URL(s) from file; for now, the code assumes that all lines in files will be valid URLs,
    #   save those that begin with Python's comment character ("#").
    urls: list[str] = get_urls(args.input_filepath)

    # Submit URLs to Spider for scraping, along with any desired options.
    # Also, set desired options for scraping in order to supply it to the scraper.
    process: CrawlerProcess = CrawlerProcess(settings=DEFAULT_SPIDER_SETTINGS)
    process.crawl(WiktionarySpider, start_urls=urls, output_location=args.output_directory, filters=filter_functions)
    process.start()
