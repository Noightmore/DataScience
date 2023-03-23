def print_queen_board(horiz_size, vert_size, queen_x, queen_y):
    # Create empty board
    board = []
    for i in range(vert_size):
        board.append(['.'] * horiz_size)

    # Mark valid moves (horizontal, vertical, and diagonal)
    for y in range(vert_size):
        for x in range(horiz_size):
            if x == queen_x or y == queen_y or abs(x - queen_x) == abs(y - queen_y):
                board[y][x] = '*'

    # Mark queen position
    board[queen_y][queen_x] = 'D'

    # Print board
    for row in board:
        print(' '.join(row))
