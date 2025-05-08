from pathlib import Path
from re import compile, Pattern

CORPUS_PATH_BASE: Path = Path("data", "corpora")
MULTISPACE_REGEX: Pattern = compile(r"[\s]{2,}")
NAMESPACE_MAPPING: dict[str, str] = {"": "http://www.tei-c.org/ns/1.0"}
XML_SUFFIX: str = ".xml"
