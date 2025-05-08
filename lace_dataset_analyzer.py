from argparse import ArgumentParser, Namespace
from math import ceil, sqrt
from multiprocessing import cpu_count
from pathlib import Path
from typing import Callable

from utils.common.messages import LaceMessage, LaceAnalyzerMessage
from utils.data.lace import collect_tsv_file_rows, get_lace_text_fields, LaceDatasetType, LaceMap
from utils.statistics import get_lace_metric, LaceMetric


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--dataset-type", type=LaceDatasetType, required=True, help=LaceMessage.DATASET_TYPE)
    parser.add_argument(
        "--metrics", type=LaceMetric, nargs="+", default=list(LaceMetric), help=LaceAnalyzerMessage.METRICS
    )
    parser.add_argument("--processes", type=int, default=ceil(sqrt(cpu_count())), help=LaceAnalyzerMessage.PROCESSES)
    parser.add_argument("--tsv-directory", type=Path, required=True, help=LaceAnalyzerMessage.TSV_DIRECTORY)
    args: Namespace = parser.parse_args()

    field_names: list[str] = get_lace_text_fields(args.dataset_type)
    tsv_rows_map: dict[str, LaceMap] = collect_tsv_file_rows(args.tsv_directory, field_names)

    lace_metrics: list[tuple[LaceMetric, Callable]] = get_lace_metric(args.dataset_type, args.metrics)
    for (metric, function) in lace_metrics:
        if metric in (LaceMetric.LACE_CHARACTER_ERROR_RATE, LaceMetric.OCR_CHARACTER_ERROR_RATE):
            function(tsv_rows_map, processes=args.processes)
        else:
            function(tsv_rows_map)
