import os
from Board.Board import Board
from DataStructures.Graph import Graph
from DataStructures.Vertex import Vertex


def initialize_graph():
    graph = Graph()
    board_data = Board.read_board(open(os.getcwd() + '\\binairo-csp\\Data\\simple_example.txt').readlines())
    board = Board(*board_data)

    # Add all the vertices to the board given the input board array
    for r, row in enumerate(board._to_string_array()):
        for c, col in enumerate(row):
            # Add the vertex with "id" r+c with initial value based on input
            graph.add_vertex(r, c, col)

    # Add all valid corresponding neighbours as edges in the CSP graph
    for v in graph:
        r, c = v.get_row(), v.get_col()
        graph.add_edge(v.id, str(r - 1) + str(c)) if r - 1 > 0 else None
        graph.add_edge(v.id, str(r + 1) + str(c)) if r + 1 < len(row) else None
        graph.add_edge(v.id, str(r) + str(c - 1)) if c - 1 > 0 else None
        graph.add_edge(v.id, str(r) + str(c + 1)) if c + 1 < len(row) else None

    for v in graph:
            print(v)


def main():
    graph = initialize_graph()


if __name__ == "__main__":
    main()