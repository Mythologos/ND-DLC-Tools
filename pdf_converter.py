from argparse import ArgumentParser, BooleanOptionalAction, Namespace
from pathlib import Path
from typing import Any

from pdf2image import convert_from_path
from tqdm import tqdm

from utils.common import PDFConverterMessage
from utils.data.ocr import gather_input_paths, gather_static_output_paths

if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--cropbox", action=BooleanOptionalAction, default=False, help=PDFConverterMessage.CROPBOX)
    parser.add_argument("--dpi", type=int, default=200, help=PDFConverterMessage.DPI)
    parser.add_argument("--grayscale", action=BooleanOptionalAction, default=False, help=PDFConverterMessage.GRAYSCALE)
    parser.add_argument("--input-path", type=Path, required=True, help=PDFConverterMessage.INPUT_PATH)
    parser.add_argument("--output-directory", type=Path, required=True, help=PDFConverterMessage.OUTPUT_DIRECTORY)
    parser.add_argument("--output-format", type=str, default="png", help=PDFConverterMessage.OUTPUT_FORMAT)
    parser.add_argument("--output-prefix", type=str, default="page-", help=PDFConverterMessage.OUTPUT_PREFIX)
    parser.add_argument(
        "--pdftocairo", action=BooleanOptionalAction, default=False, help=PDFConverterMessage.PDF_TO_CAIRO
    )
    parser.add_argument(
        "--strict-errors", action=BooleanOptionalAction, default=False, help=PDFConverterMessage.STRICT_ERRORS
    )
    args: Namespace = parser.parse_args()

    input_paths: list[Path] = gather_input_paths(args.input_path, filetype="pdf")
    output_paths: list[Path] = gather_static_output_paths(args.output_directory, input_paths)

    conversion_kwargs: dict[str, Any] = {
        "dpi": args.dpi,
        "fmt": args.output_format,
        "grayscale": args.grayscale,
        "output_file": args.output_prefix,
        "strict": args.strict_errors,
        "use_cropbox": args.cropbox,
        "use_pdftocairo": args.pdftocairo
    }
    for i in tqdm(range(0, len(input_paths)), desc="Converting PDFs to Images"):
        output_paths[i].mkdir(exist_ok=True)
        convert_from_path(input_paths[i], output_folder=output_paths[i], **conversion_kwargs)
