#!/usr/bin/python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser, Namespace, BooleanOptionalAction
from csv import DictReader, QUOTE_NONE
from pathlib import Path
from sys import exit

from PIL import Image

from utils.common import LaceMessage, LaceOCRGeneratorMessage
from utils.data.lace import DEFAULT_LACE_FIELDS, get_lace_text_fields, LaceDatasetType


# This code was modified from this script by Bruce Robertson:
# https://github.com/brobertson/Lace2-tools/blob/master/training_set_from_tsv.py


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate OCR training set from Lace TSV output.")
    parser.add_argument(
        "--image-format", type=str, choices=["jpg", "png", "tif"], default="png",
        help=LaceOCRGeneratorMessage.IMAGE_FORMAT
    )
    parser.add_argument(
        "--output-directory", type=Path, required=True, help=LaceOCRGeneratorMessage.OUTPUT_DIRECTORY
    )
    parser.add_argument(
        "--tsv-filepath", type=Path, required=True, help=LaceMessage.OCR_TSV_FILEPATH
    )
    parser.add_argument(
        "-v", "--verbose", action=BooleanOptionalAction, default=False, help=LaceOCRGeneratorMessage.VERBOSE
    )
    args: Namespace = parser.parse_args()

    # Check that the TSV files actually exist:
    if not args.tsv_filepath.is_file():
        print(f"TSV file <{args.tsv_filepath}> is not a valid filepath. Exiting ...")
        exit(1)

    # Create the output directory if it doesn't exist:
    try:
        if not args.output_directory.exists():
            args.output_directory.mkdir(exist_ok=True)
    except Exception as e:
        print(f"Error on creating output directory <{args.output_directory}>: {e}"
              f"\n\tExiting ...")
        exit(1)

    if args.verbose:
        print("Image Directory:", args.image_directory)
        print("Output Directory:", args.output_directory)
        print("TSV File:", args.tsv_filepath)

    with open(args.tsv_filepath, newline="", encoding="utf-8") as tsv_file:
        tsv_reader: DictReader = DictReader(
            tsv_file, fieldnames=DEFAULT_LACE_FIELDS + get_lace_text_fields(LaceDatasetType.OCR), delimiter="\t",
            quotechar="|", quoting=QUOTE_NONE
        )

        correction_map: dict[str, list[tuple[str, str]]] = {}
        for row in tsv_reader:
            if correction_map.get(row["path"]) is None:
                correction_map[row["path"]] = []

            correction: tuple[str, str] = (row["bounds"], row["post_ocr_text"])
            correction_map[row["path"]].append(correction)

    if args.verbose:
        print(correction_map)

    output_counter: int = 0
    for (path, corrections) in correction_map.items():
        image_path: Path = Path(path)
        print(f"Processing Image at: <{path}>")
        page: Image = Image.open(image_path)

        for (bounds, text) in corrections:
            base_filename: str = f"{image_path.stem}_{output_counter}"
            gt_filepath: Path = args.output_directory / f"{base_filename}.gt.txt"
            image_output_filepath: Path = args.output_directory / f"{base_filename}.png"

            # Output the text GT file:
            with gt_filepath.open(encoding="utf-8", mode="w+") as gt_file:
                gt_file.write(text)

            # Try to find the original image in the directories given:
            try:
                bounding_box: list[int] = [int(bound) for bound in bounds.strip().split()]
            except Exception as e:
                print(f"Error on parsing bbox <{bounds}>:"
                      f"\n\t{str(e)}"
                      f"\n\tExiting ...")
                exit(1)

            assert len(bounding_box) == 4
            bounding_box: tuple[int, int, int, int]

            cropped_page: Image = page.crop(bounding_box)
            cropped_page.save(image_output_filepath)
            output_counter += 1
