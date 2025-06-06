from piece import Piece

class Rook(Piece):
    def __init__(self, name, position, color):
        self.static = True
        super().__init__(name, position, color)

    def move(self, newPos):
        self.pos = newPos
        self.static = False

    def isStatic(self):
        return self.static
    
