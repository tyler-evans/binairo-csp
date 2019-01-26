import random
import time
import os

from DataUtility.ReadData import read_board, read_boards_from_file
from CSPBuilding.CSPBuilding import construct_variables, construct_constraints
from DataStructures.CSP import CSP
from Heuristic.Heuristic import random_heuristic, most_constrained_node_heuristic, most_constraining_node_heuristic
from DataStructures.NodeTracker import NodeTracker


def backtracking(csp, heuristic):
    node_tracker = NodeTracker()
    result = recursive_backtracking(csp, heuristic, node_tracker)
    return result, node_tracker


def recursive_backtracking(csp, heuristic, node_tracker):
    if csp.is_solution_board():
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


def time_solve(path, heuristic, board=None, heuristic_name=''):
    if heuristic_name:
        heuristic.__name__ = heuristic_name
    if board is None:
        board, n = read_board(path)
    else:
        n = board.shape[0]

    print(60*'=')
    print('Solving ({}x{}) board with ({})'.format(n, n, heuristic.__name__))
    print('\n'.join([''.join(r) for r in board]), '\n')

    row_vars, col_vars = construct_variables(board, n)
    constraints = construct_constraints(row_vars, col_vars, n)
    csp = CSP(row_vars, col_vars, constraints, n)

    start_time = time.time()
    result, node_tracker = backtracking(csp, heuristic)
    total_time = time.time() - start_time
    print('(Solution)')
    print("{}\n".format(result))
    print('Total Time: {}'.format(total_time))
    print('Total Nodes: {}'.format(node_tracker.num_search_nodes))

    return result, total_time, node_tracker


def debugging_example():
    # KEPT DEBUGGING EXAMPLE FOR FUTURE TESTING PURPOSES IF NEEDED
    data, n = read_board('Data/example_1.txt')
    print(data, f'{n}x{n}')

    row_vars, col_vars = construct_variables(data, n)
    constraints = construct_constraints(row_vars, col_vars, n)
    csp = CSP(row_vars, col_vars, constraints, n)

    print('\n', len(csp.constraints), 'constraints and', len(csp.variables), 'variables')
    print('domain sizes: ', [len(v.domain) for v in csp.unassigned_variables])

    start_time = time.time()
    result, node_tracker = backtracking(csp, random_heuristic)
    total_time = time.time() - start_time

    print('Solution\n'.format(result))
    print('Total time: ', total_time)
    # KEPT DEBUGGING EXAMPLE FOR FUTURE TESTING PURPOSES IF NEEDED

    # Go through some timings
    # TODO Implement node counting
    boards = {
        6: 'Data/6x6_very_hard.txt',
        8: 'Data/8x8_example.txt',
        10: 'Data/10x10_example.txt',
        12: 'Data/12x12_example.txt',
        14: 'Data/14x14_example.txt'
    }

    print('\n', '='*64)
    board_path = boards[6]
    heuristic = lambda x: most_constrained_node_heuristic(x, False)
    print('Solving board at', board_path, 'with heuristic:', heuristic.__name__)
    result, total_time, node_tracker = time_solve(board_path, heuristic)

    print('\n', '='*64)
    board_path = boards[8]
    heuristic = lambda x: most_constrained_node_heuristic(x, False)
    print('Solving board at', board_path, 'with heuristic:', heuristic.__name__)
    result, total_time, node_tracker = time_solve(board_path, heuristic)

    print('\n', '='*64)
    board_path = boards[6]
    heuristic = random_heuristic
    print('Solving board at', board_path, 'with heuristic:', heuristic.__name__)
    result, total_time, node_tracker = time_solve(board_path, heuristic)

    print('\n', '='*64)
    board_path = boards[8]
    heuristic = random_heuristic
    print('Solving board at', board_path, 'with heuristic:', heuristic.__name__)
    result, total_time, node_tracker = time_solve(board_path, heuristic)


# Iterate through all backtracking-heuristic combinations
def solve():
    file_name = 'Data/binairo_evaluation.txt'
    all_boards = read_boards_from_file(file_name)

    heuristics = {'random': random_heuristic,
                  'most_constrained': lambda x: most_constrained_node_heuristic(x, False),
                  'most_constraining': lambda x: most_constraining_node_heuristic(x, False)}

    for board in all_boards:
        for name, heuristic in heuristics.items():
            result, total_time, node_tracker = time_solve("", heuristic, board=board, heuristic_name=name)


def main():
    random.seed(1)
    solve()
    #debugging_example()


if __name__ == "__main__":
    main()
