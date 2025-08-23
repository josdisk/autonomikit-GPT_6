from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from loguru import logger
from .config import settings
import httpx
import json
import os

# We use OpenAI's SDK style but keep it flexible via envs.
try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore

@dataclass
class ChatMessage:
    role: str
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None

class LLMClient:
    def __init__(self, model: Optional[str] = None):
        self.model = model or settings.llm_model
        self.provider = settings.provider

        if self.provider == "openai":
            if not settings.openai_api_key:
                logger.warning("OPENAI_API_KEY not set; client calls will fail.")
            self.client = OpenAI(api_key=settings.openai_api_key)
        elif self.provider == "openrouter":
            if not settings.openrouter_api_key:
                logger.warning("OPENROUTER_API_KEY not set; client calls will fail.")
            # We'll use direct HTTP for OpenRouter
            self.client = None
        elif self.provider == "azure":
            # Azure OpenAI via OpenAI SDK configuration (envs)
            if not (settings.azure_api_key and settings.azure_endpoint and settings.azure_deployment):
                logger.warning("Azure OpenAI envs not set; calls will fail.")
            os.environ["AZURE_OPENAI_API_KEY"] = settings.azure_api_key or ""
            os.environ["AZURE_OPENAI_ENDPOINT"] = settings.azure_endpoint or ""
            os.environ["OPENAI_API_VERSION"] = "2024-07-01-preview"
            self.client = OpenAI(azure_endpoint=settings.azure_endpoint, api_key=settings.azure_api_key)
            self.model = settings.azure_deployment or self.model
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        logger.debug(f"Chat call -> provider={self.provider}, model={self.model}")
        if self.provider == "openai" or self.provider == "azure":
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools or None,
                tool_choice="auto" if tools else "none",
                temperature=0.2,
                timeout=settings.timeout_seconds,
            )
            return resp.model_dump()  # type: ignore

        elif self.provider == "openrouter":
            headers = {
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "HTTP-Referer": "https://github.com/josdisk/AutonomiKit-GPT",
                "X-Title": "AutonomiKit-GPT",
                "Content-Type": "application/json",
            }
            payload = {
                "model": settings.openrouter_model or self.model,
                "messages": messages,
                "temperature": 0.2,
                **({"tools": tools, "tool_choice": "auto"} if tools else {}),
            }
            with httpx.Client(timeout=settings.timeout_seconds) as client:
                r = client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                r.raise_for_status()
                return r.json()
        else:
            raise RuntimeError("Unsupported provider")

def tool_schema(name: str, description: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters,
        },
    }
