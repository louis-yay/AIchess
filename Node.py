import copy

class Node:
    """
    Define node object for the tree construction
    """
    BLACK = True
    WHITE = False

    def __init__(self, board):
        self.board = board       # Nom du coup
        self.childs = []

    def getBoard(self):
        return self.board
    
    def getChilds(self):
        return self.childs

    def addChild(self, board):
        """
        Don't update the winning condition.
        """
        for child in self.childs:
            if child.board == board:
                return child

        node = Node(board)
        self.childs.append(node)
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

