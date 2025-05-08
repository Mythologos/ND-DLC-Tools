from pathlib import Path
from typing import Callable


def gather_input_paths(input_path: Path, filetype: str) -> list[Path]:
    if input_path.is_dir():
        input_paths: list[Path] = [path for path in input_path.glob(f"**/*.{filetype}")]
    elif input_path.is_file():
        input_paths: list[Path] = [input_path]
    else:
        raise ValueError(f"The path <{input_path}> is not a file or directory.")

    return input_paths


def gather_static_output_paths(output_path: Path, input_paths: list[Path]) -> list[Path]:
    if output_path.is_dir():
        output_filepaths: list[Path] = []
        for input_path in input_paths:
            output_filepath: Path = output_path / input_path.stem
            output_filepaths.append(output_filepath)
    else:
        raise ValueError(f"The path <{output_path}> is not a directory.")

    return output_filepaths


def gather_dynamic_output_paths(output_path: Path, input_paths: list[Path]) -> list[Path]:
    if output_path.is_dir():
        output_paths: list[Path] = []
        for new_input_path in input_paths:
            output_directory: Path = output_path / new_input_path.parent.stem
            if not output_directory.exists():
                output_directory.mkdir()

            new_output_path: Path = output_directory / (new_input_path.stem + ".hocr")
            output_paths.append(new_output_path)
    else:
        raise ValueError(f"The path <{output_path}> is not a directory.")

    return output_paths


def produce_hocr(input_path: Path, output_path: Path, hocr_function: Callable[[str], bytes]):
    hocr_output: bytes = hocr_function(str(input_path))
    encoded_hocr_output: str = str(hocr_output, encoding="utf-8")
    with open(output_path, encoding="utf-8", mode="w+") as output_file:
        output_file.write(encoded_hocr_output)
