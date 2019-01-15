from Board.Board import Board
from DataStructures.Graph import Graph
from DataStructures.Vertex import Vertex


def graph_vertex_test():
    g = Graph()
    for i in range(6):
        g.add_vertex(i)
    g.add_edge(0,1)
    g.add_edge(0,5)
    g.add_edge(1,2)
    g.add_edge(2,3)
    g.add_edge(3,4)
    g.add_edge(3,5)
    g.add_edge(4,0)
    g.add_edge(5,4)
    g.add_edge(5,2)
    for v in g:
        for w in v.get_connections():
            print("( %s , %s )" % (v.get_id(), w.get_id()))


def main():
    print('Reading board')
    board_data = Board.read_board(open('Data/simple_example.txt').readlines())
    board = Board(*board_data)

    print('\nBoard: ')
    print(board)
    assert not board.is_solution_board

    print('\nAvailable tiles: ', board.available_tiles)
    print('Valid moves: ', board.valid_moves)
    print('Fully constrained moves: ', board.fully_constrained_moves)
    print('Invalid moves: ', board.invalid_moves)

    print('\nSanity check: solving simple 4x4 example using fully constrained moves')
    while True:
        print(board, '\n')
        moves = board.fully_constrained_moves
        if moves:
            move = moves[0]
            board.set_tile(*move[0], move[1])
        else:
            break

    assert board.is_solution_board


if __name__ == "__main__":
    # main()
    graph_vertex_test()
