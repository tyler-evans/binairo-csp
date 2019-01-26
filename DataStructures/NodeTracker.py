import time


class NodeTracker:

    def __init__(self):
        self.num_search_nodes = 0
        self.start_time = time.time()
        self.end_time = None

    def increment(self):
        self.num_search_nodes += 1

    def end(self):
        self.end_time = time.time()

    def get_elapsed_time(self):
        return self.end_time - self.start_time

    def __str__(self):
        result = 'Number of nodes: {}'.format(self.num_search_nodes)
        result += '\nTime: {:.5f} seconds'.format(self.get_elapsed_time())
        return result
