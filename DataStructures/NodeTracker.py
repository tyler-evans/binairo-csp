import time


class NodeTracker:

    def __init__(self, time_limit=60, verbose_display=False):
        self.solution_board = None
        self.verbose_display = verbose_display
        self.num_search_nodes = 0
        self.end_time = None
        self.did_not_finish = False
        self.time_limit = time_limit  # time_limit in seconds
        self.start_time = time.time()

    def increment(self):
        self.num_search_nodes += 1

    def end(self):
        if not self.did_not_finish:
            self.end_time = time.time()

    def get_elapsed_time(self):
        if self.did_not_finish:
            return -1
        else:
            return self.end_time - self.start_time

    def out_of_time(self):
        result = (time.time() - self.start_time) > self.time_limit
        if result:
            self.did_not_finish = True
        return result

    def __str__(self):
        result = '\tNodes: {}'.format(self.num_search_nodes)
        if self.did_not_finish:
            result += '\n\tTime: DNF after limit of {} seconds\n'.format(self.time_limit)
        else:
            result += '\n\tTime: {:.5f} seconds\n'.format(self.get_elapsed_time())
        if self.verbose_display:
            result += '\t' + '\t'.join(str(self.solution_board).splitlines(True)) + '\n'
        return result
