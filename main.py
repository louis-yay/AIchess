from chessgame import Board
import random
from NGram.constructor import constructNGRam
import time
from NGram.Node import Node
from saving import save, load
import time



# Game init
board = Board()
DEPTH = 7

gram = constructNGRam("data", 5000, 3)

# Loading N-Gram from file, 50000 game, depth of 7.
# gram = load("models/gram.pkl")
        
# user play the white
gamelog = []
insideTree = True
running = True


def next(log, depth):
    """
    Return the next move to be played by the computer
    """
    out = None
    max = -1
    PGN = gram.getNextMove(gamelog[::-depth])        # List of move in the N-Gram
    for pgn in PGN:
        move = board.convertPgn(pgn)

        # We only consider move legal and found at least 10 times in the dataset
        if board.isLegalMove(move) and gram.getChilds()[pgn].ratio(Node.BLACK) > max and gram.getChilds()[pgn].gameCount > 10:
            out = (move, pgn)
            max = gram.getChilds()[pgn].ratio(Node.BLACK)

    if out == None:
        if depth > 1:
            return next(log, depth-1)
        else:
            print("Computer Resign")
            exit()

    gamelog.append(out[1])
    return out[0]
            



while running:
    # TODO Check winning conditions
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

    # log the game
    gamelog.append(PGN)
    print(gamelog)
    
    # Get next computer move
    move = next(gamelog, DEPTH)

    print(f"Computer played: {move.origin} -> {move.dest}")
    board.play(move)
    board.display()
    board.nextTurn()

    print("\n\n###########################")
    print(f"Current log: [[[ {gamelog} ]]]")
