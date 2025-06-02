import os
from Node import Node

DATADIR = "data"

# 1. Create a tab from a game
data = []

print("#################################################")
print("LECTURE DES FICHIERS")
#for file in os.listdir(DATADIR):
with open("sample.pgn", "r", errors='ignore') as file:
    print(file)
    # Read only the gameplay part
    
    reader = file.read().split("\n\n")
    for i in range(1, len(reader), 2):
        data.append(reader[i])


# On remplace les retour à la ligne par des espaces
# Split pour récupérer les coups un à un
print("#################################################")
print("EXTRACTION DES COUPS:")

for i in range(len(data)):
    print(f'Extraction des coups: {round(i/len(data)*100)}%')
    data[i] = data[i].replace("\n", " ")
    data[i] = data[i].split(" ")

final = [ [] for i in range(len(data))]


print("#################################################")
print("FORMATAGE DES COUPS:")

# Formatage d'un coup en retirant le numéro de manche
for i in range(len(data)):
    print(f'Formatage des coups: {round(i/len(data)*100)}%')
    for move in data[i]:
        move = move.split(".")
        try:
            final[i].append(move[1])
        except IndexError:
            final[i].append(move[0])


# Définition de l'arbre
tree = Node()
i = 0

# Contruction de l'arbre
for game in final:
    current = tree
    i += 1
    for move in game:
        print(f"Contruction de l'arbre: {i/len(data)*100}%")
        if (game[-1] == "1-0"):
            current.updateWin("white")
        elif (game[-1] == "0-1"):
            current.updateWin("black")
        else:
            current.updateWin("draw")
        if (move in current.getChilds()):
            current = current.getChilds()[move]
        else:
            current = current.addChild(move, Node())

# Game
# user play the whites
current = tree
while True:
    print(current.getChilds())
    # User play
    move = input("Enter move using PGN format: ")
    current = current.getChilds()[move]

    # Computer play
    play = current.getNextMove()
    current = current.getChilds()[play]
    print(f"played: {play}")
