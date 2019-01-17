class Constraint:

    def __init__(self, v1, v2, condition, name=''):
        self.v1 = v1
        self.v2 = v2
        self.condition = condition
        self.name = name

    def __bool__(self):
        return self.condition(self.v1, self.v2)

    def __str__(self):
        return self.name
