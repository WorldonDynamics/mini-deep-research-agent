# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

- Add Copilot/AI contributor instructions and `AGENT.md` onboarding.
- Add unit-test skeleton and CI workflow (`.github/workflows/ci.yml`) to run `pytest`.
- Lazy-load embedding model via `get_model()` to make tests/CI faster.
- Add Streamlit demo (`src/web_app.py`) and CLI demo runner (`mini-deep-research-agent/src/main.py`).
- Add demo screenshot (placeholder) and architecture diagram under `docs/`.
- Add `LICENSE` (MIT) and `CONTRIBUTING.md`.

## 0.1.0 - 2025-11-21

- Initial public-ready release: basic embedding + semantic search pipeline, docs, tests, CI.
