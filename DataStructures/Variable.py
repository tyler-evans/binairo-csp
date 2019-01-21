class Variable:

    def __init__(self, domain):
        self.domain = domain
        self.value = None

    def set_value(self, value):
        self.value = value
        self.domain = {value}

    @property
    def unassigned(self):
        return self.value is None
