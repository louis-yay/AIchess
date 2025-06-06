from pieces.piece import Piece

class Bishop(Piece):

    def __init__(self, position, color):
        super().__init__( position, color)

    def toString(self):
        return self.color + 'B'
    
