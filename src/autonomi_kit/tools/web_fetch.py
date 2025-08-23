from __future__ import annotations
import time
import re
from typing import Dict, Any
import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from .base import Tool, ToolResult

class WebFetch(Tool):
    name = "web_fetch"
    description = "Fetch a URL and return a cleaned markdown summary of the page contents."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Full URL to fetch."},
        },
        "required": ["url"],
    }

    def run(self, url: str, **_) -> ToolResult:
        # Simple robot-friendly delay
        time.sleep(1.0)
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            r = client.get(url, headers={"User-Agent": "AutonomiKit-GPT/1.0"})
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            # Drop script/style
            for s in soup(["script", "style", "noscript"]):
                s.decompose()
            text_md = md(str(soup))
            # Truncate to avoid overlong contexts
            text_md = re.sub(r"\n{3,}", "\n\n", text_md)
            if len(text_md) > 8000:
                text_md = text_md[:8000] + "\n\n[...truncated...]"
            return ToolResult(content=text_md, meta={"url": url, "length": len(text_md)})
