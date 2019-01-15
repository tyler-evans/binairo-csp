class Vertex:

    def __init__(self, id):
        self.id = id
        self.connected_to = {}

    def add_neighbour(self, n):
        if n not in self.connected_to:
            self.connected_to[n] = True

    def get_id(self):
        return self.id

    def get_connections(self):
        return self.connected_to

    def __str__(self):
        return str(self.id + "connected to: " + [x.id for x in self.connected_to])
