from re import fullmatch
from typing import Sequence

from utils.data.loaders.common import WordFilter

from .constants import LATIN_ALPHABET_PATTERN


HEADWORD_FILTERS: dict[str, WordFilter] = {
    "non-latin": lambda word: fullmatch(LATIN_ALPHABET_PATTERN, word) is None,
}

INFLECTION_FILTERS: dict[str, WordFilter] = {
    "affix": lambda word: word.startswith("-") or word.endswith("-"),
    "multiword": lambda word: " " in word,
    "reconstruction": lambda word: word.startswith("*") or (word.startswith("(") and word.endswith(")"))
}

DEFAULT_HEADWORD_FILTERS: Sequence[WordFilter] = tuple([value for value in HEADWORD_FILTERS.values()])
DEFAULT_INFLECTION_FILTERS: Sequence[WordFilter] = tuple([value for value in INFLECTION_FILTERS.values()])
