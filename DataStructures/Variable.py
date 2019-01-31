class Variable:

    def __init__(self, domain):
        self.domain = domain
        self.value = None

    @property
    def unassigned(self):
        return self.value is None

    def commit_value(self, val):
        self.value = val
        self.domain = {val}
