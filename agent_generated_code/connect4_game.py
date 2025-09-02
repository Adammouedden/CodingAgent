import tkinter as tk
import numpy as np
import random
import time

# --- Game Constants ---
BOARD_ROWS = 6
BOARD_COLS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
EMPTY = 0

BLUE = "#0000FF"
BLACK = "#000000"
RED = "#FF0000"
YELLOW = "#FFFF00"
WHITE = "#FFFFFF"

# --- Game Logic Functions ---
def create_board():
    return np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[BOARD_ROWS - 1][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(BOARD_ROWS):
        if board[r][col] == EMPTY:
            return r
    return -1 # Should not happen if is_valid_location is true

def check_win(board, piece):
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
    return False

def is_board_full(board):
    for c in range(BOARD_COLS):
        if is_valid_location(board, c):
            return False
    return True

# --- GUI Functions ---
def draw_board(canvas, board):
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS):
            # Draw blue rectangles for the board background
            canvas.create_rectangle(c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, (c + 1) * SQUARESIZE, (r + 1) * SQUARESIZE + SQUARESIZE, fill=BLUE, outline=BLUE)

            # Draw empty circles (holes)
            canvas.create_oval(c * SQUARESIZE + 5, r * SQUARESIZE + SQUARESIZE + 5, (c + 1) * SQUARESIZE - 5, (r + 1) * SQUARESIZE + SQUARESIZE - 5, fill=BLACK)

    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS):
            # Draw pieces on top of the holes if present
            if board[BOARD_ROWS - 1 - r][c] == PLAYER1_PIECE:
                canvas.create_oval(c * SQUARESIZE + 5, r * SQUARESIZE + SQUARESIZE + 5, (c + 1) * SQUARESIZE - 5, (r + 1) * SQUARESIZE + SQUARESIZE - 5, fill=RED)
            elif board[BOARD_ROWS - 1 - r][c] == PLAYER2_PIECE:
                canvas.create_oval(c * SQUARESIZE + 5, r * SQUARESIZE + SQUARESIZE + 5, (c + 1) * SQUARESIZE - 5, (r + 1) * SQUARESIZE + SQUARESIZE - 5, fill=YELLOW)
    canvas.update()

# --- Main Game Loop ---
def play_game(canvas, board, status_label):
    game_over = False
    turn = random.randint(0, 1) # Randomly decide who starts

    def make_move():
        nonlocal game_over, turn
        if game_over:
            return

        if turn == 0: # Player 1 (Red)
            player_piece = PLAYER1_PIECE
            status_label.config(text="Player 1 (Red) Turn")
        else: # Player 2 (Yellow)
            player_piece = PLAYER2_PIECE
            status_label.config(text="Player 2 (Yellow) Turn")

        # Simple AI: choose a random valid column
        valid_cols = [c for c in range(BOARD_COLS) if is_valid_location(board, c)]
        if not valid_cols:
            game_over = True
            status_label.config(text="Game Over! It's a Draw!")
            return

        col = random.choice(valid_cols)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player_piece)
        draw_board(canvas, board)

        if check_win(board, player_piece):
            game_over = True
            status_label.config(text=f"Player {turn + 1} Wins!")
        elif is_board_full(board):
            game_over = True
            status_label.config(text="Game Over! It's a Draw!")
        else:
            turn = 1 - turn # Switch turn
            if not game_over: # Schedule next move if game is still on
                root.after(1000, make_move) # 1-second delay for next move

    # Start the game loop after a short delay
    root.after(100, make_move)

# --- Main Application Setup ---
if __name__ == "__main__":
    board = create_board()

    root = tk.Tk()
    root.title("Connect 4")
    root.resizable(False, False)

    # Frame for game board and status
    game_frame = tk.Frame(root)
    game_frame.pack()

    status_label = tk.Label(game_frame, text="", font=("Arial", 18), fg=BLACK)
    status_label.pack(pady=10)

    canvas = tk.Canvas(game_frame, width=BOARD_COLS * SQUARESIZE, height=BOARD_ROWS * SQUARESIZE + SQUARESIZE, bg=BLUE)
    canvas.pack()

    # Initial board draw
    draw_board(canvas, board)

    # Start the auto-play game
    play_game(canvas, board, status_label)

    root.mainloop()