from pathlib import Path
from typing import Iterable

from natsort import natsorted
from tqdm import tqdm

from cltk.core import CLTKException
from cltk.morphology.lat import CollatinusDecliner

from .dictionary import LewisShortDictionary
from .macronization import KeelineKirbyWordlist
from .mappings import WORDLIST_RAW_PATHS, WORDLIST_PROCESSED_PATHS
from .vulgate import VulgateProperNameDataset
from .wiktionary import WiktionaryInflectionDataset
from .types import NamedWordlist


def collect_wordlist(wordlist_name: str) -> Iterable[str]:
    wordlist_filepath: Path = get_raw_wordlist_filepath(wordlist_name)

    match wordlist_name:
        case NamedWordlist.LEWIS_SHORT:
            dictionary: LewisShortDictionary = LewisShortDictionary(wordlist_filepath)
            headwords: list[str] = dictionary.get_headwords()
            wordlist: list[str] = gather_collatinus_inflections(headwords)
            wordlist = natsorted(wordlist)
        case NamedWordlist.KEELINE_KIRBY:
            macronization_dataset: KeelineKirbyWordlist = KeelineKirbyWordlist(wordlist_filepath)
            wordlist: list[str] = natsorted(list(macronization_dataset))
        case NamedWordlist.WIKTIONARY:
            inflection_dataset: WiktionaryInflectionDataset = WiktionaryInflectionDataset(wordlist_filepath)
            wordlist: list[str] = natsorted(list(inflection_dataset))
        case NamedWordlist.VULGATE:
            vulgate_dataset: VulgateProperNameDataset = VulgateProperNameDataset(wordlist_filepath)
            wordlist: list[str] = natsorted(list(vulgate_dataset))
        case _:
            raise ValueError(f"The wordlist <{wordlist_name}> is not recognized.")

    return wordlist


def gather_collatinus_inflections(words: list[str]) -> list[str]:
    decliner: CollatinusDecliner = CollatinusDecliner()
    inflections: list[str] = []
    errors: list[str] = []
    for word in tqdm(words, desc="Inflecting Words"):
        try:
            tagged_inflections: list[tuple[str, str]] = decliner.decline(word)
            word_inflections, _ = list(zip(*tagged_inflections))
            filtered_inflections = \
                [inflection for inflection in word_inflections if inflection != "" and not inflection.isspace()]
        except CLTKException:
            inflections.append(word)
        except KeyError:
            errors.append(word)
        else:
            inflections.extend(set(filtered_inflections))
    else:
        print(f"CLTK Key Errors: <{errors}>")

    return inflections


def get_raw_wordlist_filepath(wordlist_name: str) -> Path:
    try:
        wordlist_filepath: Path = WORDLIST_RAW_PATHS[wordlist_name]
    except KeyError:
        raise ValueError(f"A path was not found for the wordlist <{wordlist_name}>.")

    return wordlist_filepath


def get_processed_wordlist_filepath(wordlist_name: str) -> Path:
    try:
        wordlist_filepath: Path = WORDLIST_PROCESSED_PATHS[wordlist_name]
    except KeyError:
        raise ValueError(f"A path was not found for the wordlist <{wordlist_name}>.")

    return wordlist_filepath
