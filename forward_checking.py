import copy
import time
import os

from DataUtility.ReadData import read_board, read_individual_board
from CSPBuilding.CSPBuilding import construct_variables, construct_constraints, update_unassigned_variables
from DataStructures.CSP import CSP
from Heuristic.Heuristic import random_heuristic_index, most_constrained_heuristic_index, most_constraining_heuristic_index
from AC3.AC3 import ac3


def recursive_forwardchecking(csp, heuristic):
    # Finished
    if not csp.unassigned_variables:
        return csp

    # Need to backtrack
    for x_k in csp.variables:
        if len(x_k.domain) == 0:
            return -1

    heuristic_index = heuristic(csp.unassigned_variables, csp)
    previous_csp = copy.deepcopy(csp)

    # For each available value x in Ai
    for val in list(csp.unassigned_variables[heuristic_index].domain):

        # For each k in (1,2,...,n) -> Define A'k = Ak
        # A'i is committed to a value
        csp.unassigned_variables[heuristic_index].set_value(val)

        print([len(x.domain) for x in csp.variables])
        print("UNASSIGNED VARS: {}".format(len(csp.unassigned_variables)))

        csp = ac3(csp)

        # We don't need to back track
        if csp.is_valid_board():

            csp_result = recursive_forwardchecking(csp, heuristic)
            if csp_result != -1:
                return csp_result

        csp = copy.deepcopy(previous_csp)

    return -1


def time_solve(board, n, heuristic):
    print(60*'=')
    print('Solving ({}x{}) board with ({})'.format(n, n, heuristic.__name__))
    print('\n'.join([''.join(r) for r in board]), '\n')

    # Construct all legal values for each row + column Variable in the CSP graph
    row_vars, col_vars = construct_variables(board, n)
    constraints = construct_constraints(row_vars, col_vars, n)
    csp = CSP(row_vars, col_vars, constraints, n)
    ac3(csp)
    start_time = time.time()
    result = recursive_forwardchecking(csp, heuristic)
    total_time = time.time() - start_time
    print('(Solution)')
    print("{}\n".format(result))
    print('Total Time: {}'.format(total_time))

    return result, total_time


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
                    for heuristic in [most_constrained_heuristic_index]:
                        result, total_time = time_solve(board, n, heuristic)
    else:
        print("File: {} not found".format(file_name))


if __name__ == "__main__":
    solve()
