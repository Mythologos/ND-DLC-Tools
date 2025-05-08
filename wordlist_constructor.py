from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Iterable

from tqdm import tqdm

from utils.common import WordlistConstructorMessage
from utils.data.loaders.wordlist import collect_wordlist, get_processed_wordlist_filepath, NamedWordlist


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--wordlist", choices=[getattr(item, "value") for item in NamedWordlist], required=True,
        help=WordlistConstructorMessage.WORDLIST
    )
    args: Namespace = parser.parse_args()

    wordlist: Iterable[str] = collect_wordlist(args.wordlist)
    output_filepath: Path = get_processed_wordlist_filepath(args.wordlist)
    with open(output_filepath, encoding="utf-8", mode="w+") as output_file:
        for item in tqdm(wordlist, desc="Writing Words"):
            output_file.write(f"{item}\n")
