from pathlib import Path

from .types import NamedWordlist

WORDLIST_BASE_PATH: Path = Path("data", "wordlist")

WORDLIST_RAW_PATHS: dict[str, Path] = {
    NamedWordlist.KEELINE_KIRBY: WORDLIST_BASE_PATH / "keeline-kirby" / "macrons.tsv",
    NamedWordlist.LEWIS_SHORT: WORDLIST_BASE_PATH / "lewis-short" / "lat.ls.perseus-eng2.xml",
    NamedWordlist.VULGATE: WORDLIST_BASE_PATH / "vulgate",
    NamedWordlist.WIKTIONARY: WORDLIST_BASE_PATH / "wiktionary" / "parses"
}

WORDLIST_PROCESSED_PATHS: dict[str, Path] = {
    NamedWordlist.KEELINE_KIRBY: WORDLIST_BASE_PATH / "keeline-kirby" / "keeline-kirby.txt",
    NamedWordlist.LEWIS_SHORT: WORDLIST_BASE_PATH / "lewis-short" / "lewis-short.txt",
    NamedWordlist.VULGATE: WORDLIST_BASE_PATH / "vulgate" / "vulgate.txt",
    NamedWordlist.WIKTIONARY: WORDLIST_BASE_PATH / "wiktionary" / "wiktionary.txt",
}
