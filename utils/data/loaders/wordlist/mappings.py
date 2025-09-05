from pathlib import Path

from .types import NamedWordlist

WORDLIST_BASE_PATH: Path = Path("data", "wordlist")

WORDLIST_RAW_PATHS: dict[str, Path] = {
    NamedWordlist.KEELINE_KIRBY: WORDLIST_BASE_PATH / "keeline-kirby" / "input" / "macrons.tsv",
    NamedWordlist.LEWIS_SHORT: WORDLIST_BASE_PATH / "lewis-short" / "input" / "lat.ls.perseus-eng2.xml",
    NamedWordlist.VULGATE: WORDLIST_BASE_PATH / "input" / "vulgate",
    NamedWordlist.WIKTIONARY: WORDLIST_BASE_PATH / "wiktionary" / "input" / "parses"
}

WORDLIST_PROCESSED_PATHS: dict[str, Path] = {
    NamedWordlist.KEELINE_KIRBY: WORDLIST_BASE_PATH / "keeline-kirby" / "output" / "keeline-kirby.txt",
    NamedWordlist.LEWIS_SHORT: WORDLIST_BASE_PATH / "lewis-short" / "output" / "lewis-short.txt",
    NamedWordlist.VULGATE: WORDLIST_BASE_PATH / "vulgate" / "output" / "vulgate.txt",
    NamedWordlist.WIKTIONARY: WORDLIST_BASE_PATH / "wiktionary" / "output" / "wiktionary.txt",
}
