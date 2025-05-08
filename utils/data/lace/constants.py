from enum import Enum
from re import compile, Pattern

BOOKMARK_SYMBOL: str = "📖×"
DEFAULT_LACE_FIELDS: list[str] = ["path", "bounds"]

# Regular Expressions:
SMART_QUOTE_PATTERN: Pattern = compile(r"’(?=\w+)")
LEFT_DUPLICATE_PATTERN: Pattern[str] = compile(r"\s+(?P<duplicate>\S+)\s+\1")
RIGHT_DUPLICATE_PATTERN: Pattern[str] = compile(r"(?P<original>\S+)\s+\1\s+")


# Enumerations:
class LaceDatasetType(str, Enum):
    OCR: str = "ocr"
    POST_OCR: str = "post-ocr"
