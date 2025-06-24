import os
from saving import load, save
from chessgame import Board
from Node import Node
from math import inf

# Maximal asbtraction version

def constructGraph(DIR, max=1000):
    """
    Return a dictionnarie of index for the graph nodes AND, the graph itselve
    """
    # 1. Create a tab from a game
    data = []   # <- a list of game
    index = 0   # index to count the number of game needed

    # Extract every game needed from files 
    for file in sorted(os.listdir(DIR)):
        with open(DIR + "/" + file, "r", errors='ignore') as file:
            index += 1

            # Read only the moves part of the game
            reader = file.read().split("\n\n")
            for i in range(1, len(reader), 2):
                if index < max:
                    data.append(reader[i])
                    index += 1
        del reader


    # Remplace every \n by space
    # Split the string by space to get move one to one
    for i in range(len(data)):
        data[i] = data[i].replace("\n", " ")
        data[i] = data[i].replace("+", "")      # Don't keep the check note
        data[i] = data[i].replace("x", "")      # Don't keep take note
        data[i] = data[i].split(" ")
        while "" in data[i]:
            data[i].remove("")
        

    final = [ [] for i in range(len(data))]

    # Formating move
    for i in range(len(data)):
        for j in range(len(data[i])-1):
            move = data[i][j].split(".")

            # Remove turn number
            try:
                move = move[1]
            except IndexError:
                move = move[0]

            # Remove abiguiti correction from PGN notation
            # if(len(move) > 2 and (not ('=' in move)) and move[0] != 'O'):   
            #     if(move[-3] in ['R', 'N', 'B', 'Q', 'K']):  # for figures
            #         move = move[-3:]
            #     else:                                       # for Pawns
            #         move = move[-2:]
            # elif(len(move) > 2 and '=' in move and move[0] != 'O'):
            #     move = move[-4:]

            final[i].append(move)
        final[i].append(data[i][-1])

    return _build(final)

def _build(dataSet):
    board = Board()
    outDict = {
        "1-0": Node("WWIN"),
        "0-1": Node("BWIN"),
        "1/2-1/2": Node("DRAW")
    }
    outGraph = Node(tuple(board.makeVector()))
    outDict[tuple(board.makeVector())] = outGraph

    for game in dataSet:
        board.resetGrid()
        board.currentPlayer = Board.WHITE
        ptGraph = outGraph  # graph pointer
        for i in range(len(game)):
            if game[i] in ["0-1", "1-0", "1/2-1/2"]:
                ptGraph.addChild(game[i], outDict[game[i]])
            else:
                if not board.isLegalMove(board.convertPgn(game[i])):
                    board.display()
                    print(board.isLegalMove(board.convertPgn(game[i])))
                    raise ValueError
                board.play(board.convertPgn(game[i]))
                # board.display()
                board.nextTurn()
                vector = tuple(board.makeVector())
                if vector in list(outDict.keys()):

                    # Make connexion between current and new
                    ptGraph = ptGraph.addChild(game[i], outDict[vector])
                else:   
                    # Make connexion from current node to new node
                    ptGraph = ptGraph.addChild(game[i], Node(vector))
                    outDict[vector] = ptGraph
    
    return (outGraph, outDict)


graph, dic = constructGraph("data", 100)
print(len(dic))


# # TODO the algo
# # TODO: faire des tests sur des cas particulier (linéaire, boucle, etc...)
# def getDistance(graph, dic: dict, dest = "WWIN"):
#     for key in dic:
#         dic[key].distance = inf
#         dic[key].visited = False
#     graph.distance = 0
#     return _parcours(graph)
# 
# 
# def _parcours(graph, dest = "WWIN"):
#     print(type(graph.board))
#     if graph.board == "WWIN" or graph.board == "BWIN" or graph.board == "DRAW":
#         return graph.distance
#     for childKey in graph.getChilds():
#         graph.getChilds()[childKey].distance = graph.distance + 1
#         _parcours(graph.getChilds()[childKey])
# 
# graph, dic = constructGraph("data", 10)
# print(getDistance(graph, dic))