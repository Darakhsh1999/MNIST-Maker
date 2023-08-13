import os
import cv2
import torch
import random
import numpy as np
import torch.nn as nn
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader

class CNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(1, 4, kernel_size=(3,3), padding="same")
        self.conv2 = nn.Conv2d(4, 8, kernel_size=(3,3), padding="same")
        self.conv3 = nn.Conv2d(8, 16, kernel_size=(3,3), padding="same")
        self.conv4 = nn.Conv2d(16, 32, kernel_size=(3,3), padding="same")
        self.linear1 = nn.Linear(32*16*16, 100)
        self.linear2 = nn.Linear(100, 10)
        self.soft_max = nn.Softmax(dim=-1)
        self.maxpool = nn.MaxPool2d(kernel_size=(2,2))
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout()

    def forward(self, x):
        
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.maxpool(x)
        x = self.relu(self.conv3(x))
        x = self.relu(self.conv4(x))
        x = self.maxpool(x)
        x = torch.flatten(x, start_dim= 1, end_dim= -1)
        x = self.linear1(x)
        x = self.linear2(x)
        if not self.training: # Logits when train (for BCE), probability when eval
            x = self.soft_max(x)
        return x
    
class CustomMNIST(Dataset):

    def __init__(self, data_path, image_shape):

        # Read in images
        self.data_path = data_path
        self.image_path = os.path.join(self.data_path,"Images")
        self.image_names = os.listdir(self.image_path)

        csv_path = [x for x in os.listdir(self.data_path) if x.endswith(".csv")][0]
        csv_labels = np.genfromtxt(os.path.join(self.data_path, csv_path), delimiter=',')
        self.n_images = len(self.image_names)


        # Allocate memory
        self.images = torch.zeros((self.n_images,*image_shape), dtype=torch.float32)
        self.labels = torch.zeros(self.n_images, dtype=torch.uint8)

        # Read in images
        for i, im_name in enumerate(self.image_names):

            # Parse image idx
            underscore_idx = im_name.index("_")
            dot_idx = im_name.index(".")
            label_idx = int(im_name[1+underscore_idx:dot_idx])-1

            # Read in image and cast to float32
            im = cv2.imread(os.path.join(self.image_path,im_name), 0).astype(np.float32)
            im = np.expand_dims(im, axis=0) / 255.0 # (1,H,W)

            self.images[i] = torch.tensor(im)
            self.labels[i] = csv_labels[label_idx]
    
    def show_example_image(self,n_examples=3):

        im_indices = random.sample(range(self.n_images), k=n_examples)
    
        for im_idx in im_indices:

            im = self.images[im_idx].numpy().squeeze()
            label = self.labels[im_idx]

            plt.imshow(im, cmap="gray")
            plt.title(f"Digit: {label}")
            plt.show()



    def __len__(self):
        return self.n_images
    
    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]
    

def train(model, n_epochs, train_loader, loss_fn, optimizer, device):
    """ Trains model """
    model.train()
    for epoch_idx in range(n_epochs):

        # Loop through training data
        epoch_loss = 0.0
        for img, labels in train_loader:
            
            # Load in batch and cast image to float32
            img = img.to(device) # (N,1,H,W)
            labels = labels.to(device)

            optimizer.zero_grad()

            output = model(img) # (N,10)
            loss = loss_fn(output, labels)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
        epoch_loss /= len(train_loader.dataset)
        print(f"Epoch {1+epoch_idx} loss = {epoch_loss:.4f}")



if __name__ == "__main__":

    image_shape = (1,64,64)
    data_path = r"Test Dataset Folder/"
    
    data = CustomMNIST(data_path, image_shape)
    data.show_example_image(15)