from pieces.piece import Piece

class Queen(Piece):

    def __init__(self, position, color):
        super().__init__(position, color)

    def toString(self):
        return self.color + 'Q'