from chessgame import Board
import random
from constructor import constructNGRam
from Move import Move
import time
from Node import Node
from saving import save, load
import time



# Game init
board = Board()
start = time.time()
gram = constructNGRam("data", max=5000, N=5)
end = time.time()

print(f"Elapsed time: {end - start}s")


# save(gram, "models/gram.pkl")
# gram = load("models/gram.pkl")
        
# user play the white
gamelog = []
insideTree = True
running = True


def next():
    out = None
    max = -1
    PGN = gram.getNextMove(gamelog)        # List of move in the N-Gram
    for pgn in PGN:
        move = board.convertPgn(pgn, Board.BLACK)
        if board.isLegalMove(move) and gram.getChilds()[pgn].ratio(Node.BLACK) > max and gram.getChilds()[pgn].gameCount > 10:
            out = (move, pgn)
            max = gram.getChilds()[pgn].ratio(Node.BLACK)

    if out == None:
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
    move = board.convertPgn(PGN, board.WHITE)

    # Warn the player if move is illegal
    while not board.isLegalMove(move):
        print("INVALID MOVE")
        PGN = input("user: >>> ")
        move = board.convertPgn(PGN, board.WHITE)

    board.play(move)

    print(f"User player {move.origin} -> {move.dest}")
    board.display()

    gamelog.append(PGN)

    print(gamelog)
    
    move = next()
    board.play(move)

    board.display()

    gamelog.append(PGN)

    print("\n\n###########################")
    print(f"Computer played: {move.origin} -> {move.dest}")
    print(f"Current log: [[[ {gamelog} ]]]")
