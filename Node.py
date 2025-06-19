import copy

class Node:
    """
    Define node object for the tree construction
    """
    BLACK = True
    WHITE = False

    def __init__(self, PGN):
        self.PGN = PGN       # Nom du coup
        self.whiteWon = 0    # Nombre de victoires blancs
        self.blackWon = 0    # Nombre de victoires noirs
        self.draw = 0        # Nombre d'égalité
        self.gameCount = 0   # Nombre de parties
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
        """
        Update winning status
        """
        if(status == "white"):
          self.whiteWon += 1
        elif(status == "black"):
          self.blackWon += 1
        elif(status == "draw"):
          self.draw += 1
        self.gameCount += 1   

    def ratio(self, player=WHITE):
       """
       Get winning ratio of the current player
       """
       if player == self.WHITE:
          return self.whiteWon/self.gameCount
       else:
          return self.blackWon/self.gameCount
    
    def getNextMove(self, gamelog: list):
        """
        Take a list of move and return a move that matches the most
        the move history
        """
        history = gamelog.copy()
        if(len(history) == 0):
            exit("INVALID HISTORY")

        pNode = copy.copy(self)    # Pointer to current node location
        while len(history) != 0:
            current = history.pop(0)
            if current in pNode.childs:
                pNode = pNode.childs[current]
            else:
               break
        
        return pNode.childs

