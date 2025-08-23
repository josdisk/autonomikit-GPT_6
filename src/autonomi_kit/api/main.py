from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ..orchestrator import run_task
from ..config import settings

app = FastAPI(title="AutonomiKit‑GPT", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    task: str
    max_steps: int = 5
    model: str | None = None

class RunResponse(BaseModel):
    result: str

@app.get("/health")
def health():
    return {"status": "ok", "provider": settings.provider, "model": settings.llm_model}

@app.post("/v1/agent/run", response_model=RunResponse)
def run(req: RunRequest):
    result = run_task(req.task, max_steps=req.max_steps, model=req.model)
    return RunResponse(result=result)
