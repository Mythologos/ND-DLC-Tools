from argparse import ArgumentParser, Namespace

from pathlib import Path

from utils.common import LaceMessage, LaceTrainingCheckerMessage
from utils.data.lace import get_duplicates, get_lace_text_fields, LaceDatasetType, LaceMap, load_rows


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--output-filepath", type=Path, default=None, help=LaceTrainingCheckerMessage.OUTPUT_FILEPATH)
    parser.add_argument("--tsv-filepath", type=Path, required=True, help=LaceMessage.OCR_TSV_FILEPATH)
    args: Namespace = parser.parse_args()

    tsv_rows: LaceMap = load_rows(args.tsv_filepath, text_fields=get_lace_text_fields(LaceDatasetType.OCR))
    discovered_duplicates: list[dict[str, str]] = get_duplicates(tsv_rows)
    if args.output_filepath is not None:
        with args.output_filepath.open(encoding="utf-8", mode="w+") as output_file:
            for duplicate in discovered_duplicates:
                output_file.write("\t".join(list(duplicate.values())) + "\n")
    else:
        for duplicate in discovered_duplicates:
            print(duplicate)
