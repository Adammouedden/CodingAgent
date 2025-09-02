import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def is_board_full(board):
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            return False
    return True

def main():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    while not game_over:
        # Player 1 turn
        if turn == 0:
            try:
                col = int(input("Player 1 (You) Make your Selection (0-6): "))
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 6.")
                continue
            if 0 <= col <= 6 and is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    print_board(board)
                    print("Player 1 (You) wins!")
                    game_over = True
                elif is_board_full(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True

            else:
                print("Invalid column or column is full. Try again.")
                continue

        # Player 2 turn
        else:
            try:
                col = int(input("Player 2 (AI) Make your Selection (0-6): ")) # Can be replaced with AI logic later
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 6.")
                continue
            if 0 <= col <= 6 and is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    print_board(board)
                    print("Player 2 (AI) wins!")
                    game_over = True
                elif is_board_full(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True

            else:
                print("Invalid column or column is full. Try again.")
                continue

        print_board(board)

        if not game_over: # Only switch turn if game is not over yet
            turn = (turn + 1) % 2

if __name__ == "__main__":
    main()