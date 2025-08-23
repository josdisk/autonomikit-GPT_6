from __future__ import annotations
from typing import Optional
from .tools.web_search import WebSearch
from .tools.web_fetch import WebFetch
from .tools.python_exec import PythonExec
from .tools.vector_store import VectorStore
from .tools.github import GitHubTool
from .tools.notion import NotionTool
from .tools.wikipedia import WikipediaTool
from .tools.arxiv import ArxivTool
from .agent.planner import Planner

def default_planner(model: Optional[str] = None) -> Planner:
    tools = [WebSearch(), WebFetch(), PythonExec(), VectorStore(), GitHubTool(), NotionTool(), WikipediaTool(), ArxivTool()]
    return Planner(tools=tools, model=model)

def run_task(task: str, max_steps: int = 5, model: Optional[str] = None) -> str:
    planner = default_planner(model=model)
    return planner.run(task, max_steps=max_steps)
