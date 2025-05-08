from argparse import ArgumentParser, Namespace
from pathlib import Path

from utils.common import WiktionaryParserMessage
from utils.data.parsing import parse_files


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--input-directory", type=Path, required=True, help=WiktionaryParserMessage.INPUT_DIRECTORY)
    parser.add_argument("--output-directory", type=Path, required=True, help=WiktionaryParserMessage.OUTPUT_DIRECTORY)
    args: Namespace = parser.parse_args()

    if not args.input_directory.is_dir():
        raise ValueError(f"The value <{args.input_directory}> is not a valid directory.")
    elif not args.output_directory.is_dir():
        raise ValueError(f"The value <{args.output_directory}> is not a valid directory.")

    parse_files(args.input_directory, args.output_directory)
