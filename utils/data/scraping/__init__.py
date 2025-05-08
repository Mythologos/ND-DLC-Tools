from typing import Sequence

from .constants import *
from .enumerations import FilterType
from .filters import FILTER_MAPPING
from .helpers import get_filter, get_urls
from .spider import WiktionarySpider
from .types import FilterFunction

DEFAULT_FILTERS: Sequence[str] = \
    (FilterType.AFFIX, FilterType.MULTIWORD, FilterType.RECONSTRUCTION, FilterType.NONALPHABETIC)
