import os
from Node import Node

def constructTree(DIR, max=1000):
    """
    Construit un arbre de décision étant donnée un dossier contenant une liste de fichier .pgn
    """
    # 1. Create a tab from a game
    data = []
    index = 0

    for file in os.listdir(DIR):
        with open(DIR + "/" + file, "r", errors='ignore') as file:
            #print(file)
            # Read only the gameplay part

            reader = file.read().split("\n\n")
            for i in range(1, len(reader), 2):
                if(index<max):
                    data.append(reader[i])
                    index += 1
        del reader


    # On remplace les retour à la ligne par des espaces
    # Split pour récupérer les coups un à un


    for i in range(len(data)):
        # print(f'Extraction des coups: {round(i/len(data)*100)}%')
        
        data[i] = data[i].replace("\n", " ")
        data[i] = data[i].replace("+", "")      # Don't keep the chess note
        data[i] = data[i].split(" ")
        if "" in data[i]:
            data[i].remove("")

    final = [ [] for i in range(len(data))]


    # Formatage d'un coup en retirant le numéro de manche
    for i in range(len(data)):
        for j in range(len(data[i])-1):
            move = data[i][j].split(".")
            try:
                final[i].append(move[1])
            except IndexError:
                final[i].append(move[0])


    # Définition de l'arbre
    tree = Node()

    # Final = Liste de toutes les parties
    # Game = Liste de coup
    # Contruction de l'arbre

    for game in final:
        current = tree
        for n in range(len(game)):
            if (game[n] in current.getChilds()):
                current = current.getChilds()[game[n]]
            else:
                current = current.addChild(game[n], Node())
            if (game[-1] == "1-0"):
                current.updateWin("white")
            elif (game[-1] == "0-1"):
                current.updateWin("black")
            else:
                current.updateWin("draw")
    return tree