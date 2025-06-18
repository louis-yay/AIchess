class Movement:
    """
    Define chess board movement
    PosA -> Pos2
        Example: Re2 -> Re7
    """
    def __init__(self, piece = '', origin='', dest='', promotion=None):
        self.piece = piece
        self.origin = origin
        self.dest = dest
        self.promotion = promotion
        
    def toTuple(self):
        return self.origin,self.dest,self.promotion
    
    def equal(self, move):
        return self.origin == move.origin and self.dest == move.dest and self.promotion == move.promotion