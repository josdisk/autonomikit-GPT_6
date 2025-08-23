from __future__ import annotations
from typing import Dict, Any
import os, httpx, json
from .base import Tool, ToolResult

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def _headers():
    token = os.getenv("NOTION_API_TOKEN") or ""
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

class NotionTool(Tool):
    name = "notion"
    description = "Fetch Notion page JSON or query a database (requires NOTION_API_TOKEN)."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["page", "database_query"]},
            "id": {"type": "string", "description": "Page ID or Database ID."},
            "query": {"type": "object", "description": "Query JSON for database_query (filters/sorts)."},
        },
        "required": ["action", "id"],
    }

    def run(self, action: str, id: str, query: Dict[str, Any] | None = None, **_) -> ToolResult:
        if not os.getenv("NOTION_API_TOKEN"):
            return ToolResult(content="NOTION_API_TOKEN not set.", meta={})
        with httpx.Client(timeout=30.0, headers=_headers()) as client:
            if action == "page":
                r = client.get(f"{NOTION_API}/pages/{id}")
                r.raise_for_status()
                data = r.json()
                title = ""
                props = data.get("properties", {})
                for k, v in props.items():
                    if v.get("title"):
                        parts = v["title"]
                        if parts and len(parts) and "plain_text" in parts[0]:
                            title = parts[0]["plain_text"]
                            break
                return ToolResult(content=json.dumps({"title": title, "properties": list(props.keys())}, ensure_ascii=False), meta={"id": id})
            else:
                r = client.post(f"{NOTION_API}/databases/{id}/query", json=query or {})
                r.raise_for_status()
                data = r.json()
                results = [{"id": it.get("id")} for it in data.get("results", [])][:10]
                return ToolResult(content=json.dumps(results, ensure_ascii=False), meta={"count": len(results)})
