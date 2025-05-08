from pathlib import Path
from string import punctuation

from cltk.tokenizers.lat.lat import LatinPunktSentenceTokenizer
from tqdm import tqdm

from utils.data.tokenization.latin_word_tokenizer import LatinWordTokenizer

from .epidoc_loader import EpidocCorpus


def load_corpus(directory: Path) -> EpidocCorpus:
    files: list[Path] = list(directory.glob("**/urn.*.xml"))
    corpus: EpidocCorpus = EpidocCorpus(files)
    return corpus


def get_sentence_counts(dataset: EpidocCorpus, tokenizer: LatinPunktSentenceTokenizer) -> dict[str, int]:
    sentence_counts: dict[str, int] = {}
    for document in tqdm(dataset, desc="Gathering Sentence Counts per Text"):
        key: str = f"{document.metadata['title']} ({document.metadata['author']})"
        sentence_counts[key] = len(tokenizer.tokenize(document.text))

    sentence_counts["total"] = sum(sentence_counts.values())
    return sentence_counts


def get_word_counts(dataset: EpidocCorpus, tokenizer: LatinWordTokenizer) -> dict[str, int]:
    word_counts: dict[str, int] = {}

    for document in tqdm(dataset, desc="Gathering Word Counts per Text"):
        key: str = f"{document.metadata['title']} ({document.metadata['author']})"
        word_counts[key] = 0
        tokens: list[str] = tokenizer.tokenize(document.text, enclitics=tuple())
        true_words: list[str] = list(filter(lambda word: word not in punctuation, tokens))
        word_counts[key] += len(true_words)

    word_counts["total"] = sum(word_counts.values())
    return word_counts
