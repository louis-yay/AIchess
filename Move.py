class Move:

    BLACK = True
    WHITE = False

    def __init__(self, PGN):
        self.PGN = PGN
        self.whiteWon = 0
        self.blackWon = 0
        self.draw = 0
        self.gameCount = 0

    def updateWin(self, status):
        if(status == "white"):
          self.whiteWon += 1
        elif(status == "black"):
          self.blackWon += 1
        elif(status == "draw"):
          self.draw += 1
        self.gameCount += 1    

    def equal(self, move):
      return self.PGN == move.PGN 
    
    def ratio(self, player=WHITE):
       if player == self.WHITE:
          return self.whiteWon/self.gameCount
       else:
          return self.blackWon/self.gameCount
    