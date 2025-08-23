![AutonomiKit-GPT Banner](assets/banner.svg)

# AutonomiKit‑GPT 6 — An Open, Agentic LLM Stack built from scratch to speed Chat GPT 5 autonomously (API + CLI + Multi‑Tool + Memory)

[![CI](https://img.shields.io/github/actions/workflow/status/josdisk/AutonomiKit-GPT/ci.yml?branch=main)](./.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#)
[![Docs](https://img.shields.io/badge/Docs-mkdocs%20material-informational.svg)](./docs)

**AutonomiKit‑GPT** is an experimental batteries‑included, production‑grade **agentic LLM starter** that shows significant lightweight Autonomouskit-GPT_6 built from ground up to speedup Chat GPT-5 light tasks:

- *Provider‑agnostic* LLM client (OpenAI ≥ v1, Azure OpenAI, OpenRouter via envs)
-  Tool use: **web search**, **web fetch/scrape**, **Python exec** (sandboxed), **Vector memory**
-  ReAct‑style loop with multi‑agent **Researcher → Critic → Writer** orchestration
-  Tests, **benchmark script** + PNG chart, and an **example** research agent
-  **FastAPI** service exposing `/v1/agent/run` + OpenAPI schema
-  **Typer CLI** (`autonomi ...`) for local runs
- **Dockerfile**, **CI** (ruff/black/mypy/pytest), **pre‑commit**, **MkDocs** docs, and **MIT** license

---

## Quickstart

```bash
# Python 3.10+ recommended
python -m venv .venv && source .venv/bin/activate

pip install -U pip
pip install -e .

# Copy env template and set your keys
cp .env.example .env
# export OPENAI_API_KEY=sk-...  (or configure Azure/OpenRouter variants in .env)

# Try the CLI
autonomi run "Research the benefits of EV heat pumps and produce a 3-bullet summary with links."

# Or start the API
autonomi api
# Then, in another shell:
curl -X POST http://localhost:8000/v1/agent/run -H "Content-Type: application/json"   -d '{"task":"Find 3 recent papers on federated learning and summarize them."}'
```

## Features

- **LLM Provider Abstraction**: Works with OpenAI, Azure OpenAI, or OpenRouter via envs.
- **Tools included**:
  - `web_search`: DuckDuckGo query (no key required)
  - `web_fetch`: fetch & parse content (bs4) with robots‑aware delays
  - `python_exec`: restricted Python runner (time/memory/args limited)
  - `vector_store`: lightweight persistent memory using ChromaDB (local)
- **Agent Orchestrator**: Researcher ⇄ Critic ⇄ Writer using ReAct‑like loop and JSON tool calls.
- **API + CLI**: One codebase: run as a service (FastAPI) or from terminal (Typer).
- **Robust OSS Setup**: CI, tests, code quality, docs, contribution guide, Code of Conduct.

## Architecture (Mermaid)

```mermaid
flowchart LR
    subgraph Client
        A[CLI (Typer)] --- B[REST (FastAPI)]
    end

    subgraph Core
        C[Agent Orchestrator] --> D[LLM Client]
        C --> E[Tools: search/fetch/python/memory]
        D <--> E
    end

    subgraph Storage
        F[(Vector DB
Chroma)]
        G[(Cache/SQLite)]
    end

    E --> F
    C --> G
```

## Repo Structure

```
AutonomiKit-GPT/
├─ src/autonomi_kit/
│  ├─ agent/                # Planner, Orchestrator
│  ├─ api/                  # FastAPI app
│  ├─ tools/                # Tools (search, fetch, python, memory)
│  ├─ __init__.py
│  ├─ cli.py                # Typer CLI
│  ├─ config.py             # Settings via envs
│  ├─ llm.py                # Provider-agnostic client
│  └─ orchestrator.py       # Multi-agent round-robin
├─ examples/
│  └─ research_agent.py
├─ tests/
│  └─ test_smoke.py
├─ docs/
│  ├─ index.md
│  ├─ quickstart.md
│  └─ architecture.md
├─ .github/workflows/ci.yml
├─ .env.example
├─ pyproject.toml
├─ Dockerfile
├─ mkdocs.yml
├─ CONTRIBUTING.md
├─ CODE_OF_CONDUCT.md
├─ SECURITY.md
└─ README.md
```

## Benchmarks

Run a tiny local benchmark (latency + success heuristic) and get a chart:

```bash
python -m autonomi_kit.eval.bench --tasks small --plot out/bench.png
```

The plot and CSV will be written to `out/`.

## Community & Contributions

- See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, issues, and PR guidelines.
- Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Security reports: see [SECURITY.md](SECURITY.md).

## Sponsor

- Add your GitHub Sponsors handle in `.github/FUNDING.yml`.
- Add a logo/banner in `assets/` and link from this README.

---

Made with ❤️ for the open-source community. Happy hacking!


## Dashboard (Next.js)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/josdisk/AutonomiKit-GPT&root-directory=dashboard&project-name=autonomikit-dashboard&env=API_BASE_URL&envDescription=Base%20URL%20of%20your%20FastAPI)



A minimal UI lives in [`dashboard/`](dashboard).

```bash
cd dashboard
npm i
cp .env.local.example .env.local
npm run dev
# open http://localhost:3000
```

## Docker Compose (API + Dashboard)

```bash
docker compose up --build
# API -> http://localhost:8000
# Web -> http://localhost:3000
```


## Deploy

- **Dashboard (Vercel)**: import `dashboard/`, set `API_BASE_URL` env to your FastAPI URL.
- **Docker (prod)**: `docker compose -f compose.prod.yml up --build` (gunicorn/uvicorn workers).
- **Docs (Pages)**: GitHub Actions deploys MkDocs to Pages on push to `main`.

## Extra Tools

- `github` tool (public reads + optional issue creation with `GITHUB_TOKEN`)
- `notion` tool (requires `NOTION_API_TOKEN`)


## Releases / Containers

This repo publishes Docker images to **GHCR** on tags (`v*.*.*`). After pushing a tag:
- API: `ghcr.io/josdisk/autonomikit-api:latest`
- Web: `ghcr.io/josdisk/autonomikit-web:latest`

Example run:
```bash
docker run -p 8000:8000 --env-file .env ghcr.io/josdisk/autonomikit-api:latest
docker run -p 3000:3000 -e API_BASE_URL=http://localhost:8000 ghcr.io/josdisk/autonomikit-web:latest
```

Create a release:
```bash
git tag -a v0.1.0 -m "first release"
git push origin v0.1.0
```

## Seed good-first-issues

After you push to GitHub, run the **Seed Issues** workflow (Actions tab → Seed Issues → Run workflow).
This will create curated `good first issue` tasks from `.github/seed_issues.json`.


## Publishing

- **Python package:** use the **Publish to (Test)PyPI** workflow (Actions).  
- **Draft release:** run **Draft GitHub Release** (uses `.github/RELEASE_NOTES.md`).  
See **docs/Publishing** for details.
