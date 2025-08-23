from __future__ import annotations
from typing import Dict, Any, List, Optional
import os, httpx, base64, json
from .base import Tool, ToolResult

GITHUB_API = "https://api.github.com"

def _gh_headers():
    token = os.getenv("GITHUB_TOKEN")
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

class GitHubTool(Tool):
    name = "github"
    description = "Query GitHub: search repos, list issues, get README, optionally create issue (requires token)."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["search_repos", "list_issues", "get_readme", "create_issue"]},
            "query": {"type": "string", "description": "Search query for repos (if action=search_repos)."},
            "owner": {"type": "string", "description": "Repo owner (for issues/readme)."},
            "repo": {"type": "string", "description": "Repo name (for issues/readme)."},
            "title": {"type": "string", "description": "Issue title (for create_issue)."},
            "body": {"type": "string", "description": "Issue body (for create_issue)."},
        },
        "required": ["action"],
    }

    def run(self, action: str, **kwargs) -> ToolResult:
        headers = _gh_headers()
        with httpx.Client(timeout=30.0, headers=headers, follow_redirects=True) as client:
            if action == "search_repos":
                q = kwargs.get("query") or "agentic LLM"
                r = client.get(f"{GITHUB_API}/search/repositories", params={"q": q, "sort": "stars", "order": "desc"})
                r.raise_for_status()
                items = r.json().get("items", [])[:5]
                trimmed = [{"full_name": it["full_name"], "stars": it["stargazers_count"], "html_url": it["html_url"]} for it in items]
                return ToolResult(content=json.dumps(trimmed, ensure_ascii=False), meta={"count": len(trimmed)})
            elif action == "list_issues":
                owner, repo = kwargs.get("owner"), kwargs.get("repo")
                if not owner or not repo:
                    return ToolResult(content="owner/repo required", meta={})
                r = client.get(f"{GITHUB_API}/repos/{owner}/{repo}/issues", params={"state": "open"})
                r.raise_for_status()
                items = r.json()[:10]
                trimmed = [{"number": it["number"], "title": it["title"], "url": it["html_url"]} for it in items if "pull_request" not in it]
                return ToolResult(content=json.dumps(trimmed, ensure_ascii=False), meta={"count": len(trimmed)})
            elif action == "get_readme":
                owner, repo = kwargs.get("owner"), kwargs.get("repo")
                if not owner or not repo:
                    return ToolResult(content="owner/repo required", meta={})
                r = client.get(f"{GITHUB_API}/repos/{owner}/{repo}/readme")
                r.raise_for_status()
                data = r.json()
                encoded = data.get("content", "")
                text = base64.b64decode(encoded).decode("utf-8", errors="ignore")
                return ToolResult(content=text[:8000], meta={"truncated": len(text) > 8000})
            elif action == "create_issue":
                owner, repo, title, body = kwargs.get("owner"), kwargs.get("repo"), kwargs.get("title"), kwargs.get("body")
                if not (owner and repo and title):
                    return ToolResult(content="owner/repo/title required", meta={})
                if "Authorization" not in headers:
                    return ToolResult(content="GITHUB_TOKEN required to create issues.", meta={})
                r = client.post(f"{GITHUB_API}/repos/{owner}/{repo}/issues", json={"title": title, "body": body or ""})
                r.raise_for_status()
                item = r.json()
                return ToolResult(content=f"Created issue #{item['number']}: {item['html_url']}", meta={"number": item["number"]})
            else:
                return ToolResult(content=f"Unknown action: {action}", meta={})
