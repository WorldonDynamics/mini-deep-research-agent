# Deep Research Agent

A modular Python project for loading research paper datasets, generating embeddings, performing semantic search, and summarizing top results.

![CI](https://github.com/WorldonDynamics/mini-deep-research-agent/actions/workflows/ci.yml/badge.svg)

Quick start

- Install dependencies (PowerShell):

```
pip install -r requirements.txt
```

- Run demo (from repository root):

```
python mini-deep-research-agent/src/main.py
```

Run tests (CI uses GitHub Actions):

```
pytest -q
```

Notes

- Embeddings are cached at `Data/processed/embeddings.pkl`. Remove that file to force re-embedding.
- See `.github/copilot-instructions.md` and `AGENT.md` for contributor and AI agent guidance.

