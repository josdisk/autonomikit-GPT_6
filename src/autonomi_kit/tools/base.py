from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
from loguru import logger

@dataclass
class ToolResult:
    content: str
    meta: Dict[str, Any]

class Tool:
    name: str = "tool"
    description: str = "Base tool"
    parameters: Dict[str, Any] = {"type": "object", "properties": {}, "required": []}

    def run(self, **kwargs) -> ToolResult:  # pragma: no cover
        logger.error("Base tool should not be called directly.")
        return ToolResult(content="", meta={})
