from functools import partial
from typing import Callable

from .constants import LaceMetric
from .functions import get_character_counts, get_character_error_rate, get_line_counts, get_page_counts, get_word_counts

from utils.data.lace import LaceDatasetType


LACE_METRIC_MAPPING: dict[LaceMetric, Callable] = {
    LaceMetric.CHARACTER_COUNT: get_character_counts,
    LaceMetric.LINE_COUNT: get_line_counts,
    LaceMetric.LACE_CHARACTER_ERROR_RATE:
        partial(get_character_error_rate, prediction_key="lace_text", gold_key="post_ocr_text"),
    LaceMetric.OCR_CHARACTER_ERROR_RATE:
        partial(get_character_error_rate, prediction_key="ocr_text", gold_key="post_ocr_text"),
    LaceMetric.PAGE_COUNT: get_page_counts,
    LaceMetric.WORD_COUNT: get_word_counts
}


DATASET_METRIC_MAPPING: dict[LaceDatasetType, list[LaceMetric]] = {
    LaceDatasetType.OCR: [
        LaceMetric.CHARACTER_COUNT,
        LaceMetric.LINE_COUNT,
        LaceMetric.PAGE_COUNT,
        LaceMetric.WORD_COUNT
    ],
    LaceDatasetType.POST_OCR: list(LaceMetric)
}
