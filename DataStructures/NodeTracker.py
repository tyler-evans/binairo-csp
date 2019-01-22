class NodeTracker:

    def __init__(self):
        self.num_search_nodes = 0

    def increment(self):
        self.num_search_nodes += 1
