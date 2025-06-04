from math import sqrt

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, pos):
        return sqrt((self.x - pos.x)**2 + (self.y - pos.y)**2)
    
    def equal(self, pos):
        return self.x == pos.x and self.y == pos.y