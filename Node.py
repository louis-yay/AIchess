import copy

class Node:
    """
    Define node object for the tree construction
    """
    BLACK = True
    WHITE = False

    def __init__(self, board):
        self.board = board       # Nom du coup
        self.childs = {}        # move -> new board


    def getBoard(self):
        return self.board
    
    def getChilds(self):
        return self.childs

    def addChild(self, pgn, node):
        """
        Don't update the winning condition.
        """
        if pgn in list(self.childs.keys()):
            return self.childs[pgn]

        self.childs[pgn] = node
        return node
               

    def ratio(self, player=WHITE):
       """
       Get winning ratio of the current player
       """
       return 
    
    def getNextMove(self, gamelog: list):
        """
        Take a list of move and return a move that matches the most
        the move history
        """
        return 1

