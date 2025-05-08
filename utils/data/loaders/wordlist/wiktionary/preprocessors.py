from typing import Sequence

from utils.data.loaders.common import WordPreprocessor
from utils.data.loaders.common.helpers import map_vowels

PREPROCESSORS: dict[str, WordPreprocessor] = {
    "punctuation": lambda word: word.strip("!?"),
    "vowels": map_vowels,
}

DEFAULT_PREPROCESSORS: Sequence[WordPreprocessor] = tuple([value for value in PREPROCESSORS.values()])
