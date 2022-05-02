# Author: Bence Racz
import os
import numpy as np
import copy as ctrlc

k = 3
depth = 2
currentPlayer = 0


# returns the position of a given player
def get_position(board, player):
    playerPosition = []
    for i in range(k):
        for j in range(k):
            if (player == 'player'):
                if (board[i][j] == 1):
                    playerPosition = [i, j]
            else:
                if (board[i][j] == 2):
                    playerPosition = [i, j]

    return playerPosition


# returns the possible moves on the board
def get_board_moves(board, player):
    moves = []
    playerPosition = []

    if (player == 'player'):
        playerPosition = get_position(board, 'player')
        playerMark = 1
        opponent = 'bot'
    else:
        playerPosition = get_position(board, 'bot')
        playerMark = 2
        opponent = 'player'

    for move in get_moves(board, player):
        auxBoard = ctrlc.deepcopy(board)
        auxBoard[playerPosition[0]][playerPosition[1]] = 0
        auxBoard[move[0]][move[1]] = playerMark
        for opponentMoves in get_moves(auxBoard, opponent):
            auxBoard2 = ctrlc.deepcopy(auxBoard)
            auxBoard2[opponentMoves[0]][opponentMoves[1]] = -1
            moves.append(auxBoard2)

    return moves


# This function clear the console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


# This function prints the board
def print_board(board):
    for i in range(k):
        for j in range(k):
            if (board[i][j] == 0):
                print(" _ ", end='')
            if (board[i][j] == -1):
                print(" X ", end='')
            if (board[i][j] == 1):
                print(" P ", end='')
            if (board[i][j] == 2):
                print(" B ", end='')

        print("\n")


# Returns if a move is valid
def is_valid_move(board, x, y):
    if (x < 0 or x >= k or y < 0 or y >= k or board[x][y] != 0):
        return False
    return True


# gets all the possible moves from the current state of the board
def get_moves(currentBoard, player):
    trans = [[1, 0], [1, 1], [1, -1], [0, 1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    move = []
    for i in range(k):
        for j in range(k):
            if (player == 'player'):
                if (currentBoard[i][j] == 1):
                    playerPosition = [i, j]
            else:
                if (currentBoard[i][j] == 2):
                    playerPosition = [i, j]

    for (x, y) in trans:
        if (is_valid_move(currentBoard, playerPosition[0] + x, playerPosition[1] + y)):
            move.append((playerPosition[0] + x, playerPosition[1] + y))

    return move


# evaluates the board
def evaluate_board(board):
    if (len(get_moves(board, 'player')) == 0):
        return -1
    if (len(get_moves(board, 'bot')) == 0):
        return 1
    return 0


# player moves it's player and blocks a tile
def player_move(board):
    # gets the current location of the player
    for i in range(k):
        for j in range(k):
            if (board[i][j] == 1):
                playerPosition = [i, j]

    newX = 100;
    newY = 100

    # move
    while (newX < 0 or newX >= k or newY < 0 or newY >= k or board[newX][newY] != 0):
        print("Please give the x coordinate of the field where you want to move: ", end='')
        newX = int(input())
        newX = newX - 1
        print("Please give the y coordinate of the field where you want to move: ", end='')
        newY = int(input())
        newY = newY - 1

    board[playerPosition[0]][playerPosition[1]] = 0
    board[newX][newY] = 1

    newX = 100;
    newY = 100

    # block
    while (newX < 0 or newX >= k or newY < 0 or newY >= k or board[newX][newY] != 0):
        print("Please give the x coordinate of the field where you want to block: ", end='')
        newX = int(input())
        newX = newX - 1
        print("Please give the y coordinate of the field where you want to block: ", end='')
        newY = int(input())
        newY = newY - 1

    board[newX][newY] = -1

    return board


# heuristic evaluation
def heuristic_eval(board):
    max = len(get_moves(board, 'bot'))
    min = len(get_moves(board, 'player'))
    return max - 2 * min


# min max algorithm
def minimax(board, isMax, depth, alfa, beta):
    # maxEval = evaluate_board(board)
    maxEval = heuristic_eval(board)
    if (depth == 0):
        return maxEval

    depth = depth - 1

    if isMax:
        maxEval = -np.inf
        for move in get_board_moves(board, 'bot'):
            eval = minimax(move, False, depth, alfa, beta)
            maxEval = max(eval, maxEval)
            alfa = max(maxEval, alfa)
            if alfa >= beta:
                return maxEval
        return maxEval

    else:
        minEval = np.inf
        for move in get_board_moves(board, 'player'):
            eval = minimax(move, True, depth, alfa, beta)
            minEval = min(minEval, eval)
            alfa = min(maxEval, alfa)
            if alfa >= beta:
                return minEval
        return minEval


# moves the bot and blocks on the map
def bot_move(board):
    moves = get_board_moves(board, 'bot')
    maxEval = -np.inf
    optimalMove = []

    for move in moves:
        currentEval = minimax(board, True, depth, -np.inf, np.inf)
        if currentEval > maxEval:
            maxEval = currentEval
            optimalMove = move

    return optimalMove


# changes the player
def change_player():
    global currentPlayer
    if (currentPlayer == 1):
        currentPlayer = 2
    else:
        currentPlayer = 1


# runs the game
def play(board):
    global depth
    steps = 0
    while (True):
        steps = steps + 1
        clearConsole()
        print_board(board)

        state = evaluate_board(board)

        if (state == -1):
            break

        if (state == 1):
            break

        if (currentPlayer == 2):
            board = player_move(board)
        else:
            board = bot_move(board)

        print_board(board)
        change_player()

        if (steps == 4):
            depth = depth + 1
            steps = 0


# places the players on their starting positions
def place_players(mode, board):
    if (mode == 2):
        board[0][int(k / 2)] = 2  # Bot
        board[k - 1][int(k / 2)] = 1  # Player
    else:
        board[0][int(k / 2)] = 1  # Player
        board[k - 1][int(k / 2)] = 2  # Bot

    play(board)


# creates the board
def create_board(mode):
    board = [[] for i in range(k)]
    for i in range(k):
        for j in range(k):
            board[i].append(0)
    place_players(mode, board)


# sets the first players turn
def set_first_player(mode):
    global currentPlayer
    if (mode == 1):
        currentPlayer = 2  # player starts
    else:
        currentPlayer = 1  # bot starts

    create_board(mode)


# This function will start the game
def start_game():
    mode = 0
    print("-------------Welcome to the game-------------")

    while (mode not in [1, 2]):
        print("Please select a game mode: \n")
        print(" Type 1 if you want the player to start")
        print(" Type 2 if you want the bot to start\n")
        mode = int(input("Please enter your choice: "))

    set_first_player(mode)


def main():
    start_game()
    return


if __name__ == '__main__':
    main()
