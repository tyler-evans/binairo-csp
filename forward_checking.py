import random
import numpy as np

from copy import deepcopy

from CSPBuilding.CSPBuilding import construct_variables, construct_constraints
from DataStructures.CSP import CSP
from Heuristic.Heuristic import random_heuristic, most_constrained_node_heuristic, most_constraining_node_heuristic
from ConstraintPropagation.ConstraintPropagation import AC_3
from Scraper.Scraper import scrape_board
from DataStructures.NodeTracker import NodeTracker


def backtracking_with_forward_checking(csp, heuristic):
    node_tracker = NodeTracker()

    csp = AC_3(csp)

    result = recursive_backtracking_with_forward_checking(csp, heuristic, node_tracker)
    node_tracker.end()
    return result, node_tracker


def recursive_backtracking_with_forward_checking(csp, heuristic, node_tracker):
    if csp.is_solution_board():
        return csp
    if 0 in [len(v.domain) for v in csp.variables] or not csp.unassigned_variables:
        return -1

    # get index of next unassigned variable to try
    variable_index = heuristic(csp)

    old_csp = deepcopy(csp)
    for d in list(csp.variables[variable_index].domain):

        csp.variables[variable_index].set_value(d)
        node_tracker.increment()

        csp = AC_3(csp)  # perform constraint propagation

        if csp.is_valid_board():  # if value is consistent
            result = recursive_backtracking_with_forward_checking(csp, heuristic, node_tracker)
            if result != -1:  # didn't fail
                return result
        csp = deepcopy(old_csp)  # revert assignments

    return -1


def main():

    ##########################################################################
    # For POC, scrape some vhard 14x14 puzzles, apply dropout (to make harder)
    # and solve using constraint prop (no heuristic)
    ##########################################################################

    # TODO: Accept user input for puzzle path

    heuristics = {'random': random_heuristic,
                  'most_constrained': lambda x: most_constrained_node_heuristic(x, True),
                  'most_constraining': lambda x: most_constraining_node_heuristic(x, True)}

    np.random.seed(42)
    random.seed(42)
    for puzzle_no in range(1, 5):

        do_dropout = True
        dropout = 0.5
        difficulty = 4
        n = 14
        data = scrape_board(difficulty, puzzle_no, n)

        if do_dropout:
            for i in range(n):
                for j in range(n):
                    mask = np.random.choice([0, 1], p=[dropout, 1 - dropout])
                    if not mask:
                        data[i][j] = '_'

        row_vars, col_vars = construct_variables(data, n)
        constraints = construct_constraints(row_vars, col_vars, n)
        csp = CSP(row_vars, col_vars, constraints, n)

        #print('solving...')
        csp, node_tracker = backtracking_with_forward_checking(csp, heuristics['random'])
        assert csp.is_solution_board()
        #print(csp)

        print('Puzzle no:', puzzle_no, 'Number of nodes:', node_tracker.num_search_nodes)
        #print('Time taken: {:.5f} seconds'.format(node_tracker.get_elapsed_time()))


if __name__ == "__main__":
    main()
