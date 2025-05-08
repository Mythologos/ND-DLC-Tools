from typing import Sequence

from utils.data.loaders.common import WordFilter

from .constants import ERRONEOUS_FORMS, ENTRY_MARKERS, PARTIAL_FORMS


FILTERS: dict[str, WordFilter] = {
    "affix": lambda word: word.startswith("-") or word.endswith("-"),
    "error": lambda word: word in ERRONEOUS_FORMS,
    "marker": lambda word: word in ENTRY_MARKERS,
    "multiword": lambda word: " " in word,
    "partial": lambda word: word in PARTIAL_FORMS
}

DEFAULT_FILTERS: Sequence[WordFilter] = tuple([value for value in FILTERS.values()])
