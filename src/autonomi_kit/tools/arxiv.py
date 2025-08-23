
from __future__ import annotations
from typing import Dict, Any, List
from .base import Tool, ToolResult

# Uses 'arxiv' package
try:
    import arxiv
except Exception:
    arxiv = None  # type: ignore

class ArxivTool(Tool):
    name = "arxiv"
    description = "Search arXiv for papers by query and return top N titles with links."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query, e.g., 'RAG retrieval augmentation'"},
            "max_results": {"type": "integer", "description": "Max results", "default": 3},
            "sort_by": {"type": "string", "enum": ["relevance","lastUpdatedDate","submittedDate"], "default": "submittedDate"}
        },
        "required": ["query"]
    }

    def run(self, query: str, max_results: int = 3, sort_by: str = "submittedDate", **_) -> ToolResult:
        if arxiv is None:
            return ToolResult(content="Dependency 'arxiv' not installed.", meta={})
        search = arxiv.Search(
            query=query,
            max_results=max(1, min(10, int(max_results))),
            sort_by=getattr(arxiv.SortCriterion, sort_by, arxiv.SortCriterion.SubmittedDate)
        )
        items: List[dict] = []
        for r in search.results():
            items.append({"title": r.title, "pdf": r.pdf_url, "entry_id": r.entry_id})
        return ToolResult(content=str(items), meta={"count": len(items)})
