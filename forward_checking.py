import random
import numpy as np

from copy import deepcopy

from CSPBuilding.CSPBuilding import construct_csp
from Heuristic.Heuristic import random_heuristic, most_constrained_node_heuristic, most_constraining_node_heuristic
from Scraper.Scraper import scrape_board
from DataStructures.NodeTracker import NodeTracker
from DataUtility.ReadData import read_boards_from_file
from AC3.AC3 import ac3


def backtracking_with_forward_checking(board, csp, heuristic):
    node_tracker = NodeTracker(board, verbose_display=True)

    csp = ac3(csp)

    result = recursive_forwardchecking(csp, heuristic, node_tracker)
    node_tracker.solution_board = result
    node_tracker.end()
    return result, node_tracker


def recursive_forwardchecking(csp, heuristic, node_tracker):
    # Finished
    if csp.is_solution_board() and not csp.unassigned_variables:
        return csp

    # Need to backtrack
    for x_k in csp.variables:
        if len(x_k.domain) == 0:
            return -1

    heuristic_index = heuristic(csp)

    # For each available value x in Ai
    for val in list(csp.variables[heuristic_index].domain):

        # For each k in (1,2,...,n) -> Define A'k = Ak
        copy_csp = deepcopy(csp)

        # A'i is committed to a value
        copy_csp.variables[heuristic_index].commit_value(val)

        node_tracker.increment()

        # Use the ac3 consistency algorithm to ensure all variables have
        # arc-consistent domains
        copy_csp = ac3(copy_csp)

        # We don't need to back track
        if copy_csp.is_valid_board():

            copy_csp_result = recursive_forwardchecking(copy_csp, heuristic, node_tracker)
            if copy_csp_result != -1:
                return copy_csp_result

    return -1


def scrape_and_solve_boards():

    ##########################################################################
    # For POC, scrape some vhard 14x14 puzzles, apply dropout (to make harder)
    # and solve using constraint prop (no heuristic)
    ##########################################################################

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

        csp = construct_csp(data)

        csp, node_tracker = backtracking_with_forward_checking(csp, heuristics['random'])
        assert csp.is_solution_board() or node_tracker.out_of_time()
        #print(csp)

        print(node_tracker)


def main():

    # TODO: Accept user input for puzzle path

    file_name = 'Data/binairo_evaluation.txt'
    num_repeat_solve = 3
    print_solutions = False

    heuristics = {'random': random_heuristic,
                  'most_constrained': lambda x: most_constrained_node_heuristic(x, True),
                  'most_constraining': lambda x: most_constraining_node_heuristic(x, True)}

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
                result, node_tracker = backtracking_with_forward_checking(board, deepcopy(csp), heuristic)
                assert result.is_solution_board()or node_tracker.out_of_time()

                if print_solutions:
                    print('Solution:')
                    print(result)

                print(solve_number + 1, node_tracker)

            print('-'*50)


if __name__ == "__main__":
    main()
    # scrape_and_solve_boards()