from csv import DictReader, QUOTE_NONE
from re import search, sub
from pathlib import Path

from .constants import BOOKMARK_SYMBOL, DEFAULT_LACE_FIELDS, LaceDatasetType, \
    LEFT_DUPLICATE_PATTERN, RIGHT_DUPLICATE_PATTERN, SMART_QUOTE_PATTERN
from .mappings import DATASET_TEXT_FIELDS
from .types import LaceMap


def get_duplicates(rows: LaceMap) -> LaceMap:
    duplicates: LaceMap = []
    for row_index, row in enumerate(rows):
        if search(LEFT_DUPLICATE_PATTERN, row["post_ocr_text"]) or \
                search(RIGHT_DUPLICATE_PATTERN, row["post_ocr_text"]):
            duplicates.append(row)

    return duplicates


def get_lace_text_fields(dataset_type: LaceDatasetType) -> list[str]:
    try:
        fields: list[str] = DATASET_TEXT_FIELDS.get(dataset_type)
    except KeyError:
        raise ValueError(f"The dataset of type <{dataset_type}> is not recognized.")

    return fields


def alter_image_paths(rows: LaceMap, new_image_directory: Path):
    for row in rows:
        original_image_path: Path = Path(row["path"])
        image_filename: str = original_image_path.name
        new_image_path: Path = new_image_directory / f"{image_filename}"
        row["path"] = str(new_image_path)


def filter_bookmarks(rows: LaceMap, text_keys: list[str] = ("post_ocr_text",)):
    for row in rows:
        for text_key in text_keys:
            row[text_key] = row[text_key].replace(BOOKMARK_SYMBOL, "")


def filter_xml_artifacts(rows: LaceMap, text_keys: list[str]):
    for row in rows:
        for text_key in text_keys:
            row[text_key] = row[text_key].replace("&amp;", "&")


def fix_smart_quotes(rows: LaceMap, text_keys: list[str]):
    for row in rows:
        for text_key in text_keys:
            row[text_key] = sub(SMART_QUOTE_PATTERN, "‘", row[text_key])


def load_rows(filepath: Path, text_fields: list[str]) -> LaceMap:
    with filepath.open(newline="", encoding="utf-8") as tsv_file:
        tsv_reader: DictReader = DictReader(
            tsv_file, fieldnames=DEFAULT_LACE_FIELDS + text_fields, delimiter="\t", quotechar="|",
            quoting=QUOTE_NONE
        )
        rows: LaceMap = [row for row in tsv_reader]

    return rows


def collect_tsv_file_rows(tsv_directory: Path, text_fields: list[str]) -> dict[str, LaceMap]:
    rows_map: dict[str, LaceMap] = {
        tsv_filepath.stem: load_rows(tsv_filepath, text_fields)
        for tsv_filepath in tsv_directory.glob("*.tsv")
    }
    return rows_map


def save_rows(rows: LaceMap, output_filepath: Path):
    with output_filepath.open(newline="", encoding="utf-8", mode="w+") as tsv_file:
        for row in rows:
            tsv_file.write("\t".join([value for value in row.values()]) + "\n")
