from typing import Callable, Sequence

from numpy import dtype, zeros
from numpy.typing import NDArray, DTypeLike

from .constants import CostFunction, EditOperation


# We initialize the chart in accordance with Wagner and Fischer's Algorithm X.
def initialize_chart(source: Sequence, destination: Sequence, cost: CostFunction, data_type: str) -> \
        NDArray[float]:
    chart_size: tuple[int, int] = (len(source) + 1, len(destination) + 1)
    data_type: DTypeLike = dtype(data_type)
    new_chart: NDArray[float] = zeros(chart_size, data_type)
    fill_edges(source, destination, new_chart, cost)
    return new_chart


def fill_edges(source: Sequence, destination: Sequence, chart: NDArray[float], cost: CostFunction,
               row_constraint: int = 1, column_constraint: int = 1):
    fill_rows(source, chart, cost, row_constraint)
    fill_columns(destination, chart, cost, column_constraint)


def fill_rows(source: Sequence, chart: NDArray[float], cost: CostFunction, row_constraint: int):
    for i in range(row_constraint, len(source) + 1):
        chart[i, 0] = chart[i - 1, 0] + cost(source[i - 1], None, EditOperation.DELETE)


def fill_columns(destination: Sequence, chart: NDArray[float], cost: Callable, column_constraint: int):
    for j in range(column_constraint, len(destination) + 1):
        chart[0, j] = chart[0, j - 1] + cost(None, destination[j - 1], EditOperation.INSERT)


# We perform the main edit distance algorithm presented in Fischer and Wagner 1974.
def calculate_minimum_edit_distance(source: Sequence, destination: Sequence, cost: CostFunction,
                                    data_type: str = "int16") -> tuple[float, NDArray[float]]:
    chart: NDArray[float] = initialize_chart(source, destination, cost, data_type)
    for i in range(1, len(source) + 1):
        for j in range(1, len(destination) + 1):
            compute_edit_cost(source, destination, chart, cost, i, j)

    minimized_edit_distance = chart[len(source), len(destination)]
    return minimized_edit_distance.item(), chart


def compute_edit_cost(source: Sequence, destination: Sequence, chart: NDArray[float], cost: CostFunction,
                      row: int, column: int):
    substitution_cost: int = chart[row - 1, column - 1] + \
        cost(source[row - 1], destination[column - 1], EditOperation.SUBSTITUTE)
    deletion_cost: int = chart[row - 1, column] + cost(source[row - 1], None, EditOperation.DELETE)
    insertion_cost: int = chart[row, column - 1] + cost(None, destination[column - 1], EditOperation.INSERT)
    chart[row, column] = min(substitution_cost, deletion_cost, insertion_cost)


def get_edit_path(source: Sequence, destination: Sequence, chart: NDArray[float], cost: CostFunction) -> \
        list[tuple[int, int]]:
    i, j = len(source), len(destination)

    path_pairs: list[tuple[int, int]] = []
    while i != 0 and j != 0:
        if chart[i, j] == (chart[i - 1, j] + cost(source[i - 1], None, EditOperation.DELETE)):
            path_pairs.append((i - 1, j - 1))
            i -= 1
        elif chart[i, j] == (chart[i, j - 1] + cost(None, destination[j - 1], EditOperation.INSERT)):
            path_pairs.append((i - 1, j - 1))
            j -= 1
        else:
            path_pairs.append((i - 1, j - 1))
            i -= 1
            j -= 1

    while i > 0:
        path_pairs.append((i - 1, j))
        i -= 1

    while j > 0:
        path_pairs.append((i, j - 1))
        j -= 1

    path_pairs.reverse()
    return path_pairs
