from pathlib import Path
from re import split
from string import punctuation
from typing import Iterable

from cltk.alphabet.lat import LigatureReplacer
from spellchecker import SpellChecker
from tqdm import tqdm

from utils.data.tokenization.latin_word_tokenizer import LatinWordTokenizer

from .constants import PUNCTUATION_PATTERN
from utils.data.loaders.corpus import get_corpus_dataset, CorpusDatasetSubclass
from utils.data.loaders.wordlist import get_processed_wordlist_filepath, NamedWordlist


def construct_frequency_mapping(chosen_wordlists: list[str]) -> dict[str, int]:
    complete_wordlist: set[str] = set()
    for wordlist_name in tqdm(chosen_wordlists, desc="Gathering Wordlists"):
        input_filepath: Path = get_processed_wordlist_filepath(wordlist_name)
        if wordlist_name in list(NamedWordlist):
            wordlist: list[str] = [line.strip().lower() for line in input_filepath.open(encoding="utf-8", mode="r")]
            complete_wordlist.update(wordlist)
        else:
            raise ValueError(f"The wordlist <{wordlist_name}> is not supported.")

    # By default, we assume that if a word exists in one of our wordlists, it must occur somewhere.
    frequential_wordlist: dict[str, int] = {word: 1 for word in complete_wordlist}
    return frequential_wordlist


def gather_corpora(input_corpora: list[str]) -> list[CorpusDatasetSubclass]:
    corpora: list[CorpusDatasetSubclass] = []
    for corpus_name in tqdm(input_corpora, desc="Gathering Input Corpora"):
        corpus_path, corpus_class = get_corpus_dataset(corpus_name)
        corpus: CorpusDatasetSubclass = corpus_class(corpus_path, sentence_tokenization=True)
        corpora.append(corpus)

    return corpora


def gather_frequencies(wordlist: dict[str, int], corpora: list[CorpusDatasetSubclass]):
    tokenizer: LatinWordTokenizer = LatinWordTokenizer()
    for corpus in tqdm(corpora, desc="Processing Corpus Tokens"):
        for sentence in tqdm(corpus, desc="Handling Corpus Sentences"):
            words: list[str] = tokenizer.tokenize(sentence.sentence)
            for word in words:
                if word.lower() in wordlist:
                    wordlist[word.lower()] += 1


def load_sentences(text_filepath: Path) -> list[str]:
    base_sentences: list[str] = []
    with text_filepath.open(encoding="utf-8", mode="r") as text_file:
        for line in text_file:
            base_sentence: str = line.strip()
            base_sentences.append(base_sentence)

    return base_sentences


def tokenize_sentence(sentence: str) -> list[str]:
    tokenizer: LatinWordTokenizer = LatinWordTokenizer()
    ligature_replacer: LigatureReplacer = LigatureReplacer()

    tokenizer_kwargs: dict[str, list[str]] = {"enclitics": [], "enclitics_exceptions": [], "replacements": []}
    base_tokenized_sentence: list[str] = tokenizer.tokenize(sentence, **tokenizer_kwargs)

    tokenized_sentence: list[str] = []
    for base_token in base_tokenized_sentence:
        tokens: list[str] = split(PUNCTUATION_PATTERN, base_token)
        postprocessed_tokens: list[str] = [ligature_replacer.replace(token) for token in tokens]
        tokenized_sentence.extend(postprocessed_tokens)

    return tokenized_sentence


def spellcheck_sentences(spellchecker: SpellChecker, base_sentences: list[str], output_filepath: Path):
    with output_filepath.open(encoding="utf-8", mode="w+") as output_file:
        for sentence_index, base_sentence in tqdm(enumerate(base_sentences), desc="Checking Sentences"):
            tokens: Iterable[str] = spellchecker.split_words(base_sentence)
            unknown_tokens: set[str] = spellchecker.unknown(tokens)
            for unknown_token in unknown_tokens:
                if unknown_token in punctuation:
                    continue
                else:
                    if is_encliticized(unknown_token, spellchecker):
                        continue
                    else:
                        output_file.write(f"Token {unknown_token} in Sentence {sentence_index} was not known.\n")


def is_encliticized(word: str, spellchecker: SpellChecker) -> bool:
    encliticized_bool: bool = False
    for enclitic in LatinWordTokenizer.ENCLITICS:
        if len(spellchecker.unknown([word[:-1 * len(enclitic)]])) == 0:
            encliticized_bool = True

    return encliticized_bool
