import random


def random_heuristic(variables, csp):
    return random.sample(variables, 1)[0]


def most_constrained_heuristic(variables, csp):
    counts = csp.get_unassigned_domain_num_consistent_counts()
    variables = sorted(counts, key=counts.get) # sorted low to high by count
    return variables[0]
