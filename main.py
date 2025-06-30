from chessgame import Board
import random
from constructor import constructDataSet
import time
import time
from math import inf
import copy



# Game init
board = Board()


def next():
    return None

# user play the white
gamelog = []
running = True


while running:
    board.display()
    # User play
    print("\n\n###########################")
    PGN = input("user: >>> ")   
    move = board.convertPgn(PGN)

    # Warn the player if move is illegal
    while not board.isLegalMove(move):
        print("INVALID MOVE")
        PGN = input("user: >>> ")
        move = board.convertPgn(PGN)


    print(f"User player {move.origin} -> {move.dest}")
    board.play(move)
    board.display()
    board.nextTurn()
    if board.isCheckMate():
        print("User Win.")
        exit()

    # log the game
    gamelog.append(PGN)
    print(gamelog)
    
    # Get next computer move
    PGN = next()
    move = board.convertPgn(PGN)
    print(f"Computer played: {move.origin} -> {move.dest}")
    board.play(move)
    gamelog.append(PGN)
    board.display()
    board.nextTurn()
    if board.isCheckMate():
        print("Computer win.")
        exit()

    print("\n\n###########################")
    print(f"Current log: [[[ {gamelog} ]]]")
