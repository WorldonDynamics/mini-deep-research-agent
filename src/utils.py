# utils.py
import os
import pickle
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# -------------------------
# Model Initialization
# -------------------------
# Lightweight, fast model for semantic embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')


# -------------------------
# Data Loading
# -------------------------
def load_data(csv_path="../Data/raw/dummy_papers.csv"):
    """
    Load raw data CSV into a pandas DataFrame.
    Default path is ../Data/raw/dummy_papers.csv
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    return pd.read_csv(csv_path)


# -------------------------
# Embedding Texts with Caching
# -------------------------
def embed_texts(texts, cache_file="../Data/processed/embeddings.pkl"):
    """
    Convert list of texts into embeddings.
    Uses caching to avoid recomputation.
    """
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)
    
    embeddings = model.encode(texts)
    
    # Ensure directory exists for cache
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    
    with open(cache_file, "wb") as f:
        pickle.dump(embeddings, f)
    
    return embeddings


# -------------------------
# Semantic Search
# -------------------------
def semantic_search(df, query, top_k=3):
    """
    Perform semantic search on title + abstract.
    Returns top_k papers most relevant to the query.
    """
    combined_texts = df['title'] + ". " + df['abstract']
    
    # Embed texts (cached)
    embeddings = embed_texts(combined_texts.tolist())
    
    # Embed query (small, no cache)
    query_embedding = model.encode([query])[0]
    
    # Compute cosine similarity
    sims = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    
    # Return top_k results
    top_indices = sims.argsort()[::-1][:top_k]
    return df.iloc[top_indices]


# -------------------------
# Summarize Papers
# -------------------------
def summarize_papers(df):
    """
    Return a short summary of each paper in the DataFrame.
    """
    summaries = []
    for _, row in df.iterrows():
        summary = (
            f"Title: {row['title']}\n"
            f"Abstract Preview: {row['abstract'][:75]}...\n"
            f"Authors: {row['authors']}\n"
        )
        summaries.append(summary)
    return summaries
