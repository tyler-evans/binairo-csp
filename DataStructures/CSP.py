import numpy as np


class CSP:

    def __init__(self, row_vars, col_vars, constraints, n):
        self.row_vars = row_vars
        self.col_vars = col_vars
        self.variables = row_vars + col_vars
        self.constraints = constraints
        self.n = n

    def is_valid_change(self, variable, value):
        old_value = variable.value
        variable.value = value
        result = self.is_valid_board()
        variable.value = old_value
        return result

    def get_unassigned_domain_num_consistent_counts(self):
        counts = {v: 0 for v in self.unassigned_variables}
        for v in self.unassigned_variables:
            for d in v.domain:
                counts[v] += self.is_valid_change(v, d)
        return counts

    def get_constraint_strs(self):
        return [(i, str(c), bool(c)) for i, c in enumerate(self.constraints)]

    @property
    def unassigned_variables(self):
        return [v for v in self.variables if v.unassigned]

    def is_valid_board(self):
        return all([len(v.domain) > 0 for v in self.variables]) and all(self.constraints)

    def is_full_board(self):
        return all([v.value is not None for v in self.variables])

    def is_solution_board(self):
        return self.is_full_board() and self.is_valid_board()

    def get_relevant_constraint(self, var_0, var_1):
        for c in self.constraints:
            if var_0 in c and var_1 in c:
                return c

    # bind values to variables that have domains of size 1
    def assign_trivial_variables(self):
        for v in self.unassigned_variables:
            if len(v.domain) == 1:
                v.value = list(v.domain)[0]

    def __str__(self):
        n = self.n
        board = np.repeat('_', n * n).reshape(n, n)
        for i, row in enumerate(self.row_vars):
            if row.value:
                board[i] = row.value
        for i, col in enumerate(self.col_vars):
            if col.value:
                board[:, i] = col.value
        return '\n'.join([''.join(r) for r in board])
