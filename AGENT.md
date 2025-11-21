
# AGENT — Contributor + AI-agent Onboarding

This document expands the quick onboarding notes and provides concrete steps, examples, and conventions for contributors and AI-assisted workflows.

Why this repo exists
- Small, focused toolkit to load research paper datasets, compute sentence-transformer embeddings, run semantic search, and produce short summaries. It is intentionally minimal so contributors and AI agents can iterate quickly.

Quick start

- Install dependencies (PowerShell):

```
pip install -r requirements.txt
```

- Run the demo runner (from repo root):

```
python mini-deep-research-agent/src/main.py
```

- Run the Streamlit web UI (optional):

```
streamlit run src/web_app.py
```

Run tests

- Run tests locally from the repository root:

```
pytest -q
```

Core files & responsibilities
- `mini-deep-research-agent/src/utils.py` — core utilities (data loading, embed_texts, semantic_search, summarize_papers). Keep cache-first and path conventions.
- `mini-deep-research-agent/src/main.py` — demo runner that executes queries and writes `output/multi_query_results.json`.
- `src/web_app.py` — small Streamlit front-end that calls `semantic_search` and `summarize_papers`.

Key conventions and guidelines
- Paths: code uses relative paths (e.g., `../Data/raw/dummy_papers.csv`) — keep changes consistent so scripts run from repo root.
- Caching: `embed_texts` defaults to `Data/processed/embeddings.pkl`. If you change the embedding model/format, clear or version the cache.
- Model loading: use `get_model()` (lazy-load) to avoid heavy imports at module import time. Tests should patch `get_model`.
- Data schema: functions assume `title`, `abstract`, `authors` exist. If schema changes, update `semantic_search` and `summarize_papers` accordingly and add tests.

Testing guidance
- Unit tests should mock `get_model()` in `utils.py` and/or `embed_texts()` to avoid downloading models in CI.
- Keep tests small and deterministic. Use `tests/test_utils.py` as the canonical example.

Code style & quality
- Keep functions small and focused.
- Add unit tests for new behavior.
- Commit messages: use short prefix (`feat:`, `fix:`, `chore:`, `test:`) then a short summary.

Pull requests
- Create a branch from `main`. Push and open a PR. CI runs automatically (GitHub Actions) and will run `pytest`.
- In the PR description, include:
  - What changed (concise)
  - Why it changed
  - How to test locally (commands)

Security & privacy
- Do not commit credentials, API keys, or large binary caches. `.gitignore` excludes `.venv/`, `Data/processed/`, and `output/`.

AI-agent usage notes
- The repo already contains `.github/copilot-instructions.md` with actionable guidance for an AI coding agent. When asking an AI to modify code, prefer small, focused tasks. Example prompts:
  - "Add a unit test for `semantic_search` that mocks `get_model()` and checks top-k behavior." 
  - "Add a lazy-loading wrapper for the embedding model and update tests to patch it."

If you want me to expand any section (detailed testing matrix, CI badges, PR templates), say which section and I will add it.
