from pieces.piece import Piece

class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__( position, color)

    def toString(self):
        return self.color + 'P'

    