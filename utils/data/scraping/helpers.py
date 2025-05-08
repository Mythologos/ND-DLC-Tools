from pathlib import Path

from .filters import FILTER_MAPPING
from .types import FilterFunction


def get_filter(filter_name: str) -> FilterFunction:
    try:
        filter_function: FilterFunction = FILTER_MAPPING[filter_name]
    except KeyError:
        raise ValueError(f"The filter <{filter_name}> is not recognized. Please try again.")
    return filter_function


def get_urls(input_filepath: Path) -> list[str]:
    wiktionary_urls: list[str] = []
    with input_filepath.open(encoding="utf-8", mode="r") as input_file:
        for line in input_file:
            if not line.startswith("#"):
                wiktionary_urls.append(line.strip())
        else:
            if not wiktionary_urls:
                raise ValueError(f"The given filepath, <{input_filepath}>, contains no URLs. "
                                 f"Please supply a file with URLs.")

    return wiktionary_urls
