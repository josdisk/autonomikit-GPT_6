from __future__ import annotations
from typing import List, Dict, Any, Optional
from loguru import logger
from ..llm import LLMClient, tool_schema
from ..tools.base import Tool, ToolResult

SYSTEM_PROMPT = (
    "You are AutonomiKit-GPT, a helpful research & writing agent. "
    "Decide when to call tools. If a tool is used, return a final, clear answer after using it. "
    "Never reveal hidden chain-of-thought; only share results, summaries, and citations when possible."
)

class Planner:
    def __init__(self, tools: List[Tool], model: Optional[str] = None):
        self.client = LLMClient(model=model)
        self.tools = {t.name: t for t in tools}

    def run(self, task: str, max_steps: int = 5) -> str:
        messages: List[Dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT},
                                          {"role": "user", "content": task}]
        tools_schema = [
            tool_schema(name=t.name, description=t.description, parameters=t.parameters)
            for t in self.tools.values()
        ]

        for step in range(max_steps):
            logger.debug(f"Step {step+1}/{max_steps}")
            resp = self.client.chat(messages, tools=tools_schema)
            choice = resp["choices"][0]
            message = choice["message"]

            # Tool call?
            tcs = message.get("tool_calls") or []
            if tcs:
                for tc in tcs:
                    fn = tc["function"]["name"]
                    args = tc["function"].get("arguments") or "{}"
                    try:
                        parsed = eval(args, {"__builtins__": {}}) if isinstance(args, str) else args
                    except Exception:
                        parsed = {}
                    tool = self.tools.get(fn)
                    if not tool:
                        messages.append({"role": "tool", "tool_call_id": tc.get("id"), "name": fn,
                                         "content": f"Tool '{fn}' not found."})
                        continue
                    result: ToolResult = tool.run(**parsed)
                    messages.append({"role": "tool", "tool_call_id": tc.get("id"), "name": fn,
                                     "content": result.content})
                # Continue the loop for model to digest tool outputs
                continue

            # No tool call; return assistant's content
            content = message.get("content") or ""
            return content.strip()

        return "Reached max steps without a final answer."
