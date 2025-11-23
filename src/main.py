<<<<<<< HEAD
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
# Paths to dataset CSVs
# -------------------------------
train_csv = r"C:\Users\bworl\.cache\kagglehub\datasets\datamunge\sign-language-mnist\versions\1\sign_mnist_train.csv"
test_csv  = r"C:\Users\bworl\.cache\kagglehub\datasets\datamunge\sign-language-mnist\versions\1\sign_mnist_test.csv"

# Check if files exist
if not os.path.isfile(train_csv):
    raise FileNotFoundError(f"Train CSV not found at {train_csv}")
if not os.path.isfile(test_csv):
    raise FileNotFoundError(f"Test CSV not found at {test_csv}")

# -------------------------------
# Load datasets
# -------------------------------
train_df = pd.read_csv(train_csv)
test_df = pd.read_csv(test_csv)

# Split off validation set from training
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
=======
# main.py
import os
import json
from utils import load_data, semantic_search, summarize_papers

# List of queries for multi-query mode
QUERIES = [
    "machine learning",
    "autonomous agents",
    "neural architecture search",
    "reinforcement learning"
]

def main():
    # Load dataset
    df = load_data()
    print("=== 🚀 Deep Research Agent — Multi‑Query Mode ===\n")
    
    all_results = {}

    for query in QUERIES:
        print("="*80)
        print(f" 🔍 Processing Query: {query}")
        print("="*80 + "\n")
        
        # Semantic search
        top_results = semantic_search(df, query)
        
        # Display top results
        for idx, row in top_results.iterrows():
            print("-"*80)
            print(f"Title: {row['title']}")
            print(f"Abstract Preview: {row['abstract'][:75]}...")
            print(f"Authors: {row['authors']}\n")
        print("-"*80 + "\n")
        
        # Summarize results
        summaries = summarize_papers(top_results)
        all_results[query] = summaries
    
    # Ensure output directory exists
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save all query results to JSON
    output_file = os.path.join(output_dir, "multi_query_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)

    print(f"\n✅ All query results saved to: {output_file}\n")
    print("=== Finished 🚀 ===")

if __name__ == "__main__":
    main()
    
>>>>>>> 270e952a2de0a6d81c3475cfc1d86291627884d4
