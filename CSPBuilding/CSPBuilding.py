import numpy as np
import itertools

from copy import deepcopy
from DataStructures.Variable import Variable
from DataStructures.Constraint import Constraint


def construct_valid_domain(n):
    domain = itertools.product([0,1], repeat=n)
    domain = itertools.filterfalse(lambda x: sum(x)!=n//2, domain)
    domain = itertools.filterfalse(lambda x: has_3_in_a_row(x), domain)
    return set(domain)


def filter_domain(domain, i, val):
    return {x for x in domain if x[i]==val}


def construct_variables(data, n):
    domain = construct_valid_domain(n)
    row_vars = [Variable(deepcopy(domain)) for row in range(n)]
    col_vars = [Variable(deepcopy(domain)) for col in range(n)]

    # filter variable domains based on provided board input
    for i in range(n):
        for j in range(n):
            if data[i][j] == '1':
                row_vars[i].domain = filter_domain(row_vars[i].domain, j, 1)
                col_vars[j].domain = filter_domain(col_vars[j].domain, i, 1)
            elif data[i][j] == '0':
                row_vars[i].domain = filter_domain(row_vars[i].domain, j, 0)
                col_vars[j].domain = filter_domain(col_vars[j].domain, i, 0)

    return row_vars, col_vars


def construct_constraints(row_vars, col_vars, n):
    constraints = []

    # constraints that relate the row/col variables to the board
    def row_col_board_constraint(i, j):
        return lambda row_var, col_var: row_var.value is None or col_var.value is None or row_var.value[j] == col_var.value[i]

    constraints += [Constraint(row_vars[i], col_vars[j], row_col_board_constraint(i,j), name=f'row_col_equal({i},{j})') for i in range(n) for j in range(n)]

    # ALLDIFF constraint on the rows
    condition = lambda v1, v2: v1.value is None or v2.value is None or v1.value != v2.value
    constraints += [Constraint(row_vars[i], row_vars[j], condition, name=f'row_alldiff({i},{j})') for i in range(n) for j in range(i+1,n)]

    # ALLDIFF constraint on the cols
    constraints += [Constraint(col_vars[i], col_vars[j], condition, name=f'col_alldiff({i},{j})') for i in range(n) for j in range(i+1,n)]

    return constraints


def has_3_in_a_row(arr):
    windows = np.array([arr[i:i+3] for i in range(len(arr)-2)])
    return np.all(windows == [0,0,0], axis=1).any() or np.all(windows == [1,1,1], axis=1).any()

