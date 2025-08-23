from __future__ import annotations
import typer, uvicorn
from rich.console import Console
from .orchestrator import run_task
from .config import settings

app = typer.Typer(help="AutonomiKit‑GPT CLI")
console = Console()

@app.command()
def run(task: str, steps: int = 5, model: str = settings.llm_model):
    """Run the agent once for a TASK."""
    console.rule("[bold]AutonomiKit‑GPT[/]")
    result = run_task(task, max_steps=steps, model=model)
    console.print(result)

@app.command()
def api(host: str = settings.host, port: int = settings.port):
    """Start the FastAPI server."""
    uvicorn.run("autonomi_kit.api.main:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    app()
