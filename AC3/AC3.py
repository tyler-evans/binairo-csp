def neighbours(x_k, csp):
    x_k_neighbours = []
    for c in csp.constraints:
        if x_k in c:
            # All constraints are binary within the CSP -> if x_k is involved in a constraint and it's not the
            # first variable, it's the second variable
            x_k_neighbours.append(c.v1 if c.v1 != x_k else c.v2)
    return x_k_neighbours


def remove_inconsistent(x_i, x_j, constraint):
    removed = False

    # Value is guaranteed to be arc-consistent if it's already been assigned
    if x_i.value:
        return False

    # For each value in x_i, check to see if there is a value within x_j which "partners" with x_i's value and allows
    # it to remain in x_i's domain (arc-consistent) -> otherwise it needs to be removed
    for i in list(x_i.domain):
        x_i.value = i

        satisfies = False
        x_j_original = x_j.value

        # For each value in x_j, determine if there's a partner for the x_i value -> if not, remove i from x_i's domain
        for j in x_j.domain:
            x_j.value = j

            if bool(constraint):
                satisfies = True

            if satisfies:
                break

        x_j.value = x_j_original

        if not satisfies:
            x_i.domain.remove(i)
            removed = True

    return removed


# AC3 consistency algorithm created by Alan Mackworth which takes in a CSP and returns the CSP with possibly reduced
# domains which are all guaranteed to be arc-consistent
def ac3(csp):

    # These are all the arcs we have to check, initially it contains all of the arcs within the CSP, as each
    # Variable in the constraint satisfaction problem could be arc-inconsistent, and may need to have its domain reduced
    to_do_arcs = []

    for c in csp.constraints:
        # Push BOTH arcs relating variables (x_i, x_j) onto the queue for to_do_arcs
        x_i, x_j = c.variables[0], c.variables[1]
        to_do_arcs.append((x_i, x_j))
        to_do_arcs.append((x_j, x_i))

    # Keep looping until we are guaranteed that we don't have any inconsistent arcs within our domain (to_do_arcs will
    # empty)
    while to_do_arcs:
        x_i, x_j = to_do_arcs.pop()
        if remove_inconsistent(x_i, x_j, csp.get_arc(x_i, x_j)):
            for x_n in neighbours(x_i, csp):
                to_do_arcs.append((x_n, x_i))

    return csp
