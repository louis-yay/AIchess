from position import Position

class Piece:
    def __init__(self, position, color):
        self.pos = Position(position[0], position[1])
        self.color = color

    def getName(self):
        return self.name
    
    def getPosition(self):
        return self.pos
    
    def getColor(self):
        return self.color
    
    def move(self, newPos):
        self.pos = newPos