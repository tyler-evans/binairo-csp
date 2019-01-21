# assumes that the value of the other variable involved in the constraint has been binded
def exists_satisfactory_value(constraint, variable):
    for v in variable.domain:
        old_value = variable.value
        variable.value = v
        result = bool(constraint)
        variable.value = old_value
        if result:
            return True
    return False


def get_neighbors(variable, all_constraints):
    return [c.v1 if c.v1 != variable else c.v2 for c in all_constraints if variable in c]


def remove_inconsistent_values(X_i, X_j, constraint):
    removed = False
    if X_i.value: # already binded, do not need to constrain domain
        return False

    for x in list(X_i.domain):
        X_i.value = x
        if not exists_satisfactory_value(constraint, X_j):
            X_i.domain.remove(x)
            removed = True
    X_i.value = None

    return removed


def AC_3(csp):
    queue = [(c.v1, c.v2) for c in csp.constraints] + [(c.v2, c.v1) for c in csp.constraints]

    while queue:
        X_i, X_j = queue.pop()
        if remove_inconsistent_values(X_i, X_j, csp.get_relevant_constraint(X_i, X_j)):
            for X_k in get_neighbors(X_i, csp.constraints):
                queue.append((X_k, X_i))

    return csp
