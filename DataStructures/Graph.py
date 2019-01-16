from DataStructures.Vertex import Vertex

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Class used to model the Constraint Satisfaction Problem (CSP) graph containing vertices representing
cells of the Binairo board and edges representing the connected vertices to which we must assign values
such that the constraints of "Binairo" hold and a solution can be achieved which satisfies all constraints.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Graph:

    def __init__(self):
        self.dimensions = -1
        self.domain = ['0', '1']
        self.vertices = {}
        self.unassigned = []
        self.assigned = []

    def add_vertex(self, row, col, value):
        id = str(row) + str(col)
        if id not in self.vertices:
            v = Vertex(row, col, value)
            self.vertices[id] = v
            if value == ".":
                self.unassigned.append(v)

    def get_vertex(self, id):
        return self.vertices[id] if id in self.vertices else None

    def add_edge(self, e1, e2):
        if e1 not in self.vertices:
            self.add_vertex(e1)
        if e2 not in self.vertices:
            self.add_vertex(e2)
        self.vertices[e1].add_neighbour(self.vertices[e2])
        self.vertices[e2].add_neighbour(self.vertices[e1])

    def get_vertices(self):
        return self.vertices.keys()

    def __iter__(self):
        return iter(self.vertices.values())

    def display_graph(self):
        for i in range(self.dimensions):
            row = []
            for j in range(self.dimensions):
                row.append(self.vertices[str(i) + str(j)].value)
            print(row)
        print()

    # Ensure that a row and column do not have more than n/2 "0's" or "1's" assigned
    def check_equivalent_zeroes_and_ones_constraint(self, row, col):
        num_ones_row, num_zeroes_row, num_ones_col, num_zeroes_col = 0, 0, 0, 0

        for i in range(self.dimensions):
            if self.vertices[str(row) + str(i)].value == "1":
                num_ones_row += 1
            if self.vertices[str(row) + str(i)].value == "0":
                num_zeroes_row += 1
            if self.vertices[str(i) + str(col)].value == "1":
                num_ones_col += 1
            if self.vertices[str(i) + str(col)].value == "0":
                num_zeroes_col += 1

        satisfies_constraint = True

        if num_ones_row > self.dimensions // 2 or num_zeroes_row > self.dimensions // 2 or \
                num_ones_col > self.dimensions // 2 or num_zeroes_col > self.dimensions // 2:
            satisfies_constraint = False

        return satisfies_constraint

    # Ensure that no more than two "0's" or "1's" are placed adjacent to one another
    def check_max_two_of_the_same_adjacent_values_constraint(self, row, col, value):
        above_rows, below_rows, right_cols, left_cols = 0, 0, 0, 0

        for i in range(1, 3):
            if row - i >= 0 and self.vertices[str(row - 1) + str(col)].value == value and self.vertices[str(row - i) + str(col)].value == value:
                above_rows += 1

            if row + i < self.dimensions and self.vertices[str(row + 1) + str(col)].value == value and self.vertices[str(row + i) + str(col)].value == value:
                below_rows += 1

            if col - i >= 0 and self.vertices[str(row) + str(col-1)].value == value and self.vertices[str(row) + str(col - i)].value == value:
                left_cols += 1

            if col + i < self.dimensions and self.vertices[str(row) + str(col+1)].value == value and self.vertices[str(row) + str(col + i)].value == value:
                right_cols += 1

        # Add up the row + cols values and add 1 because of the node's value we're checking
        max_similar_adjacency_values = max(above_rows+below_rows, left_cols+right_cols)

        # A result of 2 or more indicates 2 other values adjacent to the node have the same value -> return False
        # A result of 1 or less indicates a max of 1 other adjacent node shares the value -> return True
        return max_similar_adjacency_values <= 1

    # Ensure that all rows and columns are unique within the CSP graph
    def check_row_and_column_uniqueness_constraint(self, row, col):
        satisfies_constraint = True

        # Ensure that the row and column the node exists in is completely filled with values, otherwise
        # there is no need to further check this constraint since it is guaranteed to be unique due to unassigned values
        for i in range(self.dimensions):
            if self.vertices[str(row) + str(i)].value == ".":
                return satisfies_constraint

        for i in range(self.dimensions):
            if self.vertices[str(i) + str(col)].value == ".":
                return satisfies_constraint

        # Build a list of all rows and columns
        rows_and_cols = []

        for i in range(self.dimensions):
            rows_and_cols.append([self.vertices[str(i)+str(j)].value for j in range(self.dimensions)])
            rows_and_cols.append([self.vertices[str(j)+str(i)].value for j in range(self.dimensions)])

        # A non-unique row or column will trigger an early return indicating non-uniqueness
        for value in rows_and_cols:
            if "." not in value and rows_and_cols.count(value) > 1:
                return False

        return satisfies_constraint

