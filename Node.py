class Node:
  def __init__(self, whiteWon=0, blackWon=0, draw=0):
    self.gameCount = 0
    self.whiteWon = whiteWon
    self.blackWon = blackWon
    self.draw = draw
    self.childs = {}

  def getCount(self):
    return self.gameCount
  
  def getWhite(self):
    return self.whiteWon
  
  def getBlack(self):
    return self.blackWon
  
  def getDraw(self):
    return self.draw
  
  def getRatio(self, white = True):
    if(white):
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
    max = 0
    next = None
    for move in self.childs:
      if(move.getRatio() > max):
        next = move
        max = move.getRatio()
    return next

  def updateWin(self, status):
    if(status == "white"):
      self.whiteWon += 1
    elif(status == "black"):
      self.blackWon += 1
    elif(status == "draw"):
      self.draw += 1
    self.gameCount += 1      