import random
import numpy as np

from copy import deepcopy

from DataUtility.ReadData import read_boards_from_file
from CSPBuilding.CSPBuilding import construct_csp
from Heuristic.Heuristic import random_heuristic, most_constrained_node_heuristic, most_constraining_node_heuristic
from DataStructures.NodeTracker import NodeTracker


def backtracking(csp, heuristic):
    node_tracker = NodeTracker()
    result = recursive_backtracking(csp, heuristic, node_tracker)
    node_tracker.end()
    return result, node_tracker


def recursive_backtracking(csp, heuristic, node_tracker):
    if csp.is_solution_board() or node_tracker.out_of_time():
        return csp

    if not csp.unassigned_variables:
        return -1

    # get index of next unassigned variable to try
    variable_index = heuristic(csp)

    for d in list(csp.variables[variable_index].domain):

        csp.variables[variable_index].value = d
        node_tracker.increment()

        if csp.is_valid_board():
            result = recursive_backtracking(csp, heuristic, node_tracker)
            if result != -1:  # didn't fail
                return result
        csp.variables[variable_index].value = None  # revert value

    return -1


def main():

    # TODO: Accept user input for puzzle path
    file_name = 'Data/binairo_samples.txt'
    num_repeat_solve = 3
    print_solutions = False

    heuristics = {'random': random_heuristic,
                  'most_constrained': lambda x: most_constrained_node_heuristic(x, False),
                  'most_constraining': lambda x: most_constraining_node_heuristic(x, False)}

    seed = random.randint(0, 4190)
    np.random.seed(seed)
    random.seed(seed)
    print('Experiment seed: {}\n'.format(seed))

    all_boards = read_boards_from_file(file_name)

    for board in all_boards:

        csp = construct_csp(board)

        for heuristic_name, heuristic in heuristics.items():
            print('Solving {}x{} board with {} heuristic'.format(csp.n, csp.n, heuristic_name))

            for solve_number in range(num_repeat_solve):
                result, node_tracker = backtracking(deepcopy(csp), heuristic)
                assert result.is_solution_board() or node_tracker.out_of_time()

                if print_solutions:
                    print('Solution:')
                    print(result)

                print(solve_number + 1, node_tracker)

            print('-' * 50)


if __name__ == "__main__":
    main()
