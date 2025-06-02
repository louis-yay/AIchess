# 1. Create a tab from a game
data = []

with open("sample.pgn", "r") as file:

    # Read only the gameplay part
    
    reader = file.read().split("\n\n")
    for i in range(1, len(reader), 2):
        data.append(reader[i])

    # On remplace les retour à la ligne par des espaces
    # Split pour récupérer les coups un à un
    for i in range(len(data)):
        data[i] = data[i].replace("\n", " ")
        data[i] = data[i].split(" ")

final = [ [] for i in range(len(data))]

# Formatage d'un coup en retirant le numéro de manche
for i in range(len(data)):
    for move in data[i]:
        move = move.split(".")
        try:
            final[i].append(move[1])
        except IndexError:
            final[i].append(move[0])

print(final[0])