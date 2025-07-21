import os
import matplotlib.pyplot as plt
from Node import Node
from constructor import constructNGRam

# The test here is to build 2 type of NGram,
# One base on the classic database and another on a specific
# The specific database class the games by oppening
# This study show that the custrom database is useful
# Only when we read 1 game of each file, and the corresponding
# Amount is the default database.
# For every bigger amount, the basic database show better result.

def size(tree):
    if tree.getChilds() != {}:
        return 1 + sum([size(tree.getChilds()[elt]) for elt in tree.getChilds().keys()])
    return 1


def tester(DIR, nbOfGame = 10, nbOfFile = 5, N=1):
    data = []
    index = 0
    """
    Here we take 10 games of every oppening file
    """
    for file in sorted(os.listdir(DIR)):
        if nbOfFile < 0:
            break
        with open(DIR + "/" + file, "r", errors='ignore') as file:

            # Read only the gameplay part
            reader = file.read().split("\n\n")
            for i in range(1, nbOfGame*2, 2):
                data.append(reader[i])
                break
        del reader
        index = 0
        nbOfFile-=1

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
    return _build(final, N)




def _build(dataSet, N):
    output = Node(PGN = None)
    for game in dataSet:
        for moveIndex in range(len(game)-N):   
            pNode = output     # For every move in every game
            for pgnIndex in range(moveIndex, moveIndex+N):
                try:
                    pNode = pNode.getChilds()[game[pgnIndex]]
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


sizeTest = {}
sizeNormal = {}

for i in range(25, 245, 25):    # the range of file
    game = 15    # The nb of game to study in each file
    sizeTest[i] = size(tester(DIR="openning", nbOfGame=game, nbOfFile=i, N=8))

    # We study the equivalent amount of game in the default "data" dataset
    sizeNormal[i] = size(constructNGRam(DIR="data", max=game*i, N=8))

plt.plot(sizeNormal.keys(), sizeNormal.values(), label="Normal dataset")
plt.plot(sizeTest.keys(), sizeTest.values(), label="Custom dataset")
plt.legend()
plt.xlabel("Number of game")
plt.ylabel("Size of the 1-Gram")

plt.show()


{
    "coupA": ['reponse1', 'reponse2', 'reponse3'],
    "coupB": ['reponse1', 'reponse3', 'reponse4']
}