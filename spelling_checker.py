from argparse import ArgumentParser, Namespace
from pathlib import Path

from spellchecker import SpellChecker

from utils.common import GeneralMessage, SpellingCheckerMessage
from utils.data.spellchecking.helpers import load_sentences, spellcheck_sentences, tokenize_sentence

if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--map-filepath", required=True, type=Path, help=GeneralMessage.MAP_FILEPATH)
    parser.add_argument("--minimum-distance", type=int, default=1, help=SpellingCheckerMessage.MINIMUM_DISTANCE)
    parser.add_argument("--input-filepath", required=True, type=Path, help=SpellingCheckerMessage.INPUT_FILEPATH)
    parser.add_argument("--output-filepath", required=True, type=Path, help=SpellingCheckerMessage.OUTPUT_FILEPATH)
    args: Namespace = parser.parse_args()

    spell_checker: SpellChecker = SpellChecker(
        language=None,
        local_dictionary=args.map_filepath,
        distance=args.minimum_distance,
        tokenizer=tokenize_sentence
    )

    sentences: list[str] = load_sentences(args.input_filepath)
    spellcheck_sentences(spell_checker, sentences, args.output_filepath)
