import numpy as np
import prettytable as pt
from collections import OrderedDict


class DataTracker:

    def __init__(self):
        self.run_times = []
        self.search_nodes = []
        self.heuristic_data = OrderedDict()
        self.table = pt.PrettyTable(["Puzzle", "Metric", "Random", "Most Constrained", "Most Constraining"])

    def get_average_run_time(self):
        return np.average(self.run_times)

    def get_average_search_nodes(self):
        return int(np.average(self.search_nodes))

    def get_standard_deviation_run_time(self):
        return np.std(self.run_times)

    def get_standard_deviation_search_nodes(self):
        return np.std(self.search_nodes)

    def add_heuristic_record(self, heuristic, n):
        if n not in self.heuristic_data:
            self.heuristic_data[n] = {heuristic: ""}

        heuristic_dict = {"avgruntime": self.get_average_run_time(),
                          "stdruntime": self.get_standard_deviation_run_time(),
                          "avgnodes": self.get_average_search_nodes(),
                          "stdnodes": self.get_standard_deviation_search_nodes()}

        self.heuristic_data[n][heuristic] = heuristic_dict

    def display_results(self):
        for puzzle_size, all_heuristics in self.heuristic_data.items():
            self.table.add_row(["{}x{}".format(puzzle_size, puzzle_size), "Average Runtime (seconds)", all_heuristics["random"]["avgruntime"], all_heuristics["most_constrained"]["avgruntime"], all_heuristics["most_constraining"]["avgruntime"]])
            self.table.add_row(["", "Standard Deviation Runtime (seconds)", all_heuristics["random"]["stdruntime"], all_heuristics["most_constrained"]["stdruntime"], all_heuristics["most_constraining"]["stdruntime"]])
            self.table.add_row(["", "Average # Search Nodes", all_heuristics["random"]["avgnodes"], all_heuristics["most_constrained"]["avgnodes"], all_heuristics["most_constraining"]["avgnodes"]])
            self.table.add_row(["", "Standard Deviation # Search Nodes", all_heuristics["random"]["stdnodes"], all_heuristics["most_constrained"]["stdnodes"], all_heuristics["most_constraining"]["stdnodes"]])
            self.table.add_row(["", "", "", "", ""])
        print(self.table)
        self.table_to_file()

    def table_to_file(self):
        table_txt = self.table.get_string()
        with open('last-run-metrics.txt', 'w') as file:
            file.write(table_txt)

    def clear(self):
        self.run_times = []
        self.search_nodes = []

    def __str__(self):
        return "Average Runtime: {}\n".format(self.get_average_run_time()) + \
                "Standard Deviation Runtime: {}\n".format(self.get_standard_deviation_run_time()) + \
                "Average Number of Search Nodes: {}\n".format(self.get_average_search_nodes()) + \
                "Standard Deviation of Search Nodes: {}\n".format(self.get_standard_deviation_search_nodes())
