import random
import time
import os
import copy

from DataUtility.ReadData import read_board, read_individual_board
from CSPBuilding.CSPBuilding import construct_variables, construct_constraints
from DataStructures.CSP import CSP
from Heuristic.Heuristic import random_heuristic, most_constrained_heuristic


def recursive_backtracking(csp, heuristic):
    if csp.is_solution_board():
        return csp

    # start_time = time.time()

    # check_list = []
    # for i in range(10000):
    #     copy_csp = copy.deepcopy(csp)
    #     check_list.append(copy_csp)
    #
    # total_time = time.time() - start_time
    # print('Total Time: {}'.format(total_time))

    unassigned_variables = csp.unassigned_variables
    if not unassigned_variables:
        return -1

    variable = heuristic(unassigned_variables, csp)
    if not variable:
        return -1

    for d in variable.domain:

        # if value is consistent
        variable.value = d
        if csp.is_valid_board():
            result = recursive_backtracking(csp, heuristic)
            if result != -1:  # didn't fail
                return result
            variable.value = None
        else:
            # revert value
            variable.value = None

    return -1


def time_solve(path, heuristic, board=None, n=None):
    if board is None or n is None:
        board, n = read_board(path)

    print(60*'=')
    print('Solving ({}x{}) board with ({})'.format(n, n, heuristic.__name__))
    print('\n'.join([''.join(r) for r in board]), '\n')

    row_vars, col_vars = construct_variables(board, n)
    constraints = construct_constraints(row_vars, col_vars, n)
    csp = CSP(row_vars, col_vars, constraints, n)

    start_time = time.time()
    result = recursive_backtracking(csp, heuristic)
    total_time = time.time() - start_time
    print('(Solution)')
    print("{}\n".format(result))
    print('Total Time: {}'.format(total_time))

    return result, total_time


def debugging_example():
    # KEPT DEBUGGING EXAMPLE FOR FUTURE TESTING PURPOSES IF NEEDED
    data, n = read_board('Data/example_1.txt')
    print(data, '{}x{}'.format(n,n))

    row_vars, col_vars = construct_variables(data, n)
    constraints = construct_constraints(row_vars, col_vars, n)
    csp = CSP(row_vars, col_vars, constraints, n)

    print('\n', len(csp.constraints), 'constraints and', len(csp.variables), 'variables')
    print('domain sizes: ', [len(v.domain) for v in csp.unassigned_variables])

    start_time = time.time()
    result = recursive_backtracking(csp, random_heuristic)
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
    heuristic = most_constrained_heuristic
    print('Solving board at', board_path, 'with heuristic:', heuristic.__name__)
    result, total_time = time_solve(board_path, heuristic)

    print('\n', '='*64)
    board_path = boards[8]
    heuristic = most_constrained_heuristic
    print('Solving board at', board_path, 'with heuristic:', heuristic.__name__)
    result, total_time = time_solve(board_path, heuristic)

    print('\n', '='*64)
    board_path = boards[6]
    heuristic = random_heuristic
    print('Solving board at', board_path, 'with heuristic:', heuristic.__name__)
    result, total_time = time_solve(board_path, heuristic)

    print('\n', '='*64)
    board_path = boards[8]
    heuristic = random_heuristic
    print('Solving board at', board_path, 'with heuristic:', heuristic.__name__)
    result, total_time = time_solve(board_path, heuristic)


# Iterate through all backtracking-heuristic combinations
def solve():
    file_name, separator = 'Data/binairo_samples.txt', "#End"
    if os.path.isfile(file_name):
        with open(file_name) as board_file:
            data = []
            for line in board_file.readlines():
                data.append(line)
                if separator in line:
                    # Read in the board and compute it's dimensionality
                    board, n = read_individual_board(data)
                    data.clear()

                    # Go through all the heuristics
                    for heuristic in [random_heuristic, most_constrained_heuristic]:
                        result, total_time = time_solve("", heuristic, board=board, n=n)
    else:
        print("File: {} not found".format(file_name))


def main():
    random.seed(1)
    solve()
    #debugging_example()


if __name__ == "__main__":
    main()
