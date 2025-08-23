# Deploy

## Vercel (Dashboard)

1. Push the repo to GitHub.
2. In Vercel, **Import Project** → select the `dashboard/` folder.
3. Set env `API_BASE_URL` to your FastAPI URL (e.g., https://api.example.com).
4. Deploy.

A basic `vercel.json` is provided in `dashboard/`.

## Docker (Production)

```bash
# Build & run production-grade API (gunicorn/uvicorn) + dashboard
docker compose -f compose.prod.yml up --build
```

## GitHub Pages (Docs)

Pushing to `main` triggers the **Docs** workflow and publishes MkDocs to Pages.
