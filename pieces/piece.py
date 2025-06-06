class Piece:
    def __init__(self, name, position, color):
        self.name = name
        self.pos = position
        self.color = color

    def getName(self):
        return self.name
    
    def getPosition(self):
        return self.pos
    
    def move(self, newPos):
        self.pos = newPos