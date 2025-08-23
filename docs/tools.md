# Tools

This project includes several built-in tools:

- `web_search`: DuckDuckGo text search
- `web_fetch`: Fetch & parse page to markdown
- `python_exec`: Sandboxed Python snippet execution
- `vector_store`: Local ChromaDB for memory
- `github`: Search repos, list issues, read README; optionally create issues (requires `GITHUB_TOKEN`)
- `notion`: Fetch page JSON or query database (requires `NOTION_API_TOKEN`)

## Environment Variables

- `GITHUB_TOKEN`: optional, enables higher rate limits and issue creation
- `NOTION_API_TOKEN`: required for Notion API access


- `wikipedia`: search/summary (requires `wikipedia` package; installed by default)
- `arxiv`: academic paper search (requires `arxiv` package; installed by default)
