

# Assumes that x_i (the other variable in the constraint) is binded, such that for each value in x_j,
# determine if there's a partner for the x_i value -> if not, remove i from x_i's domain
def exists_satisfactory_value(constraint, variable):
    for v in variable.domain:
        old_value = variable.value
        variable.value = v
        result = bool(constraint)
        variable.value = old_value
        if result:
            return True
    return False


# All constraints are binary within the CSP -> if x_k (a variable in a constraint) is involved in a constraint and it's
# not the first variable, it's the second variable
def get_neighbors(variable, all_constraints):
    return [c.v1 if c.v1 != variable else c.v2 for c in all_constraints if variable in c]


def remove_inconsistent_values(X_i, X_j, constraint):
    removed = False

    # Value is guaranteed to be arc-consistent if it's already been assigned
    if X_i.value:
        return False

    # For each value in x_i, check to see if there is a value within x_j which "partners" with x_i's value and allows
    # it to remain in x_i's domain (arc-consistent) -> otherwise it needs to be removed
    for x in list(X_i.domain):
        X_i.value = x
        if not exists_satisfactory_value(constraint, X_j):
            X_i.domain.remove(x)
            removed = True
    X_i.value = None

    return removed


# AC3 consistency algorithm created by Alan Mackworth which takes in a CSP and returns the CSP with possibly reduced
# domains which are all guaranteed to be arc-consistent
def AC_3(csp):

    # These are all the arcs we have to check, initially it contains all of the arcs within the CSP, as each
    # Variable in the constraint satisfaction problem could be arc-inconsistent, and may need to have its domain reduced
    # This initialization pushes BOTH arcs relating variables (x_i, x_j) onto the queue
    queue = [(c.v1, c.v2) for c in csp.constraints] + [(c.v2, c.v1) for c in csp.constraints]

    while queue:
        X_i, X_j = queue.pop()
        if remove_inconsistent_values(X_i, X_j, csp.get_relevant_constraint(X_i, X_j)):
            for X_k in get_neighbors(X_i, csp.constraints):
                queue.append((X_k, X_i))

    return csp
