import os
from Move import Move
from saving import load, save
from chessgame import Board
from Node import Node

# Maximal asbtraction version

def constructNGRam(DIR, max=1000, N=1):
    """
    Build a N-Gram with N arg
    The N-Gram is represented by a tree where the depth represent the N of the N-Gram
    The max arg speficy how many game you want to use into the N-Gram build
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
            if(len(move) > 2 and (not ('=' in move)) and move[0] != 'O'):   
                if(move[-3] in ['R', 'N', 'B', 'Q', 'K']):  # for figures
                    move = move[-3:]
                else:                                       # for Pawns
                    move = move[-2:]
            elif(len(move) > 2 and '=' in move and move[0] != 'O'):
                move = move[-4:]

            final[i].append(move)
        final[i].append(data[i][-1])

    del data

    return _build(final, N)




def _build(dataSet, N):
    """
    Take formated dataset and N, the depth of the N-Gram
    Return a tree version of the N-Gram
    """
    output = Node(PGN = None)
    # For every move in every game
    for game in dataSet:
        for moveIndex in range(len(game)-N):   
            pNode = output     

            # For every set of size N
            for pgnIndex in range(moveIndex, moveIndex+N):

                # We try to find a branch that exist
                try:
                    pNode = pNode.getChilds()[game[pgnIndex]]

                # If not, we build the new brand
                except KeyError:
                    pNode = pNode.addChilds(game[pgnIndex], Node(game[pgnIndex+1]))

                # Update winning rate
                match game[-1]:
                    case "1-0":
                        pNode.updateWin("white")
                    case "0-1":
                        pNode.updateWin("black")
                    case "1/2-1/2":
                        pNode.updateWin("draw")  


    return output
