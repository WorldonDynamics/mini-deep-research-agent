# AGENT — Contributor onboarding

This repository includes short machine-readable instructions for AI contributors in `.github/copilot-instructions.md` (root and `mini-deep-research-agent/.github`). Use this document for quick onboarding steps.

Quick start

- Install deps (PowerShell):

```
pip install -r requirements.txt
```

- Run demo (from repo root):

```
python mini-deep-research-agent/src/main.py
```

Testing

- Run tests from the repository root:

```
pytest -q
```

Notes for contributors

- The core logic is in `mini-deep-research-agent/src/utils.py`. Key functions:
  - `load_data(file_path)` — loads CSV/JSON/XLS files.
  - `embed_texts(texts, cache_file)` — uses a cache file at `Data/processed/embeddings.pkl` by default.
  - `semantic_search(df, query, top_k)` — composes `title` + `abstract` and finds top-k by cosine similarity.
  - `summarize_papers(df)` — returns short text summaries; assumes `title`, `abstract`, `authors` exist.

- Because `SentenceTransformer` is instantiated at import time, tests should mock `utils.model` or `embed_texts`.

If you want a draft PR created for your change, push a branch and use the GitHub UI or `gh` CLI. See `.github/copilot-instructions.md` for more details.
