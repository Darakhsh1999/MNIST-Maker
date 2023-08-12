import torch
import numpy as np
import torch.nn as nn
import matplotlib.pyplot as plt
from pytorch_stuff import CNN, CustomMNIST, train
from torch.utils.data import DataLoader, random_split

# Data sets
image_shape = (1,64,64)
data_path = r"Test Dataset Folder/"
data = CustomMNIST(data_path, image_shape)

# Model
device = torch.device("cuda" if torch.cuda.is_available else "cpu")
model = CNN()
model = model.to(device)

# Hyperparameters
batch_size = 20
lr = 0.001
n_epochs = 50

# Train data
train_data, test_data = random_split(data, [0.9,0.1])
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

# Optimizer and loss function 
optimizer = torch.optim.Adam(model.parameters(), lr=lr)
loss_fn = nn.CrossEntropyLoss()

train(model, n_epochs, train_loader, loss_fn, optimizer, device)

# Test on images
model.eval()

with torch.no_grad():

    for test_idx in range(len(test_data)):

        img, target = test_data[test_idx]
        img = img[None].to(device) # (N,1,H,W)

        output = model(img) # (N,10)
        predicted_class = torch.argmax(output, dim=-1).item()

        plt.imshow(img.cpu().numpy().squeeze(), cmap="gray")
        plt.title(f"Prediction {predicted_class} | Target: {target}")
        plt.show()


