class Constraint:

    def __init__(self, v1, v2, condition, name=''):
        self.v1 = v1
        self.v2 = v2
        self.condition = condition
        self.name = name
        self.variables = [v1, v2]

    def __bool__(self):
        return self.condition(self.v1, self.v2)

    def __contains__(self, variable):
        return variable == self.v1 or variable == self.v2

    def __str__(self):
        return self.name

    def is_row_col_equal_constraint(self):
        return "row_col_equal" in self.name
