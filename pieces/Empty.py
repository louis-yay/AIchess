from pieces.piece import Piece

class Empty(Piece):
    def __init__(self, position):
        super().__init__(position, None)

    def toString(self):
        return '00'

    