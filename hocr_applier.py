from argparse import ArgumentParser, Namespace
from functools import partial
from math import ceil, sqrt
from multiprocessing import Pool
from os import cpu_count
from pathlib import Path
from typing import Any, Callable

from pytesseract import image_to_pdf_or_hocr
from tqdm import tqdm

from utils.common import hOCRApplierMessage
from utils.data.ocr import gather_input_paths, gather_dynamic_output_paths, produce_hocr


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--input-format", type=str, default="png", help=hOCRApplierMessage.INPUT_FORMAT)
    parser.add_argument("--input-path", type=Path, required=True, help=hOCRApplierMessage.INPUT_PATH)
    parser.add_argument("--languages", type=str, nargs="*", default=["lat", "grc"], help=hOCRApplierMessage.LANGUAGES)
    parser.add_argument("--output-directory", type=Path, required=True, help=hOCRApplierMessage.OUTPUT_DIRECTORY)
    args: Namespace = parser.parse_args()

    input_paths: list[Path] = gather_input_paths(args.input_path, filetype=args.input_format)
    output_paths: list[Path] = gather_dynamic_output_paths(args.output_directory, input_paths)

    hocr_kwargs: dict[str, Any] = {"extension": "hocr", "lang": "+".join(args.languages)}
    allotted_processes: int = ceil(sqrt(cpu_count()))
    hocr_pairs: list[tuple[str, str]] = list(zip(input_paths, output_paths))
    hocr_base_function: Callable[[str], bytes] = partial(image_to_pdf_or_hocr, **hocr_kwargs)
    hocr_output_function: Callable[[str, str, Callable], None] = partial(produce_hocr, hocr_function=hocr_base_function)
    with Pool(processes=allotted_processes) as pool:
        with tqdm(total=len(hocr_pairs), desc="Gathering hOCR for Images") as completion_tracker:
            for _ in pool.starmap(hocr_output_function, hocr_pairs):
                completion_tracker.update()
