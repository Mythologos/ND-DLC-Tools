from typing import Sequence

from utils.data.loaders.common import map_vowels, WordPreprocessor

from .constants import MISCELLANEOUS_CHARACTERS


def remove_miscellany(word: str) -> str:
    for mark in MISCELLANEOUS_CHARACTERS:
        word = word.replace(mark, "").strip()

    return word


PREPROCESSORS: dict[str, WordPreprocessor] = {
    "miscellany": remove_miscellany,
    "segmentation": lambda word: word.replace("-", ""),
    "vowels": map_vowels,
}

DEFAULT_PREPROCESSORS: Sequence[WordPreprocessor] = tuple([value for value in PREPROCESSORS.values()])
