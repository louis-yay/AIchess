from pieces.piece import Piece

class Rook(Piece):
    def __init__(self, position, color):
        self.static = True
        super().__init__(position, color)

    def move(self, newPos):
        self.pos = newPos
        self.static = False

    def isStatic(self):
        return self.static
    
    def toString(self):
        return self.color + 'R'