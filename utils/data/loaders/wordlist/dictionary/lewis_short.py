from os import PathLike
from typing import Any, Sequence
# noinspection PyPep8Naming
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from tqdm import tqdm

from utils.data.loaders.common import WordFilter, WordPreprocessor

from .constants import CORRECTION_ELEMENT_XPATH, ENTRY_ELEMENT_XPATH, ORTHOGRAPHY_ELEMENT_XPATH
from .filters import DEFAULT_FILTERS
from .preprocessors import DEFAULT_PREPROCESSORS


class LewisShortDictionary:
    def __init__(self, input_filepath: PathLike, **kwargs):
        self.entries: dict[str, set[int]] = self._load_entries(input_filepath, **kwargs)

    def __iter__(self):
        return iter(self.entries.items())

    def __getitem__(self, key: str) -> set[int]:
        return self.entries[key]

    def __len__(self):
        return len(self.entries)

    def get_headwords(self):
        return list(self.entries.keys())

    def get_entries(self, key: int) -> list[str]:
        entries: list[str] = []
        for orthography, entry_numbers in self.entries.items():
            if key in entry_numbers:
                entries.append(orthography)

        return entries

    @staticmethod
    def _load_entries(input_filepath: PathLike, filters: Sequence[WordFilter] = DEFAULT_FILTERS,
                      preprocessors: Sequence[WordPreprocessor] = DEFAULT_PREPROCESSORS) -> dict[str, set[int]]:
        entries: dict[str, set[int]] = {}
        tree: ElementTree = ET.parse(input_filepath)
        root: Element = tree.getroot()

        entry_elements: list[Element] = root.findall(ENTRY_ELEMENT_XPATH)
        tqdm_kwargs: dict[str, Any] = {"total": len(entry_elements), "desc": "Loading Lewis-Short Entries"}
        for entry_index, entry in tqdm(enumerate(entry_elements, start=1), **tqdm_kwargs):
            orthography_elements: list[Element] = entry.findall(ORTHOGRAPHY_ELEMENT_XPATH)
            for orthography in orthography_elements:
                if orthography.text is not None:
                    current_orthography: str = orthography.text.strip()
                else:
                    correction: Element = orthography.find(CORRECTION_ELEMENT_XPATH)
                    if correction.text is not None:
                        current_orthography: str = correction.text.strip()
                    else:
                        raise ValueError(f"Entry {entry_index} has no orthography for at least "
                                         f"one of its orthographic entries.")

                if any([filter_function(current_orthography) for filter_function in filters]):
                    continue
                else:
                    for preprocessor in preprocessors:
                        current_orthography: str = preprocessor(current_orthography)

                if current_orthography is not None:
                    if current_orthography not in entries:
                        entries[current_orthography] = set()
                    entries[current_orthography].add(entry_index)

        return entries
