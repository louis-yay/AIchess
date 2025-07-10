from torch.utils.data import Dataset
import numpy as np
import chess
import re

class ChessDataset(Dataset):
    def __init__(self, data, size= 40000):
        super(ChessDataset, self).__init__()
        self.games = data['AN']
        self.data = data
        self.size = size
        self.letterToNum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self.numToLetter = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

    def __len__(self):
        return self.size
    
    def __getitem__(self, index):
        """
        Pick a random move from a random game
            -> Don't keep index
            -> smaller loading time
        """
        gameIndex = np.random.randint(self.games.shape[0])
        randomGame = self.data['AN'].values[gameIndex]
        moves = self.formatList(randomGame)
        gameStateIndex = np.random.randint(len(moves)-1)
        nextMove = moves[gameStateIndex]
        moves = moves[:gameStateIndex]
        board = chess.Board()
        for move in moves:
            board.push_san(move)
        x = self.boardToRep(board)
        y = self.moveToRep(nextMove, board)
        if gameStateIndex % 2 == 1:
            x *= -1
        return x,y
    
    def createLayer(self, board, type):
        """
        Transform a board, considering a piece type 
        into a specific board layer (matrice)
        """

        # Clean the board form everything we don't need
        s = str(board)
        s = re.sub(f'[^{type}{type.upper()} \n]', '.', s)
        s = re.sub(f'{type}', '-1', s)
        s = re.sub(f'{type.upper()}', '1', s)
        s = re.sub(f'\.', '0', s)

        boardMatrice = []
        for row in s.split('\n'):
            row = row.split(' ')
            row = [int(x) for x in row]
            boardMatrice.append(row)

        return np.array(boardMatrice)


    def boardToRep(self, board):
        pieces = ['p', 'r', 'n', 'b', 'q', 'k']
        layers = []
        for piece in pieces:
            layers.append(self.createLayer(board,piece))
        board_rep = np.stack(layers)
        return board_rep

    def moveToRep(self, move, board):
        """
        Transform a move into 2 matrices
        One indication the origin position of the move
        The second the destination of the move
        """


        board.push_san(move).uci()
        move = str(board.pop())

        originLayer = np.zeros((8,8))
        originRow = 8-int(move[1])
        originColumn = self.letterToNum[move[0]]
        originLayer[originRow, originColumn] = 1


        destLayer = np.zeros((8,8))
        destRow = 8-int(move[3])
        destColumn = self.letterToNum[move[2]]
        destLayer[destRow, destColumn] = 1

        return np.stack([originLayer, destLayer])

    def formatList(self, s):
        return re.sub('\d*\. ', '', s).split(' ')[:-1]