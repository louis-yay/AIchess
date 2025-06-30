import torch
import torch.nn as nn
import torch.nn.functional as F

VECTOR_SIZE = 768 + 1   # Current player color
POSSIBLE_MOVE = 386

class Model(nn.Module):
    """
    Input layer of size of board vector: 12x8x8 = 768
    """
    def __init__(self, in_features=VECTOR_SIZE, h1=2*VECTOR_SIZE, h2=2*VECTOR_SIZE, out_features=POSSIBLE_MOVE):
        super().__init__() # instantiate our nn.Module
        self.fc1 = nn.Linear(in_features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.out = nn.Linear(h2, out_features)   

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.out(x)   
        return x