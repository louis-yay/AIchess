import os
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from model import Model
from chessgame import Board
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def pgnToVector(PGN):
    """
    Return a vector the following form:
    [
        a1: False,
        a2: False,
        a3: False,
        ...
        a8: False,
        ...
        Qf3: True,
        etc...
    ]
    """
    out = [PGN == 'O-O', PGN=='O-O-O']
    for piece in ['', 'R', 'N', 'B', 'Q', 'K']:
        for i in range(8):
            for j in range(1, 9):
                out.append(PGN == f"{piece}{chr(ord('a')+i)}{j}")

    return out
                
def vectorToPgn(vector):
    if vector[0]:
        return 'O-O'
    elif vector[1]: 
        return 'O-O-O'
    vector = vector[2:]

    pieces = ['', 'R', 'N', 'B', 'Q', 'K']
    for pieceIndex in range(len(pieces)):
        for i in range(8):
            for j in range(8):
                if(vector[(pieceIndex*8*8)+i*8+j]):
                    return f"{pieces[pieceIndex]}{chr(ord('a')+i)}{j+1}"



def constructDataSet(DIR, max=1):
    """
    we want a list:
    [
        [VECTOR]: Move to play,
        [VECTOR]: move to play,
        ...
        [VECTOR]: Move to play,
        [VECTOR]: move to play,
    ]
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

    # Randomise datset game's order.
    random.shuffle(data)

    # Remplace every \n by space
    # Split the string by space to get move one to one
    for i in range(len(data)):
        data[i] = data[i].replace("\n", " ")
        data[i] = data[i].replace("+", "")      # Don't keep the check note
        data[i] = data[i].replace("x", "")      # Don't keep take note
        data[i] = data[i].split(" ")
        while "" in data[i]:
            data[i].remove("")
        

    formated = [ [] for i in range(len(data))]

    # Formating move
    for i in range(len(data)):
        for j in range(len(data[i])-1):
            move = data[i][j].split(".")

            # Remove turn number
            try:
                move = move[1]
            except IndexError:
                move = move[0]

            formated[i].append(move)
        formated[i].append(data[i][-1])


    #
    X_train = []
    Y_train = []
    board = Board()
    for i in range(len(formated)):
        board.resetGrid()
        board.currentPlayer = Board.WHITE
        for j in range(len(formated[i])-2):
            
            # Make VECTOR -> Move combinaison
            X_train.append(board.makeVector())
            Y_train.append(pgnToVector(formated[i][j]))
            if not True in Y_train[-1]:
                # cd5 don't is not catched by pgnToVector.
                print("Should have a True")
            move = board.convertPgn(formated[i][j])
            board.play(move)
            board.nextTurn()

    X_train = torch.FloatTensor(X_train)
    Y_train = torch.FloatTensor(Y_train)

    return (X_train, Y_train)

def constructModel(X_train, Y_train, epochs=100):
    model = Model()
    criterion = nn.CrossEntropyLoss()

    # Choose Adam optim, popular, lr=learning rate
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    losses = []
    for i in range(epochs):
        y_pred = model.forward(X_train) # Get predicted results

        # Measure the loss/error, gonna be high at first
        loss = criterion(y_pred, Y_train) # predicted values vs the y_train     
        
        # Keep Track of our losses
        losses.append(loss.detach().numpy())        
        
        # print every 10 epoch
        if i % 10 == 0:
          print(f'Epoch: {i} and loss: {loss}')     
        # Do some back propagation: take the error rate of forward propagation and feed it back
        # thru the network to fine tune the weights
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return model, losses
    
EPOCHS = 30
DATASET_SIZE = 100

b = Board()
X, Y = constructDataSet("data", max=DATASET_SIZE)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)

print("CONSTRUCTING MODEL")
model, losses = constructModel(X_train, Y_train, epochs=EPOCHS) 

# TEST OF OUR MODEL:
correct = 0
with torch.no_grad():
    for i, data in enumerate(X_test):
        y_val = model.forward(data)   

        # Correct or not
        normal = Y_test[i].tolist()
        if y_val.argmax().item() == normal.index(1.):
            correct +=1

print(f'We got {correct} correct on {len(X_test)} ! \t({correct/len(X_test)*100}% success rate.)')

# Display loss evolution
plt.plot(range(EPOCHS), losses)
plt.ylabel("loss/error")
plt.xlabel('Epoch')
plt.legend()
plt.show()