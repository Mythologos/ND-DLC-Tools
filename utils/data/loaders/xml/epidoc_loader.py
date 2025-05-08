from itertools import chain
from pathlib import Path
from re import compile, Pattern, sub
from typing import Iterator, Optional

from lxml import etree
from lxml.etree import ElementTree, Element

from .types import EpidocDocument


class EpidocCorpus:
    # XPath Constants:
    PARAGRAPH_PATH: str = ".//p"
    HEAD_PATH: str = ".//titleStmt"

    # Namespace Constant:
    NAMESPACE_MAP: dict[Optional[str], str] = {None: "http://www.tei-c.org/ns/1.0"}

    # Regular Expression Pattern Constants:
    LINE_BREAK_PATTERN: Pattern = compile(r"-\s+")
    WHITESPACE_PATTERN: Pattern = compile(r"(\s{2,})|([\t\n\r\f\v])")

    # Other Replacements:
    REPLACEMENT_TABLE: dict[str, str] = {
        "‘": "'",
        "’": "'",
        "«": "\"",
        "»": "\"",
    }

    def __init__(self, dataset_paths: list[Path]):
        self.data: list[EpidocDocument] = self._load_data(dataset_paths)

    def __getitem__(self, index: int):
        return self.data[index]

    def __iter__(self) -> Iterator[EpidocDocument]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def _load_data(self, paths: list[Path]) -> list[EpidocDocument]:
        texts: list[EpidocDocument] = []
        for path in paths:
            tree: ElementTree = etree.parse(path)
            root: Element = tree.getroot()

            metadata: dict[str, str] = {}

            metadata_head: Element = root.find(self.HEAD_PATH, namespaces=self.NAMESPACE_MAP)
            metadata["title"] = metadata_head.find("title", namespaces=self.NAMESPACE_MAP).text
            metadata["author"] = metadata_head.find("author", namespaces=self.NAMESPACE_MAP).text

            body: Element = root.find("text", namespaces=self.NAMESPACE_MAP)
            paragraphs: list[Element] = list(body.iterfind(self.PARAGRAPH_PATH, namespaces=self.NAMESPACE_MAP))

            segments: list[str] = list(chain.from_iterable([list(paragraph.itertext()) for paragraph in paragraphs]))

            # We postprocess by ensuring clean whitespace and joining page breaks.
            text: str = ""
            for segment in segments:
                cleaned_segment: str = sub(self.WHITESPACE_PATTERN, " ", segment.strip())
                if text.endswith("-"):
                    text = f"{text.rstrip('-')}{cleaned_segment}"
                else:
                    text = f"{text} {cleaned_segment}"

            for key, value in self.REPLACEMENT_TABLE.items():
                text = text.replace(key, value)

            text: EpidocDocument = EpidocDocument(metadata, text)
            texts.append(text)

        return texts
