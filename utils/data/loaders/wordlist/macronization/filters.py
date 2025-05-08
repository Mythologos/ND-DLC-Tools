from typing import Sequence

from utils.data.loaders.common import WordFilter


FILTERS: dict[str, WordFilter] = {
    "prefixed": lambda word: "#" in word,
}

DEFAULT_FILTERS: Sequence[WordFilter] = tuple([value for value in FILTERS.values()])
