from argparse import ArgumentParser, Namespace
from json import dump
from pathlib import Path

from utils.common import GeneralMessage, SpellingMapBuilderMessage
from utils.data.loaders.corpus import CorpusDatasetSubclass, NamedCorpus
from utils.data.loaders.wordlist import NamedWordlist
from utils.data.spellchecking import construct_frequency_mapping, gather_corpora, gather_frequencies


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--corpora", type=str, nargs="*", choices=[getattr(item, "value") for item in NamedCorpus],
        help=SpellingMapBuilderMessage.CORPORA, default=[]
    )
    parser.add_argument("--output-filepath", type=Path, required=True, help=GeneralMessage.MAP_FILEPATH)
    parser.add_argument(
        "--wordlists", type=str, nargs="+", choices=[getattr(item, "value") for item in NamedWordlist],
        help=SpellingMapBuilderMessage.WORDLISTS
    )
    args: Namespace = parser.parse_args()

    frequency_mapping: dict[str, int] = construct_frequency_mapping(args.wordlists)
    corpora: list[CorpusDatasetSubclass] = gather_corpora(args.corpora)
    gather_frequencies(frequency_mapping, corpora)

    with args.output_filepath.open(mode="w+", encoding="utf-8") as output_file:
        dump(frequency_mapping, output_file)
