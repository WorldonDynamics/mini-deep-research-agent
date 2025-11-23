# utils.py
import os
import pickle
import pandas as pd
import os
import pickle
import pandas as pd
import numpy as np

# Lazy-loaded global model
_model = None


def get_model():
    """Lazy-load and return the SentenceTransformer model.

    Loading the model at import time makes test execution and small scripts
    slow. Use this lazy loader so tests can patch `get_model` and CI can
    run quickly without importing heavy dependencies until needed.
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


# Paths (use relative defaults, callers may override)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RAW_CSV = os.path.join(BASE_DIR, "..", "Data", "raw", "dummy_papers.csv")
DEFAULT_PROCESSED_DIR = os.path.join(BASE_DIR, "..", "Data", "processed")
DEFAULT_EMBEDDINGS_FILE = os.path.join(DEFAULT_PROCESSED_DIR, "embeddings.pkl")


def load_data(csv_path=DEFAULT_RAW_CSV):
    """Load raw data CSV into a pandas DataFrame.

    Default path is `../Data/raw/dummy_papers.csv` relative to this file.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    return pd.read_csv(csv_path)


def embed_texts(texts, cache_file=DEFAULT_EMBEDDINGS_FILE):
    """Convert list of texts into embeddings using a cache-first strategy.

    If `cache_file` exists it is loaded and returned. Otherwise the model
    encodes the texts, the embeddings are cached to `cache_file`, and then
    returned.
    """
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    model = get_model()
    embeddings = model.encode(texts)

    # Ensure directory exists for cache
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    with open(cache_file, "wb") as f:
        pickle.dump(embeddings, f)

    return embeddings


def semantic_search(df, query, top_k=3):
    """Perform semantic search over `title + ". " + abstract`.

    Returns the top_k rows from `df` most similar to `query` by cosine
    similarity on sentence-transformer embeddings.
    """
    combined_texts = df['title'] + ". " + df['abstract']

    # Embed texts (cached) and the query (small, no cache)
    embeddings = embed_texts(combined_texts.tolist())
    model = get_model()
    query_embedding = model.encode([query])[0]

    # Cosine similarity
    sims = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    top_indices = sims.argsort()[::-1][:top_k]
    return df.iloc[top_indices]


def summarize_papers(df):
    """Return a short summary string for each paper in `df`.

    The summary includes title, a short abstract preview, and authors.
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
