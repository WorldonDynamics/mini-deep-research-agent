# Contributing

Thanks for your interest in contributing to Deep Research Agent. This project is kept intentionally small and focused — follow these steps to contribute.

1. Fork the repository and create a feature branch.
2. Run tests locally with `pytest` and ensure new changes add or update tests.
3. Push your branch and open a pull request; CI will run tests automatically.

Developer notes:
- The core utilities are in `mini-deep-research-agent/src/utils.py`.
- Embeddings are cached at `Data/processed/embeddings.pkl`. If you change the embedding model, clear or version the cache.
- To keep CI/tests fast, the model is lazy-loaded via `get_model()` — patch `get_model` in unit tests when mocking the encoder.

PR guidance:
- Keep changes small and focused.
- Add tests for new behavior.
- Ensure code is formatted consistently.
