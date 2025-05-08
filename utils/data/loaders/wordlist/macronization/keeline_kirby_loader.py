from pathlib import Path
from typing import Sequence

from utils.data.loaders.common import WordFilter
from utils.data.loaders.wordlist.macronization import DEFAULT_FILTERS


class KeelineKirbyWordlist:
    def __init__(self, macronization_path: Path, **kwargs):
        self.forms: list[str] = self._load_inflections(macronization_path, **kwargs)

    def __len__(self):
        return len(self.forms)

    def __iter__(self):
        return iter(self.forms)

    def __getitem__(self, index: int) -> str:
        return self.forms[index]

    @staticmethod
    def _load_inflections(macronization_path: Path, filters: Sequence[WordFilter] = DEFAULT_FILTERS) -> list[str]:
        inflections: set[str] = set()
        with macronization_path.open(encoding="utf-8", mode="r") as macronization_file:
            for line in macronization_file:
                form, tag, lemma, macronization = line.strip().split("\t")
                if any([filter_function(form) for filter_function in filters]):
                    continue

                if lemma.istitle():
                    form = form.capitalize()   # assures consistency in casing

                inflections.add(form)

        inflections: list[str] = list(inflections)
        return inflections
