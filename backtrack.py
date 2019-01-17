import random
import time

from DataUtility.ReadData import read_board
from CSPBuilding.CSPBuilding import construct_variables, construct_constraints
from DataStructures.CSP import CSP
from Heuristic.Heuristic import random_heuristic, most_constrained_heuristic


def recursive_backtracking(csp, heuristic):
    if csp.is_solution_board():
        return csp

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


def time_solve(path, heuristic):
    board, n = read_board(path)
    print('\n'.join([''.join(r) for r in board]), '\n')

    row_vars, col_vars = construct_variables(board, n)
    constraints = construct_constraints(row_vars, col_vars, n)
    csp = CSP(row_vars, col_vars, constraints, n)

    start_time = time.time()
    result = recursive_backtracking(csp, heuristic)
    total_time = time.time() - start_time
    print(result)
    print('Total time: ', total_time)

    return result, total_time


def main():
    random.seed(1)

    # Debugging example
    data, n = read_board('Data/example_1.txt')
    print(data, f'{n}x{n}')

    row_vars, col_vars = construct_variables(data, n)
    constraints = construct_constraints(row_vars, col_vars, n)
    csp = CSP(row_vars, col_vars, constraints, n)

    print('\n', len(csp.constraints), 'constraints and', len(csp.variables), 'variables')
    print('domain sizes: ', [len(v.domain) for v in csp.unassigned_variables])

    start_time = time.time()
    result = recursive_backtracking(csp, random_heuristic)
    total_time = time.time() - start_time

    print(result)
    print('Total time: ', total_time)

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


if __name__ == "__main__":
    main()
