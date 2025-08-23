# Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
cp .env.example .env
# set OPENAI_API_KEY or alternate provider envs
autonomi run "Find 3 recent Rust web frameworks and give pros/cons."
```

To serve the API:

```bash
autonomi api
# -> FastAPI on http://localhost:8000
```

To build docs locally:

```bash
mkdocs serve
```
