puzzle = [
[0, 0, 0, 2, 6, 0, 7, 0, 1],
[6, 8, 0, 0, 7, 0, 0, 9, 0],
[1, 9, 0, 0, 0, 4, 5, 0, 0],
[8, 2, 0, 1, 0, 0, 0, 4, 0],
[0, 0, 4, 6, 0, 2, 9, 0, 0],
[0, 5, 0, 0, 0, 3, 0, 2, 8],
[0, 0, 9, 3, 0, 0, 0, 7, 4],
[0, 4, 0, 0, 5, 0, 0, 3, 6],
[7, 0, 3, 0, 1, 8, 0, 0, 0]
]


def print_board(board):
    for i in range(0,9):
        if i%3 == 0:
            print("- "*12,end="-\n")
        for j in range(0,9):
            if j%3 == 0:
                print("|", end=" ")
            if puzzle[i][j] == 0:
                print(" ", end=" ")
            else:
                print(puzzle[i][j],end=" ")
            if(j==8):
                print("|",end="")
        print("\n", end="")

print_board(puzzle)


def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    
    for i in range(9):
        if board[i][col] == num:
            return False
    
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def lcv(board, row, col):
    valid_values = []
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            count = 0
           
            for i in range(9):
                if board[row][i] == 0 and is_valid(board, row, i, num):
                    count += 1
            for i in range(9):
                if board[i][col] == 0 and is_valid(board, i, col, num):
                    count += 1
            
            valid_values.append((num, count))
   
    valid_values.sort(key=lambda x: x[1])
    return [x[0] for x in valid_values]

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve(board):
    empty_cell = find_empty(board)
    if not empty_cell:
        return True  
    row, col = empty_cell

    for num in lcv(board, row, col):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0 

    return False



solve(puzzle)

print("\n\n\n\n")

print_board(puzzle)