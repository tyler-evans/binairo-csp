"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Representation of a cell within the game of Binairo which is used to track neighbouring cells and this cell's value
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Vertex:

    def __init__(self, row, col, value):
        self.id = str(row) + str(col)
        self.row = row
        self.col = col
        self.value = value
        self.connected_to = {}

    def add_neighbour(self, n):
        if n not in self.connected_to:
            self.connected_to[n] = True

    def get_id(self):
        return self.id

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_value(self):
        return self.value

    def get_connections(self):
        return self.connected_to

    def __str__(self):
        return str("[" + str(self.row) + str(self.col) + "](" + str(self.value) + ") connected to: " + str([x.id for x in self.connected_to]))
