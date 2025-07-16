import chess
import torch
import numpy as np
from dataset import boardToRep, moveToRep, createLayer, letterToNum, numToLetter
from chessnet import chessNet
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = chessNet() # .to(device)
model.load_state_dict(torch.load('chessNet.pth', weights_only=True))

@torch.no_grad()  # Disable gradient calculation for efficiency
def predict(x):
    """
    x: torch.Tensor of shape (1, 6, 8, 8) — single board representation
    returns: torch.Tensor of shape (2, 8, 8) — predicted origin and destination probabilities
    """
    output = model(x)  # Shape: (1, 2, 8, 8)
    output = torch.softmax(output, dim=2)  # Optional: normalize across rows
    return output.squeeze(0)  # Remove batch dimension: (2, 8, 8)


def check_mate_single(board):
    board = board.copy()
    legal_moves = list(board.legal_moves)

    for move in legal_moves:
        board.push_uci(str(move))
        if board.is_checkmate():
            move = board.pop()
            return move
        _ = board.pop()

def distribution_over_moves(vals):
    probs = np.array(vals)
    probs = np.exp(probs)
    probs = probs / probs.sum()
    probs = probs ** 3
    probs = probs / probs.sum()
    return probs

def chooseMove(board, color):

    legalMoves = list(board.legal_moves)

    move = check_mate_single(board)
    if move is not None:
        return move
    
    x = torch.Tensor(boardToRep(board)).float() # .to('cuda')
    if color == chess.BLACK:
        x *= 1
    x = x.unsqueeze(0)
    move = predict(x)

    vals = []
    froms = [str(legal_move)[:2] for legal_move in legalMoves]
    froms = list(set(froms))
    for from_ in froms:
        val = move[0,:,:][8-int(from_[1]), letterToNum[from_[0]]]
        vals.append(val)

    probs = distribution_over_moves(vals)

    originChoosen = str(np.random.choice(froms, size=1, p=probs)[0])[:2]

    vals = []
    for legal_move in legalMoves:
        from_ = str(legal_move)[:2]
        if from_ == originChoosen:
            dest = str(legal_move)[2:]
            val = move[1,:,:][8- int(dest[1]), letterToNum[dest[0]]]
            vals.append(val)
        else:
            vals.append(0)

    choosenMove = legalMoves[np.argmax(vals)]
    return choosenMove

board = chess.Board()
move = chooseMove(board, chess.WHITE)
print(move)