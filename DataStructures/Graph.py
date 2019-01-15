from DataStructures.Vertex import Vertex

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Class used to model the Constraint Satisfaction Problem (CSP) graph containing vertices representing
cells of the Binairo board and edges representing the connected vertices to which we must assign values
such that the constraints of "Binairo" hold and a solution can be achieved which satisfies all constraints.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Graph:

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, row, col, value):
        id = str(row) + str(col)
        if id not in self.vertices:
            v = Vertex(row, col, value)
            self.vertices[id] = v

    def get_vertex(self, id):
        return self.vertices[id] if id in self.vertices else None

    def add_edge(self,e1,e2):
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
