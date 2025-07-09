import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from model import Model, VECTOR_SIZE, POSSIBLE_MOVE
from chessgame import Board
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from movement import Movement
import time
import json


# VARIABLE
DURATION = 3600*24*7   # full week training
DATASET_SIZE = 244000  # 50% of the dataSet
            
def moveToVector(move):
    """
    Return a list of all possible move,
    using chess notation [originSquare][destinationSquare]
    """
    out = [move.origin[1:] == "O-O", move.origin[1:] == "O-O-O"]
    moveString = move.origin + move.dest
    for originX in range(8):
        for originY in range(8):
            for destX in range(8):
                for destY in range(8):
                    out.append(f"{chr(ord('a') + originX)}{originY + 1}{chr(ord('a') + destX)}{destY + 1}" == moveString)

    return out


def VectorToMove(vector):
    """
    take a vector and return a move
    using chess notation [originSquare][destinationSquare]
    """
    for originX in range(8):
        for originY in range(8):
            for destX in range(8):
                for destY in range(8):
                    if(vector[originX*(8**3)+originY*(8**2)+destX*8+destY]):
                        return Movement(origin=f"{chr(ord('a') + originX)}{originY + 1}",dest=f"{chr(ord('a') + destX)}{destY + 1}")




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
                reader = file.read().split("\n")
                for i in range(len(reader)-1):
                    if index < max:
                        data.append(reader[i].split(" "))
                        index += 1
    

    X_train = []
    Y_train = []
    board = Board()
    for i in range(len(data)):
        board.resetGrid()
        board.currentPlayer = Board.WHITE
        for j in range(len(data[i])-2):
            
            # Make VECTOR -> Move combinaison
            move = board.convertPgn(data[i][j])
            X_train.append(board.makeVector())
            Y_train.append(moveToVector(move))
            if not True in Y_train[-1]:
                # cd5 don't is not catched by pgnToVector.
                print("Should have a True")
            board.play(move)
            board.nextTurn()

    X_train = torch.FloatTensor(X_train)
    Y_train = torch.FloatTensor(Y_train)

    return (X_train, Y_train)

def constructModel(X_train, Y_train, duration=60):
    """
    Time based training.
    """
    model = Model()
    criterion = nn.CrossEntropyLoss()

    # Choose Adam optim, popular, lr=learning rate
    optimizer = torch.optim.Adagrad(model.parameters(), lr=0.01)

    losses = []
    start = time.time()
    epochs = 0
    current = 0
    while current-start < duration:
        y_pred = model.forward(X_train) # Get predicted results

        # Measure the loss/error, gonna be high at first
        loss = criterion(y_pred, Y_train) # predicted values vs the y_train     
        
        # Keep Track of our losses
        losses.append(loss.detach().numpy())        
        
        # print every epoch
        if epochs % 10 == 0:
            print(f'Epoch: {epochs} and loss: {loss}')     
        # Do some back propagation: take the error rate of forward propagation and feed it back
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        current = time.time()
        epochs += 1

    return model, losses, epochs
    



# DATA EXTRACTION
# Data folder contain 488930 games
print("COMPUTING DATA")
start = time.time()
X, Y = constructDataSet("data", max=DATASET_SIZE)
end = time.time()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

# MODEL CONSTRUCTION
print("CONSTRUCTING MODEL")
model, losses, epochs = constructModel(X_train, Y_train, duration=DURATION) 
print(f"computed {epochs}, epochs")


# TEST OF THE MODEL:
correct = 0
with torch.no_grad():
    for i, data in enumerate(X_test):
        y_val = model.forward(data)   

        # Correct or not
        normal = Y_test[i].tolist()
        if y_val.argmax().item() == normal.index(1.):
            correct +=1


print(f'We got {correct} correct on {len(X_test)} ! \t({correct/len(X_test)*100}% success rate.)')

# SAVING THE MODEL
print("SAVING...")
torch.save(model.state_dict(), f'{DATASET_SIZE}Games{epochs}EpochsModel.pt')

# SAVING LOG DATA
with open(f"log.json", 'w') as f:
    json.dump({
        "model": f'{DATASET_SIZE}Games{epochs}EpochsModel.pt',
        "computingTime": DURATION,
        "datasetSize": DATASET_SIZE,
        "epochs": epochs,
        "successRate": correct/len(X_test),
        "losses": [i.tolist() for i in losses],
        "dataComputingTime": end-start
    }, f, indent=4)
