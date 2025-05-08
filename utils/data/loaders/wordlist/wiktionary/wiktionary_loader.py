from pathlib import Path
from typing import Sequence

from utils.data.loaders.common import WordFilter, WordPreprocessor

from .constants import COMMENT_HEADING
from .filters import DEFAULT_HEADWORD_FILTERS, DEFAULT_INFLECTION_FILTERS
from .preprocessors import DEFAULT_PREPROCESSORS


class WiktionaryInflectionDataset:
    def __init__(self, wiktionary_path: Path, **kwargs):
        self.inflections: list[str] = self._load_inflections(wiktionary_path, **kwargs)

    def __len__(self):
        return len(self.inflections)

    def __iter__(self):
        return iter(self.inflections)

    def __getitem__(self, index: int) -> str:
        return self.inflections[index]

    def _load_inflections(self, wiktionary_path: Path,
                          headword_filters: Sequence[WordFilter] = DEFAULT_HEADWORD_FILTERS,
                          inflection_filters: Sequence[WordFilter] = DEFAULT_INFLECTION_FILTERS,
                          preprocessors: Sequence[WordPreprocessor] = DEFAULT_PREPROCESSORS) -> list[str]:
        inflections: set[str] = set()

        if wiktionary_path.is_file():
            filepaths: list[Path] = [wiktionary_path]
        else:   # wiktionary_path.is_dir()
            filepaths: list[Path] = list(wiktionary_path.iterdir())

        for filepath in filepaths:
            if any([filter_function(filepath.stem) for filter_function in headword_filters]):
                continue
            else:
                file_inflections: list[str] = \
                    self._load_file_inflections(filepath, filters=inflection_filters, preprocessors=preprocessors)
                inflections.update(file_inflections)

        inflections: list[str] = list(inflections)
        return inflections

    @staticmethod
    def _load_file_inflections(wiktionary_filepath: Path, filters: Sequence[WordFilter],
                               preprocessors: Sequence[WordPreprocessor]) -> list[str]:
        file_inflections: set[str] = set()
        with wiktionary_filepath.open(encoding="utf-8", mode="r") as inflection_file:
            for line in inflection_file:
                if line.startswith(COMMENT_HEADING):
                    continue
                else:
                    line = line.strip()
                    if any([filter_function(line) for filter_function in filters]):
                        continue
                    else:
                        for preprocessor in preprocessors:
                            line = preprocessor(line)

                        file_inflections.add(line)

        file_inflections: list[str] = list(file_inflections)
        return file_inflections
