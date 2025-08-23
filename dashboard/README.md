# AutonomiKit Dashboard (Next.js)

A minimal UI to call the FastAPI agent.

## Run

```bash
cd dashboard
npm i
cp .env.local.example .env.local  # adjust API_BASE_URL if needed
npm run dev
# open http://localhost:3000
```

This app proxies `/api/run` to `${API_BASE_URL}/v1/agent/run`.
