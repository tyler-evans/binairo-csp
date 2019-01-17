import numpy as np


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
