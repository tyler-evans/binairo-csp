import numpy as np
from collections import Counter

try: # please forgive
    import matplotlib.pyplot as plt
except:
    pass


class Board:
    
    def __init__(self, zeros_bool_arr, ones_bool_arr):
        self.n = zeros_bool_arr.shape[0]
        self.zeros = zeros_bool_arr
        self.ones = ones_bool_arr
        
    def copy(self):
        return Board(self.zeros.copy(), self.ones.copy())

    # set tile i, j, to 1 if ones else 0
    # intended to only be called from the result of `valid_moves`
    def set_tile(self, i, j, ones):
        self._get_mask(ones)[i,j] = True

    # return boolean if placing a 0 or 1 (according to `ones`) is a valid move
    def is_valid_move(self, i, j, ones):
        row, col = self._get_row_col(i, j, ones)
        row[j], col[i] = True, True
        return self._check_array(row) and self._check_array(col) and self._has_all_unique()


    @property
    def is_solution_board(self):
        full_board = len(self.available_tiles) == 0

        valid_rows_ones = np.all([self._check_array(row) for row in self.ones])
        valid_rows_zeros = np.all([self._check_array(row) for row in self.zeros])

        valid_cols_ones = np.all([self._check_array(row) for row in self.ones.T])
        valid_cols_zeros = np.all([self._check_array(row) for row in self.zeros.T])

        is_unique = self._has_all_unique()

        conditions = [full_board, valid_rows_ones, valid_rows_zeros, valid_cols_ones, valid_cols_zeros, is_unique]
        return all(conditions)


    # returns all empty tiles
    @property
    def available_tiles(self):
        return list(zip(*np.where(~(self.ones | self.zeros))))

    # returns all valid moves in format: 
    # [((i, j), val), ...] where i,j indices of tile and val (0 or 1) is what to place
    @property
    def valid_moves(self):             
        return [(tile, val) for tile in self.available_tiles for val in [0,1] if self.is_valid_move(*tile, val)]

    # return moves that correspond to tiles with only one possible choice.
    # in the same format as `valid_moves`
    @property
    def fully_constrained_moves(self):
        counts = Counter([move[0] for move in self.valid_moves])
        return [move for move in self.valid_moves if counts[move[0]] == 1]

    # for debugging
    @property
    def invalid_moves(self):
        # for debugging
        # I think this is a superset of the complement (w.r.t. state) of the fully constrained moves
        return [(t, v) for t in self.available_tiles for v in [0,1] if (t, v) not in self.valid_moves]

    # get the bitmap for either the 1's or 0's
    def _get_mask(self, ones):
        return self.ones if ones else self.zeros

    # extract the i row and j col of the indicated bitmap
    def _get_row_col(self, i, j, ones):
        mask = self._get_mask(ones).copy()
        return mask[i,:], mask[:,j]

    def _check_array(self, arr):
        return not self._has_unbalance(arr) and not self._has_3_adjacent(arr)

    def _has_unbalance(self, arr_1d):
        return np.sum(arr_1d) > (self.n // 2)

    def _has_3_adjacent(self, arr_1d):
        arr_1d = arr_1d.reshape(-1)
        result = arr_1d

        for i in range(1,3):
            result = np.bitwise_and(result, np.pad(arr_1d, (i,0), 'constant')[:-i])

        return np.any(result)

    def _has_all_unique(self):
        # TODO (maybe simplify) and test this a bit
        unique_rows, unique_cols = True, True
        
        completed_rows = np.all(self.ones | self.zeros, axis=1)
        if np.any(completed_rows):
            unique_rows = np.all(np.unique(self.ones[completed_rows, :], axis=0, return_counts=True)[1] == 1)
        
        completed_cols = np.all(self.ones.T | self.zeros.T, axis=1)
        if np.any(completed_cols):
            unique_cols = np.all(np.unique(self.ones.T[completed_cols, :], axis=0, return_counts=True)[1] == 1)
            
        return unique_rows and unique_cols

    def _to_string_array(self):
        str_board = np.full((self.n, self.n), '.')
        str_board[self.zeros] = '0'
        str_board[self.ones] = '1'
        return str_board

    def __str__(self):
        return '\n'.join([''.join(x) for x in self._to_string_array()])

    def show_board(self):
        try:
            plt.axis('off')
            plt.table(cellText=self._to_string_array(), loc='center', cellLoc='center', bbox=[0,0,1,1])
            plt.show()
        except:
            print('Failed to plot board')

    @staticmethod
    def read_board(lines):
        header = lines[0]
        footer = lines[-1]

        board_dims = tuple([int(x) for x in lines[1].split()])

        board = np.array([list(x.strip()) for x in lines[2:-2]], dtype=object)
        assert board_dims == board.shape

        zeros = board == '0'
        ones = board == '1'

        return zeros, ones
