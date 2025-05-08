from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, Tag, PageElement
from tqdm import tqdm

from .constants import LATIN_HEADER_ATTRIBUTES, LATIN_HEADWORD_ATTRIBUTES, MAIN_DIV_ATTRIBUTES


def parse_files(input_directory: Path, output_directory: Path):
    for input_filepath in tqdm(input_directory.iterdir(), desc="Parsing Wiktionary Files"):
        filename: str = input_filepath.stem
        output_filepath: Path = output_directory / (filename + ".txt")
        parse_file(input_filepath, output_filepath)


def parse_file(input_filepath: Path, output_filepath: Path):
    with input_filepath.open(encoding="utf-8", mode="r") as input_file:
        html_tree: BeautifulSoup = BeautifulSoup(input_file, features="lxml")

    main_div: Tag = html_tree.find("div", MAIN_DIV_ATTRIBUTES)
    bounds: dict[str, Optional[Tag]] = gather_bounds(input_filepath, main_div)
    language_elements: list[PageElement] = get_language_elements(bounds)
    inflections: dict[str, list[str]] = get_inflections(language_elements)

    with output_filepath.open(encoding="utf-8", mode="w+") as output_file:
        for headword_number, (headword, inflections) in enumerate(inflections.items(), start=1):
            output_file.write(f"### Headword {headword_number}:\n")
            if len(inflections) == 0:
                output_file.write(f"{headword}\n")
            else:
                for inflection in inflections:
                    output_file.write(f"{inflection}\n")


def gather_bounds(input_filepath: Path, main_div: Tag) -> dict[str, Optional[Tag]]:
    language_headers: list[Tag] = main_div.find_all("h2", recursive=True)
    bounds: dict[str, Optional[Tag]] = {"upper": None, "lower": None}
    if len(language_headers) == 0:
        raise ValueError(f"No languages headers found for <{input_filepath}>.")
    else:   # len(language_headers) >= 1:
        for header in language_headers:
            if header.find("span", LATIN_HEADER_ATTRIBUTES, recursive=True) is not None:
                bounds["upper"] = header
                bounds["lower"] = header.find_next_sibling("h2")
                break

    return bounds


def get_language_elements(bounds: dict[str, Optional[Tag]]) -> list[PageElement]:
    following_elements: list[PageElement] = list(bounds["upper"].next_siblings)
    if bounds["lower"] is not None:
        lower_bound_index: int = following_elements.index(bounds["lower"])
        language_elements: list[PageElement] = following_elements[:lower_bound_index]
    else:
        language_elements = following_elements

    return language_elements


def get_inflections(language_elements: list[PageElement]) -> dict[str, list[str]]:
    last_headword: Optional[str] = None
    paradigms: dict[str, list[str]] = {}
    for element in language_elements:
        if has_headword(element):
            element: Tag

            headword: str = get_headword(element)
            paradigms[headword] = []
            last_headword = headword
        elif has_inflection_table(element):
            element: Tag

            table_words: list[str] = get_inflected_forms(element)
            if last_headword is not None:
                paradigms[last_headword] = table_words
            else:
                raise ValueError("Paradigm retrieved without corresponding headword.")

    return paradigms


def has_headword(element: PageElement) -> bool:
    # We check whether the element is a Tag; if it is, we check if it has the attributes to contain a Latin headword.
    return isinstance(element, Tag) and element.find("strong", LATIN_HEADWORD_ATTRIBUTES) is not None


def get_headword(element: Tag) -> str:
    headword: str = element.find("strong", LATIN_HEADWORD_ATTRIBUTES).get_text(strip=True)
    return headword


def has_inflection_table(element: PageElement) -> bool:
    inflection_table_bool: bool = False
    if isinstance(element, Tag):
        table_bool: bool = element.name == "table"
        inflection_table_bool: bool = element.attrs.get("class", None) is not None and \
            "inflection-table" in element.attrs["class"]

        if table_bool and inflection_table_bool:
            inflection_table_bool = True

    return inflection_table_bool


def get_inflected_forms(element: Tag) -> list[str]:
    inflections: list[str] = []
    table_forms: list[Tag] = element.find_all("td")
    for form in table_forms:
        spans: list[PageElement] = form.findChildren("span")
        for form_span in spans:
            inflection: str = form_span.get_text(strip=True)
            inflections.append(inflection)

    return inflections
