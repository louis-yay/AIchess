import os
from Move import Move
from saving import load, save
from chessgame import Board
from Node import Node

# Maximal asbtraction version

def constructNGRam(DIR, max=1000, N=1):
    """
    Construit un arbre de décision étant donnée un dossier contenant une liste de fichier .pgn
    """
    # 1. Create a tab from a game
    data = []
    index = 0

    for file in os.listdir(DIR):
        if index < max:
            with open(DIR + "/" + file, "r", errors='ignore') as file:
                index += 1
                #print(file)
                # Read only the gameplay part

                reader = file.read().split("\n\n")
                for i in range(1, len(reader), 2):
                    data.append(reader[i])
            del reader


    # On remplace les retour à la ligne par des espaces
    # Split pour récupérer les coups un à un

    for i in range(len(data)):
        # print(f'Extraction des coups: {round(i/len(data)*100)}%')
        
        data[i] = data[i].replace("\n", " ")
        data[i] = data[i].replace("+", "")      # Don't keep the chess note
        data[i] = data[i].replace("x", "")      # Don't keep take info
        data[i] = data[i].split(" ")
        while "" in data[i]:
            data[i].remove("")
        

    final = [ [] for i in range(len(data))]

    # Formatage d'un coup en retirant le numéro de manche
    for i in range(len(data)):
        for j in range(len(data[i])-1):
            move = data[i][j].split(".")

            try:
                move = move[1]
            except IndexError:
                move = move[0]

            if(len(move) > 2 and (not ('=' in move)) and move[0] != 'O'):   
                if(move[-3] in ['R', 'N', 'B', 'Q', 'K']):  # figures
                    move = move[-3:]
                else:                                       # Pawn
                    move = move[-2:]
            elif(len(move) > 2 and '=' in move and move[0] != 'O'):
                move = move[-4:]

            final[i].append(move)
        final[i].append(data[i][-1])

    del data

    output = Node(PGN=None)
    return _build(final, output, N)



def _build(dataSet, output, depth, history = []):
    if depth > 0:
        for game in dataSet:
            for i in range(len(game)-1-len(history)):     # for move in game
                next = Node(game[i])
                winUpdate = [next]
                isCombValid = True
                for checkIndex in range(len(history)):
                    if game[i+checkIndex] != history[checkIndex]:
                        isCombValid = False

                if isCombValid:
                    if game[i] in output.getChilds():
                        winUpdate.append(output)
                    else:
                        output.addChilds(game[i], next)
                    for elt in winUpdate:
                            match game[-1]:
                                case "1-0":
                                    elt.updateWin("white")
                                case "0-1":
                                    elt.updateWin("black")
                                case "1/2-1/2":
                                    elt.updateWin("draw")
                    winUpdate.clear()
                    history.append(game[i+len(history)])
                    _build(dataSet, next, depth-1, history)
                    history = []

    return output


tree = constructNGRam("data", 1, 2)
for elt in tree.getChilds().keys():
    print(f"MOVE: {elt} -> {tree.getChilds[elt].ratio()}%")
