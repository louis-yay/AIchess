class Node:

  WHITE = True
  BLACK = False

  def __init__(self, whiteWon=0, blackWon=0, draw=0):
    self.gameCount = 0
    self.whiteWon = whiteWon
    self.blackWon = blackWon
    self.draw = draw
    # self.turn = self.BLACK
    self.childs = {}

  def getCount(self):
    return self.gameCount
  
  def getWhite(self):
    return self.whiteWon
  
  def getBlack(self):
    return self.blackWon
  
  def getDraw(self):
    return self.draw
  
  def getRatio(self, turn):
    if(turn == self.WHITE):
      return self.whiteWon/self.gameCount
    return self.blackWon/self.gameCount
  
  def getChilds(self): 
    return self.childs
  
  def setChilds(self, newChilds):
    self.childs = newChilds

  def addChild(self, key, value):
    self.childs[key] = value
    return value
  
  def getNextMove(self):
    max = -1
    next = None
    for move in self.childs.keys():
      if(self.childs[move].getRatio(self.BLACK) > max):
        next = move
        max = self.childs[move].getRatio(self.BLACK)
    return next

  def updateWin(self, status):
    if(status == "white"):
      self.whiteWon += 1
    elif(status == "black"):
      self.blackWon += 1
    elif(status == "draw"):
      self.draw += 1
    self.gameCount += 1      