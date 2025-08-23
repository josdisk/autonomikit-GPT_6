# Contributing to AutonomiKit‑GPT

Thanks for your interest in contributing! This project aims to be a **clean, professional OSS** example
that solo builders can showcase.

## Development Setup

```bash
git clone https://github.com/<you>/AutonomiKit-GPT.git
cd AutonomiKit-GPT
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
cp .env.example .env
```

## Code Quality

- Format: `black .`
- Lint: `ruff .`
- Types: `mypy src`
- Tests: `pytest -q`

Consider installing **pre-commit**:

```bash
pre-commit install
```

## Issues & PRs

- Before filing a PR, open an issue describing the change or link an existing issue.
- Keep PRs small & focused. Include tests where feasible.
- For new tools, add docs in `docs/` and update the README if needed.

## Release

- We use semantic versioning (MAJOR.MINOR.PATCH).
- Tag releases and draft notes with highlights, breaking changes, and upgrade steps.

Thank you! 🙌
