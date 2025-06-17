class Node:

    BLACK = True
    WHITE = False

    def __init__(self, PGN):
        self.PGN = PGN
        self.whiteWon = 0
        self.blackWon = 0
        self.draw = 0
        self.gameCount = 0
        self.childs = {}

    def getPGN(self):
        return self.PGN
    
    def getChilds(self):
        return self.childs
    
    def addChilds(self, PGN, node):
        """
        Don't update the winning condition.
        """
        if not PGN in self.childs:
            self.childs[PGN] = node
        return self.childs[PGN]
    
    def updateWin(self, status):
        if(status == "white"):
          self.whiteWon += 1
        elif(status == "black"):
          self.blackWon += 1
        elif(status == "draw"):
          self.draw += 1
        self.gameCount += 1   

    def ratio(self, player=WHITE):
       if player == self.WHITE:
          return self.whiteWon/self.gameCount
       else:
          return self.blackWon/self.gameCount
    
    def getNextMove(self, history: list):
        """
        Take a list of move and return a move that matches the most
        the move history
        """
        if(len(history) == 0):
            exit("INVALID HISTORY")

        pNode = self    # Pointer to current node location
        while len(history) != 0:
            current = history.pop(0)
            if current in pNode.childs:
                pNode = pNode.childs[current]
        
        return pNode.PGN

