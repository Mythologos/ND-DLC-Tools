from enum import Enum


class LaceMetric(str, Enum):
    CHARACTER_COUNT: str = "character-count"
    LACE_CHARACTER_ERROR_RATE: str = "lace-cer"
    LINE_COUNT: str = "line-count"
    OCR_CHARACTER_ERROR_RATE: str = "original-cer"
    PAGE_COUNT: str = "page-count"
    WORD_COUNT: str = "word-count"
