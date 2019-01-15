from Board.Board import Board


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
