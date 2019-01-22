import random
import numpy as np

from copy import deepcopy

from CSPBuilding.CSPBuilding import construct_variables, construct_constraints
from DataStructures.CSP import CSP
from Heuristic.Heuristic import random_heuristic
from ConstraintPropagation.ConstraintPropagation import AC_3
from Scraper.Scraper import scrape_board
from DataStructures.NodeTracker import NodeTracker


def backtracking_with_forward_checking(csp, heuristic):
    node_tracker = NodeTracker()

    csp = AC_3(csp)
    #csp.assign_trivial_variables()

    result = recursive_backtracking_with_forward_checking(csp, heuristic, node_tracker)
    return result, node_tracker


def recursive_backtracking_with_forward_checking(csp, heuristic, node_tracker):
    if csp.is_solution_board():
        return csp

    if 0 in [len(v.domain) for v in csp.variables]:
        return -1

    #unassigned_variables = csp.unassigned_variables
    if not csp.unassigned_variables:
        return -1

    #variable = heuristic(unassigned_variables, csp)
    # TODO Heuristics modified to support new variable index approach
    variable_index = 0
    # if not variable:
    #     return -1

    old_csp = deepcopy(csp)
    for d in list(csp.unassigned_variables[variable_index].domain):


        csp.unassigned_variables[variable_index].set_value(d)
        node_tracker.increment()

        csp = AC_3(csp)  # perform constraint propagation
        #csp.assign_trivial_variables()  # bind all variables that have a one element domain

        if csp.is_valid_board():  # if value is consistent
            result = recursive_backtracking_with_forward_checking(csp, heuristic, node_tracker)
            if result != -1:  # didn't fail
                return result
            csp = deepcopy(old_csp)  # revert assignments
        else:
            csp = deepcopy(old_csp)  # revert assignments

    return -1


def main():

    ##########################################################################
    # For POC, scrape some vhard 14x14 puzzles, apply dropout (to make harder)
    # and solve using constraint prop (no heuristic)
    ##########################################################################

    # TODO: Heuristics return index into `csp.unassigned_variables`
    # TODO: Implement all heuristics
    # TODO: Accept user input for puzzle
    # TODO: Clean up

    np.random.seed(42)
    random.seed(42)
    for puzzle_no in range(1, 100):

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

        print('solving...')
        csp, node_tracker = backtracking_with_forward_checking(csp, random_heuristic)
        print(csp)

        print('\n', puzzle_no, csp.is_solution_board(), 'num_nodes: {}'.format(node_tracker.num_search_nodes))


if __name__ == "__main__":
    main()
