from chessgame import Board
from random import choice



# Game init
board = Board()


# user play the white
gamelog = ""
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
    board.play(move)

    print(f"User player {move.origin} -> {move.dest}")
    gamelog += f"{PGN} "
    
    move = choice(board.getLegalMoves('B'))
    board.play(move)

    print("\n\n###########################")
    print(f"Computer played: {move.origin} -> {move.dest}")
    print(f"Current log: [[[ {gamelog} ]]]")
        


    


