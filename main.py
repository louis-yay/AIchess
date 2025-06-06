from tree.saving import save, load
from tree.Node import Node
from tree.constructor import constructTree
from chessgame import Board
from random import choice


# tree = constructTree("sample")
# save(tree, "models/50PlayerTree.pkl")
tree = load("sample/50PlayerTree.pkl")


# Game init
board = Board()


# user play the white
gamelog = ""
current = tree
insideTree = True
running = True

while running:
    # TODO Check winning conditions
    board.display()
    # User play
    print("\n\n###########################")
    # print(f"Available move for player: {current.getChilds().keys()}")
    PGN = input("user: >>> ")   

    move = board.convertPgn(PGN, False)
    board.play(move.origin, move.dest)

    try:
        current = current.getChilds()[PGN]
    except KeyError:
        insideTree = False
        print("Left the tree.")

    print(f"User player {move.origin} -> {move.dest}")
    gamelog += f"{PGN} "
    

    # Computer play
    if insideTree:
        PGN = current.getNextMove()
        move = board.convertPgn(PGN, True)
        board.play(move.origin, move.dest)
        current = current.getChilds()[PGN]
        
    else:
        move = choice(board.getLegalMoves('B'))
        board.play(move.origin, move.dest)

    print("\n\n###########################")
    print(f"Computer played: {move.origin} -> {move.dest}")
    print(f"Current log: [[[ {gamelog} ]]]")
        


    


