import copy
import time
import os

from DataUtility.ReadData import read_board, read_individual_board
from CSPBuilding.CSPBuilding import construct_variables, construct_constraints, update_unassigned_variables
from DataStructures.CSP import CSP
from Heuristic.Heuristic import random_heuristic_index, most_constrained_heuristic_index, most_constraining_heuristic_index


def recursive_forwardchecking(csp, heuristic):
    if not csp.unassigned_variables:
        return csp

    heuristic_index = heuristic(csp.unassigned_variables, csp)
    previous_csp = copy.deepcopy(csp)

    # For each available value x in Ai
    for val in csp.unassigned_variables[heuristic_index].domain:

        # For each k in (1,2,...,n) -> Define A'k = Ak
        # A'i is committed to a value
        csp.unassigned_variables[heuristic_index].domain = {val}
        csp.unassigned_variables[heuristic_index].value = val

        # print([len(x.domain) for x in csp.variables])
        # print("UNASSIGNED VARS: {}".format(len(csp.unassigned_variables)))

        result = propagate(csp)

        # We don't need to back track
        if result != -1:

            result = recursive_forwardchecking(csp, heuristic)
            if result != -1:
                return result

        csp = copy.deepcopy(previous_csp)

    return -1


def propagate(csp):
    finished = False

    # Iterate until no availability lists change
    while not finished:
        finished = True

        # Only keep values satisfying the CSP's constraints within each Variable's domain
        for i, c in enumerate(csp.constraints):
            v1 = c.variables[0]
            v2 = c.variables[1]

            # Store the original value so we can reset it after, and track if the Variable's domain changed
            v1_original_value, v2_original_value = v1.value, v2.value
            v1_legal_values, v2_legal_values = set(), set()
            changed = False

            # Reduce all the domains for arcs one way
            if v1_original_value is None and v2_original_value is not None:
                for val in v1.domain:
                    v1.value = val

                    if c:
                        v1_legal_values.add(val)

                v1.value = v1_original_value

                # Need to backtrack as we've exhausted all the possible options for this Variable's domain
                if len(v1_legal_values) == 0:
                    return -1

                if len(v1_legal_values) == 1:
                    v1.value, v1.domain = max(v1_legal_values), max(v1_legal_values)

                if len(v1_legal_values) < len(v1.domain):
                    changed = True
                    v1.domain = v1_legal_values

            # Reduce all the domains for arcs the other way
            if v2_original_value is None and v1_original_value is not None:
                for val in v2.domain:
                    v2.value = val

                    if c:
                        v2_legal_values.add(val)

                v2.value = v2_original_value

                # Need to backtrack as we've exhausted all the possible options for this Variable's domain
                if len(v2_legal_values) == 0:
                    return -1

                if len(v2_legal_values) == 1:
                    v2.value, v2.domain = max(v2_legal_values), max(v2_legal_values)

                if len(v2_legal_values) < len(v2.domain):
                    changed = True
                    v2.domain = v2_legal_values

                # print([len(x.domain) for x in csp.variables])
                # print("UNASSIGNED VARS: {}".format(len(csp.unassigned_variables)))
                # print(i)
                # print()

            if not csp.unassigned_variables:
                return

            # A variable's domain changed -> we're not finished ensuring all domains are reduced yet
            if changed:
                finished = False

    return


def time_solve(board, n, heuristic):
    print(60*'=')
    print('Solving ({}x{}) board with ({})'.format(n, n, heuristic.__name__))
    print('\n'.join([''.join(r) for r in board]), '\n')

    # Construct all legal values for each row + column Variable in the CSP graph
    row_vars, col_vars = construct_variables(board, n)
    constraints = construct_constraints(row_vars, col_vars, n)
    csp = CSP(row_vars, col_vars, constraints, n)

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
