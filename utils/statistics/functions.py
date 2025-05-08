from functools import partial
from multiprocessing import Pool
from typing import Any

from tqdm import tqdm

from utils.algorithms.edit_distance import calculate_minimum_edit_distance, levenshtein_cost_function
from utils.data.lace import LaceMap
from utils.data.tokenization import LatinWordTokenizer


def get_character_counts(rows_map: dict[str, LaceMap]):
    character_counts: dict[str, int] = {
        key: sum([len(row["post_ocr_text"]) - row["post_ocr_text"].count(" ") for row in rows])
        for key, rows in tqdm(rows_map.items(), desc="Counting Characters")
    }

    print("Displaying Character Counts:")
    for (filename, count) in character_counts.items():
        print(f"\t- {filename}: {count}")
    else:
        print(f"Total: {sum([value for value in character_counts.values()])}")


def get_word_counts(rows_map: dict[str, LaceMap]):
    tokenizer: LatinWordTokenizer = LatinWordTokenizer()
    tokenizer_kwargs: dict[str, list[str]] = {"enclitics": [], "enclitics_exceptions": [], "replacements": []}
    word_counts: dict[str, int] = {
        key: sum([len(tokenizer.tokenize(row["post_ocr_text"], **tokenizer_kwargs)) for row in rows])
        for key, rows in tqdm(rows_map.items(), desc="Counting Words")
    }

    print("Displaying Word Counts:")
    for (filename, count) in word_counts.items():
        print(f"\t- {filename}: {count}")
    else:
        print(f"Total: {sum([value for value in word_counts.values()])}")


def get_line_counts(rows_map: dict[str, LaceMap]):
    line_counts: dict[str, int] = {key: len(rows) for key, rows in tqdm(rows_map.items(), desc="Counting Lines")}

    print("Displaying Line Counts:")
    for (filename, count) in line_counts.items():
        print(f"\t- {filename}: {count}")
    else:
        print(f"Total: {sum([value for value in line_counts.values()])}")


def get_page_counts(rows_map: dict[str, LaceMap]):
    page_counts: dict[str, int] = {
        key: len(set([row["path"] for row in rows]))
        for key, rows in tqdm(rows_map.items(), desc="Counting Pages")
    }

    print("Displaying Page Counts:")
    for (filename, count) in page_counts.items():
        print(f"\t- {filename}: {count}")
    else:
        print(f"Total: {sum([value for value in page_counts.values()])}")


def get_character_error_rate(rows_map: dict[str, LaceMap], processes: int, prediction_key: str, gold_key: str):
    character_errors: dict[str, list[float]] = {key: [] for key in rows_map.keys()}

    static_kwargs: dict[str, Any] = {"cost": levenshtein_cost_function}
    edit_distance_partial = partial(calculate_minimum_edit_distance, **static_kwargs)
    for key, rows in tqdm(rows_map.items(), desc="Counting Errors (by File)"):
        pairs: list[tuple[str, str]] = [(row[prediction_key], row[gold_key]) for row in rows]
        with Pool(processes=processes) as pool:
            with tqdm(total=len(pairs), desc=f"Counting Errors (File <{key}>)") as completion_tracker:
                for starmap_result in pool.starmap(edit_distance_partial, pairs):
                    edit_distance, *_ = starmap_result
                    character_errors[key].append(edit_distance)
                    completion_tracker.update()

    expected_max_character_errors: dict[str, list[int]] = {
        key: [len(row[gold_key]) for row in rows]
        for key, rows in tqdm(rows_map.items(), desc="Counting Expected Maximum Errors")
    }

    print(f"Displaying Character Error Rates (<{prediction_key}> vs. <{gold_key}>):")
    for (filename, error_counts) in character_errors.items():
        print(f"\t- {filename}: "
              f"\n\t\t- Errors: {sum(error_counts)}"
              f"\n\t\t- Expected Maximum: {sum(expected_max_character_errors[filename])}"
              f"\n\t\t- Character Error Rate: {sum(error_counts) / sum(expected_max_character_errors[filename]):.4f}")
    else:
        total_character_errors: int = sum([sum(value) for value in character_errors.values()])
        total_expected_max_character_errors: int = sum([sum(value) for value in expected_max_character_errors.values()])
        print(f"Total: {total_character_errors / total_expected_max_character_errors:.4f}")
