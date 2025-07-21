from chessgame import Board
from constructor import constructDataSet, VectorToMove
from model import Model
import torch

# Game init
board = Board()

model = Model()
model.load_state_dict(torch.load('20000Games1369EpochsModel.pt'))

def next():
    val = model.forward(torch.FloatTensor(board.makeVector()))
    vector = [False for i in range(len(val))]
    vector[val.argmax().item()] = True
    move = VectorToMove(vector)
    print(f"{move.origin} -> {move.dest}")
    exit()

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
