import os
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from model import Model, VECTOR_SIZE, POSSIBLE_MOVE
from chessgame import Board
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from movement import Movement
import time

                
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
            move = board.convertPgn(formated[i][j])
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

def constructModel(X_train, Y_train, epochs=100):
    model = Model()
    criterion = nn.CrossEntropyLoss()

    # Choose Adam optim, popular, lr=learning rate
    optimizer = torch.optim.Adagrad(model.parameters(), lr=0.01)

    losses = []
    for i in range(epochs):
        y_pred = model.forward(X_train) # Get predicted results

        # Measure the loss/error, gonna be high at first
        loss = criterion(y_pred, Y_train) # predicted values vs the y_train     
        
        # Keep Track of our losses
        losses.append(loss.detach().numpy())        
        
        # print every epoch
        if i % 1 == 0:
          print(f'Epoch: {i} and loss: {loss}')     
        # Do some back propagation: take the error rate of forward propagation and feed it back
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return model, losses
    
EPOCHS = 50
DATASET_SIZE = 200

# BASE
print("COMPUTING DATA")
start = time.time()
X, Y = constructDataSet("data", max=DATASET_SIZE)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

print("CONSTRUCTING MODEL")
model, losses = constructModel(X_train, Y_train, epochs=EPOCHS) 
end = time.time()
print(f"Formation time: {end-start}")


# TEST OF OUR MODEL:
correct = 0
with torch.no_grad():
    for i, data in enumerate(X_test):
        y_val = model.forward(data)   

        # Correct or not
        normal = Y_test[i].tolist()
        if y_val.argmax().item() == normal.index(1.):
            correct +=1

# EPOCHS: 140, DATASET 800; sucess rate: 16% (training time: 1h23)
# 4 time sized layer, 200/50 success rate: 8.8%
# 2 time sized layer, 200/50 success rate: 9.9% (training time: 4m)
# 2 then 4 time sized layer, 200/50 success rate: 7.5%
# 4 then 2 time sized layer, 200/50 sucess rate 9.9%: 
# 3 time sized layer, 200/50 sucess rate: 9.0%
# 4 then 3 time sized layer, 200/50 success rate: 7.5%

# NOW WE KEEP 2 time sized layer, 200/50 and change learning rate:
# LR = 0.05 => 6.2%
# LR = 0.01 => 9.9%
# LR = 0.02 => 3.9%

# OTHER 
# BASIC 1300/10 => 1%
# 200/50 relu only at the end => 10.6%
# 400/90 relu only at the end => 15.0%
# 600/110 relu only at the end => 16.3% (training time: 17m)
# 800/140 relu only at the end => % (taining time: )

# OPTIMISER 200/50 & relu only at the end & LR = 0.01:
# ADAM => %
# SGD => 0.04%
# SGD (relu on every step) => 0.19%
# RMSprop => 1.5%
# RMSprop (relu on every step) =>  6.8%
# Adagrad => 5.4%
# Adagrad (relu on evert step) =>  %


print(f'We got {correct} correct on {len(X_test)} ! \t({correct/len(X_test)*100}% success rate.)')

print("SAVING...")
torch.save(model.state_dict(), f'{DATASET_SIZE}Games{EPOCHS}EpochsModel.pt')

