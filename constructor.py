import os
from Move import Move
from saving import load, save
from chessgame import Board

# Maximal asbtraction version

def constructNGRam(DIR, max=1000, N=1):
    """
    Construit un arbre de décision étant donnée un dossier contenant une liste de fichier .pgn
    """
    # 1. Create a tab from a game
    data = []
    index = 0

    print("#################################################")
    print("LECTURE DES FICHIERS")
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
    print("#################################################")
    print("EXTRACTION DES COUPS")

    for i in range(len(data)):
        # print(f'Extraction des coups: {round(i/len(data)*100)}%')
        
        data[i] = data[i].replace("\n", " ")
        data[i] = data[i].replace("+", "")      # Don't keep the chess note
        data[i] = data[i].replace("x", "")      # Don't keep take info
        data[i] = data[i].split(" ")
        while "" in data[i]:
            data[i].remove("")
        

    final = [ [] for i in range(len(data))]

# 32. Rf1 Qf1
    print("#################################################")
    print("FORMATAGE DES COUPS")

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

    print("#################################################")
    print("CONSTRUCTION DU 1-GRAM")
    output = {}


# Dict PGN -> Move Object
    index = 0
    for game in final:
        index += 1
        # print(f"{index/len(final)*100}%")
        for i in range(len(game) - (N+1)):

            # Define the key
            current = []
            for n in range(N):
                current.append(game[i+n])
            
            current = tuple(current)

            # Move to play
            next = Move(game[i+N])
            match game[-1]:
                case "1-0":
                    next.updateWin("white")
                case "0-1":
                    next.updateWin("black")
                case "1/2-1/2":
                    next.updateWin("draw")
            
            if(current in output):
                exist = False
                for elt in output[current]:
                    if next.equal(elt):
                        elt.whiteWon += next.whiteWon
                        elt.blackWon += next.blackWon
                        elt.draw += next.draw
                        elt.gameCount += next.gameCount
                        exist = True
                        break

                if not exist:
                    output[current].append(next)
            else:
                output[current] = [next]

    return output


PROFONDEUR = 5

unGram = constructNGRam("data", 1, N=PROFONDEUR)
# save(unGram, "models/100PlayerUnGram.pkl")
print(len(unGram))

# unGram = load("models/100PLayerUnGram.pkl")


while True:
    key = []
    try:
        for i in range(PROFONDEUR):
            key.append(input(f"Coups N°{i+1}\n>>>"))
        print(f"AVAILABLE MOVE: {len(unGram[tuple(key)])}")
        for move in unGram[tuple(key)]:
            print(f"{move.PGN}: {move.ratio(Move.WHITE)*100}%")

    except KeyError:
        print("Move not in files.")