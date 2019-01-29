import numpy as np
import itertools

from copy import deepcopy
from DataStructures.Variable import Variable
from DataStructures.Constraint import Constraint


# Construct all permutations of "0's" and "1's" in a list of size n ->
# find all possible permutations in which the number of "0's" and "1's" in the list are both equivalent (n//2) ->
# find all possible permutations in which there are no 3 adjacent "0's" and "1's" in a row -> return
def construct_valid_domain(n):
    domain = itertools.product([0,1], repeat=n)
    domain = itertools.filterfalse(lambda x: sum(x)!=n//2, domain)
    domain = itertools.filterfalse(lambda x: has_3_in_a_row(x), domain)
    return set(domain)


# Given the already "set" values in the row or column domain passed in, filter
# the constraints to the possibilities that the row or column can theoretically satisfy
def filter_domain(domain, i, val):
    return {x for x in domain if x[i]== val}


# Remove the specified value from the domain range of all vars
def modify_domain_value(assigned_variable, variables, mode):
    if mode == "add":
        [var.domain.add(assigned_variable.value) for var in variables if assigned_variable.value in var.domain and var is not assigned_variable]
    elif mode == "remove":
        [var.domain.remove(assigned_variable.value) for var in variables if assigned_variable.value in var.domain and var is not assigned_variable]


def construct_variables(data, n):
    # Create a representation of all the valid row + col domains for Binairo
    domain = construct_valid_domain(n)

    # Create an individual constraint domain for each cell within the nxn board
    row_vars = [Variable(deepcopy(domain)) for row in range(n)]
    col_vars = [Variable(deepcopy(domain)) for col in range(n)]

    # Based on the values a given row or column already has set in their cells, we can filter the valid domains
    # such that the number of valid states we need to check later on is reduced by the information about
    # the row, column and existing domain constraints we already know
    for i in range(n):
        for j in range(n):
            if data[i][j] == '1':
                row_vars[i].domain = filter_domain(row_vars[i].domain, j, 1)
                col_vars[j].domain = filter_domain(col_vars[j].domain, i, 1)
            elif data[i][j] == '0':
                row_vars[i].domain = filter_domain(row_vars[i].domain, j, 0)
                col_vars[j].domain = filter_domain(col_vars[j].domain, i, 0)

    return row_vars, col_vars


# Update all unassigned variable's domains based off of the value assigned to an adajcent node in the CSP graph
def update_unassigned_variables(assigned_variable, csp, in_row_vars, mode):
    # Modify all row or column unassigned variable's domain values based on assigned value and mode (add or remove)
    modify_domain_value(assigned_variable, csp.row_vars, mode) if in_row_vars else modify_domain_value(assigned_variable, csp.col_vars, mode)


def construct_constraints(row_vars, col_vars, n):
    constraints = []

    # This is an additional constraint which is not inherently required in the Binairo puzzle, however it is necessary
    # in order to ensure a row + column node representation of a CSP graph works. This function ensures that if any
    # value is currently assigned to a row or a column which satisfies the constraints, that the assignment of another
    # row or column value doesn't "overwrite" the value stored in the row or column it would be affecting  -> this
    # function thereby ensures that all corresponding row and column value assignments "line up" with one another, such
    # that row + column value assignments do not compete with each other and overwrite their own data
    def row_col_board_constraint(i, j):
        return lambda row_var, col_var: row_var.value is None or col_var.value is None or row_var.value[j] == col_var.value[i]

    constraints += [Constraint(row_vars[i], col_vars[j], row_col_board_constraint(i,j), name='row_col_equal({},{})'.format(i,j)) for i in range(n) for j in range(n)]

    # Ensure each row is unique from every other row
    condition = lambda v1, v2: v1.value is None or v2.value is None or v1.value != v2.value
    constraints += [Constraint(row_vars[i], row_vars[j], condition, name='row_alldiff({},{})'.format(i,j)) for i in range(n) for j in range(i+1,n)]

    # Ensure each col is unique from every other col
    constraints += [Constraint(col_vars[i], col_vars[j], condition, name='col_alldiff({},{})'.format(i,j)) for i in range(n) for j in range(i+1,n)]

    return constraints


def has_3_in_a_row(arr):
    windows = np.array([arr[i:i+3] for i in range(len(arr)-2)])
    return np.all(windows == [0,0,0], axis=1).any() or np.all(windows == [1,1,1], axis=1).any()

