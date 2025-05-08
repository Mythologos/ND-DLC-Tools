from pathlib import Path
from re import compile, fullmatch, Match, Pattern
from string import punctuation
from typing import Optional


class VulgateProperNameDataset:
    TESSERAE_LINE_PATTERN: Pattern = compile(r"(?P<annotation><.+>)\s(?P<text>.+);?\n?")

    def __init__(self, input_filepath: Path):
        self.names: list[str] = self._load_names(input_filepath)

    def __iter__(self):
        return iter(self.names)

    def __getitem__(self, index: int) -> str:
        return self.names[index]

    def __len__(self):
        return len(self.names)

    def _load_names(self, input_path: Path) -> list[str]:
        if input_path.is_dir():
            names: set[str] = set()
            for filepath in input_path.iterdir():
                file_names: set[str] = self._load_file_names(filepath)
                names.update(file_names)
        elif input_path.is_file():
            names: set[str] = self._load_file_names(input_path)
        else:
            raise ValueError(f"The input path, <{input_path}>, is not a valid file or directory path.")

        names: list[str] = list(names)
        return names

    def _load_file_names(self, input_filepath: Path) -> set[str]:
        names: set[str] = set()
        with input_filepath.open(encoding="utf-8", mode="r") as input_file:
            for line in input_file:
                matched_line: Optional[Match] = fullmatch(self.TESSERAE_LINE_PATTERN, line)
                if matched_line is not None:
                    line_text: str = matched_line.group("text")
                    line_words: list[str] = line_text.strip().split()
                    for word in line_words:
                        word = word.strip(punctuation)
                        if word.istitle() is True:   # Only proper nouns should be capitalized.
                            names.add(word)
                else:
                    raise ValueError(f"The line <{line}> does not match the expected pattern.")

        return names
