import math

def display_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    return [player, player, player] in win_conditions

def board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def minimax(board, depth, is_ai_turn, alpha, beta):
    if check_winner(board, 'X'):
        return 10 - depth
    if check_winner(board, 'O'):
        return depth - 10
    if board_full(board):
        return 0

    if is_ai_turn:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        return best_score
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        return best_score
        return best_score

def find_best_move(board):
    best_move = None
    best_score = -math.inf
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def tic_tac_toe():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    while True:
        display_board(board)
        
        # Player move
        try:
            row, col = map(int, input("Enter row and column (0-2): ").split())
            if board[row][col] != ' ':
                print("Invalid move. Try again.")
                continue
        except (ValueError, IndexError):
            print("Invalid input. Enter numbers between 0 and 2.")
            continue
        
        board[row][col] = 'O'
        if check_winner(board, 'O'):
            display_board(board)
            print("You win!")
            break
        if board_full(board):
            display_board(board)
            print("It's a draw!")
            break
        
        # AI move
        ai_move = find_best_move(board)
        if ai_move:
            board[ai_move[0]][ai_move[1]] = 'X'
            if check_winner(board, 'X'):
                display_board(board)
                print("AI wins!")
                break
        
        if board_full(board):
            display_board(board)
            print("It's a draw!")
            break

tic_tac_toe()
