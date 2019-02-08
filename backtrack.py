import random
import numpy as np
import argparse

from copy import deepcopy

from DataUtility.ReadData import read_boards_from_file
from CSPBuilding.CSPBuilding import construct_csp
from Heuristic.Heuristic import random_heuristic, most_constrained_node_heuristic, most_constraining_node_heuristic
from DataStructures.NodeTracker import NodeTracker
from DataUtility.DataTracker import DataTracker


def backtracking(csp, heuristic):
    node_tracker = NodeTracker(verbose_display=True)
    result = recursive_backtracking(csp, heuristic, node_tracker)
    node_tracker.solution_board = result
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

    parser = argparse.ArgumentParser(description='Solve binairo puzzles')
    parser.add_argument('--file', type=str, help='Path to input file')
    parser.add_argument('--num_runs', type=int, help='Number of solves for each puzzle/heuristic combination', default=1)
    args = parser.parse_args()

    if args.file is None:
        file = 'Data/binairo_evaluation.txt'
        print('No file provided, defaulting to file at: ', file)

    print('Solving', args.num_runs, 'runs for each puzzle/heuristic combination')

    heuristics = {'most_constrained': lambda x: most_constrained_node_heuristic(x, False),
                  'most_constraining': lambda x: most_constraining_node_heuristic(x, False),
                  'random': random_heuristic}

    seed = random.randint(0, 4190)
    np.random.seed(seed)
    random.seed(seed)
    print('Experiment seed: {}\n'.format(seed))

    all_boards = read_boards_from_file(file)
    data_tracker = DataTracker()

    for board in all_boards:

        csp = construct_csp(board)

        for heuristic_name, heuristic in heuristics.items():

            data_tracker.clear()
            print('Solving {}x{} board with {} heuristic'.format(csp.n, csp.n, heuristic_name))

            for solve_number in range(args.num_runs):
                result, node_tracker = backtracking(deepcopy(csp), heuristic)
                assert result.is_solution_board() or node_tracker.out_of_time()
                data_tracker.run_times.append(node_tracker.get_elapsed_time())
                data_tracker.search_nodes.append(node_tracker.num_search_nodes)

                print(solve_number + 1, node_tracker)

            data_tracker.add_heuristic_record(heuristic_name, csp.n)
            print(data_tracker)
            print('-' * 50)

    data_tracker.display_results()


if __name__ == "__main__":
    main()
