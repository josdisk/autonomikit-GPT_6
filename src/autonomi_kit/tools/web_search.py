from __future__ import annotations
from typing import Dict, Any, List
from dataclasses import dataclass
from loguru import logger
from duckduckgo_search import DDGS
from .base import Tool, ToolResult

class WebSearch(Tool):
    name = "web_search"
    description = "Search the web for recent information using DuckDuckGo."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query string."},
            "max_results": {"type": "integer", "description": "Max results (1-10).", "default": 5},
        },
        "required": ["query"],
    }

    def run(self, query: str, max_results: int = 5, **_) -> ToolResult:
        max_results = max(1, min(10, int(max_results)))
        results: List[Dict[str, Any]] = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({"title": r.get("title"), "href": r.get("href"), "body": r.get("body")})
        logger.debug(f"web_search: {len(results)} results for {query!r}")
        return ToolResult(content=str(results), meta={"count": len(results)})
