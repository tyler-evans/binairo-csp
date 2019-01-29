import random
import numpy as np

def random_heuristic(variables, csp):
    return random.sample(variables, 1)[0]


def most_constrained_heuristic(variables, csp):
    counts = csp.get_unasigned_domain_num_consistent_counts()
    variables = sorted(counts, key=counts.get)  # sorted low to high by count
    return variables[0]


def random_heuristic_index(variables, csp):
    return variables.index(random.sample(variables, 1)[0])


def most_constrained_heuristic_index(variables, csp):
    counts = csp.get_unassigned_domain_greater_than_one_domain_num_consistent_counts(variables)
    variables = sorted(counts, key=counts.get)  # sorted low to high by count
    return variables.index(variables[0])


def most_constraining_heuristic_index(variables, csp):
    counts = [len(v.domain) for v in variables]
    max_indices = np.where(counts == np.max(counts))[0]
    unassigned_variable_index = random.choice(max_indices)
    return unassigned_variable_index


def _get_counts(csp):
    counts = [len(v.domain) for v in csp.unassigned_variables]
    return np.array(counts)