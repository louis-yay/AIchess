class Movement:

    def __init__(self, origin='', dest='', promotion=None):
        self.origin = origin
        self.dest = dest
        self.promotion = promotion
        
    def toTuple(self):
        return self.origin,self.dest,self.promotion
    
    def equal(self, move):
        return self.origin == move.origin and self.dest == move.dest and self.promotion == move.promotion