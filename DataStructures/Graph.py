from DataStructures.Vertex import Vertex

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Class used to model the Constraint Satisfaction Problem (CSP) graph containing vertices representing
cells of the Binairo board and edges representing the connected vertices to which we must assign values
such that the constraints of "Binairo" hold and a solution can be achieved which satisfies all constraints.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Graph:

    def __init__(self):
        self.dimensions = -1
        self.domain = ["0", "1"]
        self.vertices = {}
        self.unassigned = []
        self.assigned = []
        self.result = False

    def add_vertex(self, row, col, value):
        id = str(row) + str(col)
        if id not in self.vertices:
            v = Vertex(row, col, value)
            self.vertices[id] = v
            if value is not 0 or value is not 1:
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
        same_adjacent_values = 0

        if row - 1 >= 0 and self.vertices[str(row - 1) + str(col)].value == value:
            same_adjacent_values += 1
        if row + 1 < self.dimensions and self.vertices[str(row + 1) + str(col)].value == value:
            same_adjacent_values += 1
        if col - 1 >= 0 and self.vertices[str(row) + str(col - 1)].value == value:
            same_adjacent_values += 1
        if col + 1 < self.dimensions and self.vertices[str(row) + str(col + 1)].value == value:
            same_adjacent_values += 1

        return same_adjacent_values <= 2

    # Ensure that all rows and columns are unique within the CSP graph
    def check_row_and_column_uniqueness_constraint(self, row, col):
        satisfies_constraint = True

        # Ensure that the row and column the node exists in is completely filled with values, otherwise
        # there is no need to further check this constraint since it is guaranteed to be unique due to unassigned values
        for i in range(self.dimensions):
            if self.vertices[str(row) + str(i)].value == "_":
                return satisfies_constraint

        for i in range(self.dimensions):
            if self.vertices[str(i) + str(col)].value == "_":
                return satisfies_constraint

        # Build a list of all rows and columns
        rows_and_cols = []

        for i in range(self.dimensions):
            rows_and_cols.append([self.vertices[str(i)+str(j)].value for j in range(self.dimensions)])
            rows_and_cols.append([self.vertices[str(j)+str(i)].value for j in range(self.dimensions)])

        unique_rows_and_cols = []
        for value in rows_and_cols:
            if value not in unique_rows_and_cols:
                unique_rows_and_cols.append(value)

        # A non-unique row or column will violate this property
        if len(unique_rows_and_cols) < len(rows_and_cols):
            satisfies_constraint = False

        return satisfies_constraint






