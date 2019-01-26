import numpy as np
import os


def read_board(path):
    lines = open(path).readlines()
    lines = map(lambda x: x.strip(), lines)

    data = np.array([list(x) for x in lines if x][2:-1])
    n = data.shape[0]

    return data, n


def read_individual_board(lines):
    lines = map(lambda x: x.strip(), lines)

    data = np.array([list(x) for x in lines if x][2:-1])
    n = data.shape[0]

    return data, n


def read_boards_from_file(file_name):
    separator = "#End"
    all_boards = []

    if os.path.isfile(file_name):
        with open(file_name) as board_file:
            data = []
            for line in board_file.readlines():
                data.append(line)
                if separator in line:
                    # Read in the board and compute it's dimensionality
                    board, n = read_individual_board(data)
                    assert board.shape == (n,n)

                    data.clear()
                    all_boards += [board]
    else:
        print("File: {} not found".format(file_name))

    return all_boards
