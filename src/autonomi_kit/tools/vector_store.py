from __future__ import annotations
from typing import Dict, Any, List
import chromadb
from chromadb.config import Settings as ChromaSettings
from .base import Tool, ToolResult
from ..config import settings

class VectorStore(Tool):
    name = "vector_store"
    description = "Persist/retrieve text snippets in a local vector DB (Chroma)."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["add", "query"], "description": "Add or query."},
            "text": {"type": "string", "description": "Text to add or query against."},
            "top_k": {"type": "integer", "description": "Top K for query.", "default": 3},
            "namespace": {"type": "string", "description": "Collection name.", "default": "default"},
        },
        "required": ["action", "text"],
    }

    def run(self, action: str, text: str, top_k: int = 3, namespace: str = "default", **_) -> ToolResult:
        client = chromadb.PersistentClient(path=settings.chroma_path, settings=ChromaSettings(anonymized_telemetry=False))
        col = client.get_or_create_collection(namespace)
        if action == "add":
            col.add(
                documents=[text],
                ids=[f"doc-{col.count()+1}"],
                metadatas=[{}],
            )
            return ToolResult(content=f"Added to collection '{namespace}'.", meta={"count": col.count()})
        else:
            res = col.query(query_texts=[text], n_results=top_k)
            # Normalize results
            hits: List[Dict[str, Any]] = []
            for i, doc in enumerate(res.get("documents", [[]])[0]):
                hits.append({"rank": i+1, "text": doc, "distance": None})
            return ToolResult(content=str(hits), meta={"k": top_k})
