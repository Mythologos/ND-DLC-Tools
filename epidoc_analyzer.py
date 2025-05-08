from argparse import ArgumentParser, Namespace
from pathlib import Path

from cltk.tokenizers.lat.lat import LatinPunktSentenceTokenizer

from utils.common import EpiDocAnalyzerMessage
from utils.data.tokenization.latin_word_tokenizer import LatinWordTokenizer
from utils.data.loaders.xml import EpidocCorpus, get_sentence_counts, get_word_counts, load_corpus


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--input-directory", type=Path, required=True, help=EpiDocAnalyzerMessage.INPUT_DIRECTORY)
    args: Namespace = parser.parse_args()

    sentence_tokenizer: LatinPunktSentenceTokenizer = LatinPunktSentenceTokenizer(strict=True)
    word_tokenizer: LatinWordTokenizer = LatinWordTokenizer()

    epidoc_corpus: EpidocCorpus = load_corpus(args.input_directory)
    tei_results: dict[str, dict[str, int]] = {
        "Sentence Counts": get_sentence_counts(epidoc_corpus, sentence_tokenizer),
        "Word Counts": get_word_counts(epidoc_corpus, word_tokenizer)
    }

    for result_type, results in tei_results.items():
        result_string: str = f"{result_type}:"
        for key, count in results.items():
            result_string += f"\n\t- {key}: {count}"
        else:
            print(result_string + "\n")
