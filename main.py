from chessgame import Board
import random
from Nconstructor import constructNGRam
from Move import Move
import time
from saving import save, load

PROFONDEUR = 9

# Game init
board = Board()


# Ngram Init
# multiModal = []
# for i in range(PROFONDEUR):
#     """
#     Avec une profondeur donnée, génère une liste de model de N-Gram sous la forme suivante:
#     1-Gram formé sur 100 Joueurs
#     2-Gram formé sur 90 joueurs
#     ...
#     N-Gram formé sur (90-N*10) Joueurs
#     """
#     print(f"Formation of the {i+1}-GRAM...")
#     multiModal.append(constructNGRam("data", 100-i*10, N=i+1))
# 
# for model in multiModal:
#     print(len(model.keys()[0]))
# 
# save(multiModal, "models/multiModal10Layer.pkl")
multiModal = load("models/multiModal10Layer.pkl")

def nextMove(input: list):
    """
    Génère une liste d'instance de Ngram de plusieurs tailles
    soit N une profondeur, génère une liste de N elements de profondeur, N, N-1, N-2, ..., 2, 1
    """
    print(f"input: {input}")
    prof = len(input)-1 # Profondeur 

    for level in range(prof, -1, -1):        # Bigger to smaller models
        if(tuple(input) in multiModal[level]):     # Input in the model
            responses = []                     
            for move in multiModal[level][tuple(input)]:                   # For every response to the input
                if(board.isLegalMove(board.convertPgn(move.PGN, Board.BLACK) )):  # If response is legal we add it to the response list
                    responses.append(move)
            if len(responses) > 0:
                return random.choice(responses)
        print(f"DECREASE: {level} -> {level-1}")
        input.pop()
    
    print("COMPUTER RESIGN.")
    exit()

        
        



# user play the white
gamelog = []
insideTree = True
running = True

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
    # time.sleep(1)

    gamelog.append(PGN)

    print(gamelog)
    
    PGN = nextMove(gamelog[-PROFONDEUR::]).PGN
    move = board.convertPgn(PGN, board.BLACK)
    board.play(move)

    gamelog.append(PGN)

    print("\n\n###########################")
    print(f"Computer played: {move.origin} -> {move.dest}")
    print(f"Current log: [[[ {gamelog} ]]]")
