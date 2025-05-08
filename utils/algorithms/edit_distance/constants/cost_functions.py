from typing import Callable, Optional, TypeAlias

from .edits import EditOperation


# TODO: alter use of Optional[str] to some Comparable type? would have to custom-define it.


# This serves as an example function for the cost of moves in minimum edit distance.
# In this case, current_input and proposed_output don't get used--but they could be in more complex variations.
def levenshtein_cost_function(current_input: Optional[str], proposed_output: Optional[str],
                              move: EditOperation) -> int:
    if move == EditOperation.INSERT:
        cost = 1
    elif move == EditOperation.DELETE:
        cost = 1
    elif move == EditOperation.SUBSTITUTE:
        if current_input == proposed_output:
            cost = 0
        else:
            cost = 1
    else:
        raise ValueError(f"Invalid move <{move}> provided. Please try again with a valid move.")
    return cost


# This serves as an example function for the cost of moves in minimum edit distance.
# In this case, current_input and proposed_output don't get used--
# but they could be in variations that aren't as simple.
def debug_levenshtein_cost_function(current_input: Optional[str], proposed_output: Optional[str],
                                    move: EditOperation) -> int:
    if move == EditOperation.INSERT:
        cost = 1
        print(f"Move: adding {proposed_output}...")
    elif move == EditOperation.DELETE:
        cost = 1
        print(f"Move: removing {current_input}...")
    elif move == EditOperation.SUBSTITUTE:
        if current_input == proposed_output:
            cost = 0
        else:
            cost = 1
        print(f"Move: replacing {current_input} with {proposed_output}...")
    else:
        raise ValueError(f"Invalid move <{move}> provided. Please try again with a valid move.")
    return cost


def lcs_cost_function(current_input: Optional[str], proposed_output: Optional[str], move: EditOperation) -> int:
    if move == EditOperation.INSERT:
        cost = 1
    elif move == EditOperation.DELETE:
        cost = 1
    elif move == EditOperation.SUBSTITUTE:
        if current_input == proposed_output:
            cost = 0
        else:
            cost = 2
    else:
        raise ValueError(f"Invalid move <{move}> provided. Please try again with a valid move.")
    return cost


CostFunction: TypeAlias = Callable[[Optional[str], Optional[str], EditOperation], float]


COST_FUNCTIONS: dict[str, CostFunction] = {
    "debug": debug_levenshtein_cost_function,
    "lcs": lcs_cost_function,
    "levenshtein": levenshtein_cost_function
}
