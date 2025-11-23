import os
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split

# -------------------------------
# Device setup
# -------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# -------------------------------
# Dataset paths
# -------------------------------
train_csv = r"C:\Users\bworl\.cache\kagglehub\datasets\datamunge\sign-language-mnist\versions\1\sign_mnist_train.csv"
test_csv  = r"C:\Users\bworl\.cache\kagglehub\datasets\datamunge\sign-language-mnist\versions\1\sign_mnist_test.csv"

# Check existence
if not os.path.isfile(train_csv):
    raise FileNotFoundError(f"Train CSV not found at {train_csv}")
if not os.path.isfile(test_csv):
    raise FileNotFoundError(f"Test CSV not found at {test_csv}")

# -------------------------------
# Load datasets
# -------------------------------
train_df = pd.read_csv(train_csv)
test_df  = pd.read_csv(test_csv)

# Split validation set
train_df, valid_df = train_test_split(train_df, test_size=0.1, random_state=42)

print(f"Training samples: {len(train_df)}, Validation samples: {len(valid_df)}, Test samples: {len(test_df)}")

# -------------------------------
# Constants
# -------------------------------
IMG_HEIGHT = 28
IMG_WIDTH  = 28
IMG_CHS    = 1
N_CLASSES  = 24
BATCH_SIZE = 32

# -------------------------------
# Dataset class
# -------------------------------
class MyDataset(Dataset):
    def __init__(self, df):
        x = df.drop(columns=['label']).values / 255.0
        x = x.reshape(-1, IMG_CHS, IMG_WIDTH, IMG_HEIGHT)
        y = df['label'].values

        self.xs = torch.tensor(x, dtype=torch.float32).to(device)
        self.ys = torch.tensor(y, dtype=torch.long).to(device)

    def __getitem__(self, idx):
        return self.xs[idx], self.ys[idx]

    def __len__(self):
        return len(self.xs)

# -------------------------------
# DataLoaders
# -------------------------------
train_dataset = MyDataset(train_df)
train_loader  = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

valid_dataset = MyDataset(valid_df)
valid_loader  = DataLoader(valid_dataset, batch_size=BATCH_SIZE)

test_dataset = MyDataset(test_df)
test_loader  = DataLoader(test_dataset, batch_size=BATCH_SIZE)

print(f"Train loader batches: {len(train_loader)}, Validation loader batches: {len(valid_loader)}, Test loader batches: {len(test_loader)}")
