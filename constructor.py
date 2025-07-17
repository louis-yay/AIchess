import time
from datetime import timedelta
import pandas as pd
import gc
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from chessnet import chessNet
import torch.optim as optim
from tqdm import tqdm
from dataset import ChessDataset
from sklearn.model_selection import train_test_split

# Load data
rawData = pd.read_csv("chess_games.csv", usecols=['AN', 'WhiteElo'])
data = rawData[rawData['WhiteElo'] > 2000]  # keep only game with Elo > 2000
del rawData
gc.collect()    # Clean the ram from unused data

# Remove non usable games
data = data[['AN']]
data = data[-data['AN'].str.contains('{')]
data = data[data['AN'].str.len() > 20]
print(f"loaded {data.shape[0]}")
# 883k games

trainingData = ChessDataset(data, 1_000)


train_data, val_data = train_test_split(trainingData, test_size=0.1, random_state=42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"training data {len(val_data)}")

# Instantiate model
model = chessNet().to(device)

# Loss function
criterion = nn.CrossEntropyLoss()

# Optimizer
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Training data loader
dataTrainLoader = DataLoader(train_data, batch_size=32, drop_last=True)

print(f"final training data: {dataTrainLoader}")

# Training parameters
start = time.time()
current = start
TRAINING_TIME = 3600
num_epochs = 1

while (time.time() - start) < TRAINING_TIME:
    total_loss = 0
    progress = tqdm(dataTrainLoader, desc=f"Remaining time: {timedelta(seconds=round(TRAINING_TIME - (time.time() - start)))}, epoch: {num_epochs}")

    for x, y in progress:

        x = x.float().to(device)        # Board
        y = y.float().to(device)        # Move

        optimizer.zero_grad()
        output = model(x)               # Move

        # Combine target to a single dimension vector
        target_origin = y[:, 0].view(x.size(0), -1).argmax(dim=1)  
        target_dest   = y[:, 1].view(x.size(0), -1).argmax(dim=1)  

        # Flatten output for cross entropy function
        output_flat = output.view(x.size(0), 2, -1)  

        # calculate loss from critetion (loss function)
        loss_origin = criterion(output_flat[:, 0], target_origin)
        loss_dest   = criterion(output_flat[:, 1], target_dest)
        loss = loss_origin + loss_dest

        # retropropagation
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        progress.set_postfix(loss=total_loss / (progress.n + 1))

    print(f"Epoch {num_epochs} Average Loss: {total_loss / len(dataTrainLoader):.4f}")
    num_epochs += 1

# Save model after training
print("saving...")
torch.save(model.state_dict(), "chessNet.pth")




# TEST THE MODEL
def evaluate(model, dataloader, device, criterion):
    model.eval()  # Set model to evaluation mode
    total_loss = 0
    correct_origin = 0
    correct_dest = 0
    total_samples = 0

    with torch.no_grad():  # Disable gradient computation
        for x, y in dataloader:
            x = x.float().to(device)  # board
            y = y.float().to(device)  # move

            output = model(x)  # move
            B = x.size(0)

            # same as the training we transform (8;8) -> 64
            output_flat = output.view(B, 2, -1) 
            target_origin = y[:, 0].view(B, -1).argmax(dim=1)  
            target_dest   = y[:, 1].view(B, -1).argmax(dim=1) 

            # loss calculation
            loss_origin = criterion(output_flat[:, 0], target_origin)
            loss_dest   = criterion(output_flat[:, 1], target_dest)
            loss = loss_origin + loss_dest
            total_loss += loss.item()

            # Accuracy
            pred_origin = output_flat[:, 0].argmax(dim=1)  
            pred_dest   = output_flat[:, 1].argmax(dim=1)  

            # Test if the output is accurate
            correct_origin += (pred_origin == target_origin).sum().item()
            correct_dest   += (pred_dest == target_dest).sum().item()
            total_samples += B

    # Calculate average loss and sucess rate
    avg_loss = total_loss / len(dataloader)
    acc_origin = correct_origin / total_samples
    acc_dest = correct_dest / total_samples
    avg_acc = (acc_origin + acc_dest) / 2

    print(f"Validation Loss: {avg_loss:.4f}")
    print(f"Origin Accuracy: {acc_origin:.4f}, Dest Accuracy: {acc_dest:.4f}, Avg Accuracy: {avg_acc:.4f}")

    return avg_loss, avg_acc

val_loss, val_acc = evaluate(model, DataLoader(val_data, batch_size=32, drop_last=True)
, device, criterion)

print(f"ACCURACY: {val_acc*100}%")
