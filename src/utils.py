# utils.py
import os
import pickle
import pandas as pd
import numpy as np
_model = None


def get_model():
    """Lazy-load and return the SentenceTransformer model.

    This avoids importing / loading the model at module import time which
    makes running fast unit tests or CI faster. Tests can patch `get_model`.
    """
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            raise ImportError(
                "The package `sentence_transformers` is required to use embeddings."
            ) from e
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, "..", "Data", "raw", "dummy_papers.csv")
PROCESSED_PATH = os.path.join(BASE_DIR, "..", "Data", "processed")
EMBEDDINGS_FILE = os.path.join(PROCESSED_PATH, "embeddings.pkl")


def load_data():
    """Load raw data CSV into a DataFrame."""
    return pd.read_csv(RAW_DATA_PATH)


def embed_texts(texts, cache_file=EMBEDDINGS_FILE):
    """
    Convert a list of texts into embeddings.
    Uses caching to avoid recomputation.
    """
    # Check if cache exists
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    model = get_model()
    embeddings = model.encode(texts)

    # Save to cache
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, "wb") as f:
        pickle.dump(embeddings, f)

    return embeddings


def semantic_search(df, query, top_k=3):
    """
    Perform semantic search on title + abstract.
    Returns top_k papers most relevant to the query.
    """
    combined_texts = df['title'] + ". " + df['abstract']
    embeddings = embed_texts(combined_texts.tolist())  # cached

    model = get_model()
    query_embedding = model.encode([query])[0]  # query is small, no need to cache
    sims = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    top_indices = sims.argsort()[::-1][:top_k]
    return df.iloc[top_indices]


def summarize_papers(df):
    """
    Return a short summary of each paper.
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
