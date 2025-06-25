from chessgame import Board
import random
from constructor import constructGraph
import time
from Node import Node
from saving import save, load
import time
from math import inf
import copy



# Game init
board = Board()

graph, dic = constructGraph("data", max=50)

# user play the white
gamelog = []
running = True

def getDistance(graph, dic: dict, dest):
    tmpDic = {}
    for key in dic.keys():
        tmpDic[key] = [dic[key], False]
    return _parcours(graph, tmpDic, dest)


def _parcours(graph, dic, dest):
    if graph.board == dest:
        return 1 #dic[graph.board][1]
    for childKey in graph.getChilds():
        child = graph.getChilds()[childKey]
        if(not dic[child.board][1]):    # this node as not been visited
            dic[child.board][1] = True  # Set the node as visited
            # dic[child.board][1] = dic[graph.board][1] + 1 # Update distance as current distance + 1 
            return 1 + _parcours(child, dic, dest)
    return 0

def next():
    
    move = None
    vector = tuple(board.makeVector())
    if vector in dic:
        current = dic[vector]  # Get the current board state node

        # Sorted list of all current node's child by distance to current player's team
        issues = sorted([(key, getDistance(current.getChilds()[key], dic, board.currentPlayer)) for key in current.getChilds()], key=lambda tup:tup[1])
        while issues != []:
            if(board.isLegalMove(board.convertPgn(issues[0][0]))):
                return issues[0][0]
            issues.pop(0)

    print("Computer resign.")
    exit()


while running:
    # TODO Check winning conditions
    board.display()
    # User play
    print("\n\n###########################")
    PGN = input("user: >>> ")   
    move = board.convertPgn(PGN)

    # Warn the player if move is illegal
    while not board.isLegalMove(move):
        print("INVALID MOVE")
        PGN = input("user: >>> ")
        move = board.convertPgn(PGN)


    print(f"User player {move.origin} -> {move.dest}")
    board.play(move)
    board.display()
    board.nextTurn()
    if board.isCheckMate():
        print("User Win.")
        exit()

    # log the game
    gamelog.append(PGN)
    print(gamelog)
    
    # Get next computer move
    PGN = next()
    move = board.convertPgn(PGN)
    print(f"Computer played: {move.origin} -> {move.dest}")
    board.play(move)
    gamelog.append(PGN)
    board.display()
    board.nextTurn()
    if board.isCheckMate():
        print("Computer win.")
        exit()

    print("\n\n###########################")
    print(f"Current log: [[[ {gamelog} ]]]")
