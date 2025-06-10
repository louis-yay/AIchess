from saving import save, load
from Node import Node
from constructor import constructTree
from chessgame import Board
from random import choice


tree = constructTree("data", max=100)
# save(tree, "models/70PlayerTree.pkl")
# tree = load("models/70PlayerTree.pkl")


# Game init
board = Board()


# user play the white
gamelog = ""
current = tree
playerStart = True
insideTree = True
running = True

while running:
    # TODO Check winning conditions
    board.display()
    # User play
    print("\n\n###########################")
    # print(f"Available move for player: {current.getChilds().keys()}")
    PGN = input("user: >>> ")   

    print(current.getChilds())

    move = board.convertPgn(PGN, not playerStart)
    board.play(move)

    try:
        current = current.getChilds()[PGN]
    except KeyError:
        insideTree = False
        print("Left the tree.")

    print(f"User player {move.origin} -> {move.dest}")
    # gamelog += f"{PGN} "
    
    print(current.getChilds())

    # Computer play
    if insideTree:
        PGN = current.getNextMove()
        move = board.convertPgn(PGN, playerStart)
        board.play(move)
        current = current.getChilds()[PGN]
        
    else:
        move = choice(board.getLegalMoves('B'))
        board.play(move)

    # gamelog += f"{PGN} "

    print("\n\n###########################")
    print(f"Computer played: {move.origin} -> {move.dest}")
    print(f"Current log: [[[ {gamelog} ]]]")
        


    


