import random
import numpy as np


def random_heuristic(csp):
    unassigned_variable_index = random.randint(0, len(csp.unassigned_variables) - 1)
    return _convert_index(csp, unassigned_variable_index)


def most_constrained_node_heuristic(csp, domains_are_consistent):
    counts = _get_counts(csp, domains_are_consistent)
    min_indices = np.where(counts == np.min(counts))[0]
    unassigned_variable_index = random.choice(min_indices)
    return _convert_index(csp, unassigned_variable_index)


def most_constraining_node_heuristic(csp, domains_are_consistent):
    counts = _get_counts(csp, domains_are_consistent)
    max_indices = np.where(counts == np.max(counts))[0]
    unassigned_variable_index = random.choice(max_indices)
    return _convert_index(csp, unassigned_variable_index)


def _get_counts(csp, domains_are_consistent):
    if domains_are_consistent:
        counts = [len(v.domain) for v in csp.unassigned_variables]
    else:
        counts = [csp.count_num_consistent_values(v) for v in csp.unassigned_variables]
    return np.array(counts)


def _convert_index(csp, unassigned_variable_index):
    return csp.variables.index(csp.unassigned_variables[unassigned_variable_index])