from chessgame import Board
import random
from constructor import constructGraph
import time
from Node import Node
from saving import save, load
import time



# Game init
board = Board()

# Loading N-Gram from file, 50000 game, depth of 7.
# gram = load("models/gram.pkl")
        
# user play the white
gamelog = []
running = True


graph, index = constructGraph("data", max=50)

def next():
    print(len(index.keys()))
    if(tuple(board.makeVector()) in list(index.keys())):
        return list(index[tuple(board.makeVector())].getChilds().keys())[0]
    else:
        print("Computer resign.")
        exit()
            



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
    PGN = next()
    move = board.convertPgn(PGN)
    print(f"Computer played: {move.origin} -> {move.dest}")
    board.play(move)
    board.display()
    board.nextTurn()

    print("\n\n###########################")
    print(f"Current log: [[[ {gamelog} ]]]")
