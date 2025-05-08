from typing import Callable

from .constants import LaceMetric
from .functions import get_character_counts, get_character_error_rate, get_line_counts, get_page_counts, get_word_counts
from .mappings import DATASET_METRIC_MAPPING, LACE_METRIC_MAPPING

from utils.data.lace import LaceDatasetType


def get_lace_metric(dataset_type: LaceDatasetType, metric_names: list[LaceMetric]) -> list[tuple[LaceMetric, Callable]]:
    metric_functions: list[tuple[LaceMetric, Callable]] = []
    for name in metric_names:
        try:
            if name not in DATASET_METRIC_MAPPING[dataset_type]:
                raise ValueError(f"Metric <{name}> not applicable to <{dataset_type}> dataset.")

            metric_function: Callable = LACE_METRIC_MAPPING[name]
            metric_functions.append((name, metric_function))
        except KeyError:
            raise ValueError(f"The metric <{name}> is not recognized.")

    return metric_functions
