from chess import Board, Move
import chess
import torch
import numpy as np
from dataset import boardToRep, letterToNum
from chessnet import chessNet


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
model = chessNet().to(device)
model.load_state_dict(torch.load('chessNet.pth', weights_only=True, map_location=torch.device('cpu')))

@torch.no_grad()  # Disable gradient calculation for efficiency
def predict(x):
    """
    x:  board representation
    returns: move of origin and destination 
    """
    output = model(x)  # Shape: (1, 2, 8, 8)
    output = torch.softmax(output, dim=2)  #  normalize across rows
    return output.squeeze(0)  # Remove batch dimension: (2, 8, 8)


def check_mate_single(board):
    """
    Check is checkMate is possible in one move.
    If so, return the move
    """
    board = board.copy()
    legal_moves = list(board.legal_moves)

    for move in legal_moves:
        board.push_uci(str(move))
        if board.is_checkmate():
            move = board.pop()
            return move
        board.pop() # undo last move

def distribution_over_moves(vals):
    """
    Make bigger gap between high probalility move and low probability move.
    """
    probs = np.array(vals)
    probs = np.exp(probs)
    probs = probs / probs.sum()
    probs = probs ** 3
    probs = probs / probs.sum()
    return probs

def chooseMove(board, color):

    legalMoves = list(board.legal_moves)

    # Check if mate is possible in one move
    move = check_mate_single(board)
    if move is not None:
        return move
    
    # Predict next move from the board
    x = torch.Tensor(boardToRep(board)).float() # .to('cuda')
    if color == chess.BLACK:
        x *= 1
    x = x.unsqueeze(0)
    move = predict(x)

    # Distribute from prediction: orgin move's probability over legal moves
    vals = []
    froms = [str(legal_move)[:2] for legal_move in legalMoves]
    froms = list(set(froms))
    for origin in froms:
        val = move[0,:,:][8-int(origin[1]), letterToNum[origin[0]]]
        vals.append(val)

    # increase probablity gap & choose origin.
    probs = distribution_over_moves(vals)
    originChoosen = str(np.random.choice(froms, size=1, p=probs)[0])[:2]

    # Distribute probablites over move's hypothetic destinations
    vals = []
    for legal_move in legalMoves:
        origin = str(legal_move)[:2]
        if origin == originChoosen:
            dest = str(legal_move)[2:]
            val = move[1,:,:][8- int(dest[1]), letterToNum[dest[0]]]
            vals.append(val)
        else:
            vals.append(0)

    # chose the move with the biggest prob
    choosenMove = legalMoves[np.argmax(vals)]
    return choosenMove


board = Board()

while not board.is_game_over():

    # COMPUTER TURN
    move = chooseMove(board, chess.WHITE)
    if move == None:
        print("Computer Resign.")
        exit()
    board.push(move)
    print(f"Computer play {move}")
    print(board)

    # PLAYER TURN
    while not board.is_legal(move):
        strmove = input("Choose move in format [origin][dest]\n>>> ")
        move = Move(chess.SQUARES[chess.parse_square(strmove[:2])], chess.SQUARES[chess.parse_square(strmove[2:])])

    print(f"You played {move}")
    board.push(move)
    print(board)



print(f"{board.result()}")



board = Board()
move = chooseMove(board, chess.WHITE)
print(board.is_legal(Move(chess.E2, chess.E5)))
print(board.san(Move(chess.E2, chess.E4)))
board.push(Move(chess.E2, chess.E4))
print(board.variation_san(board.move_stack))


print(chess.SQUARES[chess.parse_square('e4')] == chess.E4)
