from argparse import ArgumentParser, BooleanOptionalAction, Namespace
from pathlib import Path

from utils.common import LaceMessage, LaceTrainingPostprocessorMessage
from utils.data.lace import alter_image_paths, filter_bookmarks, filter_xml_artifacts, fix_smart_quotes, \
    get_lace_text_fields, LaceDatasetType, LaceMap, load_rows, save_rows


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--current-tsv-filepath", type=Path, required=True, help=LaceTrainingPostprocessorMessage.CURRENT_TSV_FILEPATH
    )
    parser.add_argument("--dataset-type", type=LaceDatasetType, required=True, help=LaceMessage.DATASET_TYPE)
    parser.add_argument(
        "--filter-bookmarks", action=BooleanOptionalAction, default=False,
        help=LaceTrainingPostprocessorMessage.FILTER_BOOKMARKS
    )
    parser.add_argument(
        "--filter-xml-artifacts", action=BooleanOptionalAction, default=False,
        help=LaceTrainingPostprocessorMessage.FILTER_XML_ARTIFACTS
    )
    parser.add_argument(
        "--fix-smart-quotes", action=BooleanOptionalAction, default=False,
        help=LaceTrainingPostprocessorMessage.FIX_SMART_QUOTES
    )
    parser.add_argument(
        "--new-image-directory", type=Path, default=None,
        help=LaceTrainingPostprocessorMessage.NEW_IMAGE_DIRECTORY
    )
    parser.add_argument(
        "--new-tsv-filepath", type=Path, required=True, help=LaceTrainingPostprocessorMessage.NEW_TSV_FILEPATH
    )
    args: Namespace = parser.parse_args()

    lace_text_fields: list[str] = get_lace_text_fields(args.dataset_type)

    # We load the data...
    tsv_rows: LaceMap = load_rows(args.current_tsv_filepath, lace_text_fields)

    # We apply different optional filters:
    if args.new_image_directory is not None:
        alter_image_paths(tsv_rows, args.new_image_directory)

    if args.filter_bookmarks is True:
        filter_bookmarks(tsv_rows)

    if args.filter_xml_artifacts is True:
        filter_xml_artifacts(tsv_rows, text_keys=lace_text_fields)

    if args.fix_smart_quotes is True:
        fix_smart_quotes(tsv_rows, text_keys=["post_ocr_text"])

    # We save the data...
    save_rows(tsv_rows, args.new_tsv_filepath)
