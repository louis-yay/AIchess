# 1. Create a tab from a game
with open("sample.pgn", "r") as file:

    # Read only the gameplay part
    data = file.read().split("\n\n")[1]

    # On remplace les retour à la ligne par des espaces
    data = data.replace("\n", " ")

    # Split pour récupérer les coups un à un
    data = data.split(" ")

final = []

# Formatage d'un coup en retirant le numéro de manche
for move in data:
    move = move.split(".")
    try:
        final.append(move[1])
    except IndexError:
        final.append(move[0])

print(final)