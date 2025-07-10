import torch.nn as nn
import torch

class module(nn.Module):
    def __init__(self, hidden_size):
        super(module, self).__init__()

        # Convolutional layer
        self.conv1 = nn.Conv2d(hidden_size, hidden_size, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(hidden_size, hidden_size, 3, stride=1, padding=1)
        
        # Batch layer
        self.bn1 = nn.BatchNorm2d(hidden_size)
        self.bn2 = nn.BatchNorm2d(hidden_size)
        self.activ1 = nn.SELU()
        self.activ2 = nn.SELU()

    def forward(self, x):

        # Connection
        input = torch.clone(x)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.activ1(x)
        x = self.conv2(x)
        x = self.bn2(x)

        # Addition of the input and output (improve learning)
        x = x + input
        x = self.activ2(x)
        return x