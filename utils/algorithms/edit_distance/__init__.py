from typing import Optional

from .constants import EditOperation
from .constants.cost_functions import levenshtein_cost_function
from .wf_edit_distance import calculate_minimum_edit_distance, get_edit_path


def nested_levenshtein_cost_function(current_input: Optional[str], proposed_output: Optional[str],
                                     move: EditOperation) -> int:
    if move == EditOperation.INSERT:
        cost = len(proposed_output)
    elif move == EditOperation.DELETE:
        cost = len(current_input)
    elif move == EditOperation.SUBSTITUTE:
        if current_input == proposed_output:
            cost = 0
        else:
            cost, _ = calculate_minimum_edit_distance(current_input, proposed_output, levenshtein_cost_function)
    else:
        raise ValueError(f"Invalid move <{move}> provided. Please try again with a valid move.")
    return cost
