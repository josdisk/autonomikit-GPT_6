
from __future__ import annotations
from typing import Dict, Any, List
from .base import Tool, ToolResult

# Uses 'wikipedia' package (MediaWiki API)
try:
    import wikipedia
except Exception:
    wikipedia = None  # type: ignore

class WikipediaTool(Tool):
    name = "wikipedia"
    description = "Search Wikipedia and fetch a page summary."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["search", "summary"]},
            "query": {"type": "string", "description": "Query or page title."},
            "lang": {"type": "string", "description": "Language code (default 'en')", "default": "en"},
            "results": {"type": "integer", "description": "Max search results", "default": 5}
        },
        "required": ["action", "query"]
    }

    def run(self, action: str, query: str, lang: str = "en", results: int = 5, **_) -> ToolResult:
        if wikipedia is None:
            return ToolResult(content="Dependency 'wikipedia' not installed.", meta={})
        wikipedia.set_lang(lang)
        if action == "search":
            hits = wikipedia.search(query, results=max(1, min(10, int(results))))
            return ToolResult(content=str(hits), meta={"count": len(hits)})
        else:
            try:
                summary = wikipedia.summary(query, sentences=5, auto_suggest=True, redirect=True)
                return ToolResult(content=summary, meta={"title": query})
            except Exception as e:
                return ToolResult(content=f"Error: {e}", meta={})
