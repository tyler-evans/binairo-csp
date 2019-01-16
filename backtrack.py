import os
from Board.Board import Board
from DataStructures.Graph import Graph
from DataStructures.Utility import Utility

utility = Utility()


def initialize_board():
    board_data = Board.read_board(open(os.getcwd() + '\\binairo-csp\\Data\\simple_example.txt').readlines())
    board = Board(*board_data)
    return board


def initialize_graph_from_board(board):
    graph = Graph()
    graph.dimensions = board.n

    # Add all the vertices to the CSP graph given the input board array
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

    for v in graph.unassigned:
        print(v)

    return graph


def solve_back_tracking_random_node(graph):
    return solve_back_tracking_random_node_recursive(graph)


def solve_back_tracking_random_node_recursive(graph):
    if graph.unassigned is []:
        graph.result = True
        return graph

    # Select a random node from the graph's currently unassigned nodes
    random_node = graph.unassigned[utility.random_number(0, len(graph.unassigned)-1)]

    for value in graph.domain:
        # Assign the random_node a value in the domain range [0 or 1]
        random_node.set_value(value)

        # Check all of the constraints ensuring the validity of this value allocation
        graph.check_equivalent_zeroes_and_ones_constraint(random_node.row, random_node.col)
        graph.check_max_two_of_the_same_adjacent_values_constraint(random_node.row, random_node.col, value)
        graph.check_row_and_column_uniqueness_constraint()

    return graph.result


def main():
    board = initialize_board()
    graph = initialize_graph_from_board(board)

    solved_graph = solve_back_tracking_random_node(graph)


if __name__ == "__main__":
    main()