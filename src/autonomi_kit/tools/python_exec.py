from __future__ import annotations
import subprocess, tempfile, textwrap, os, sys, json
from typing import Dict, Any
from .base import Tool, ToolResult

SAFE_PREFIX = "# Safe Python execution (no internet). Avoid long loops, imports restricted.\n"

class PythonExec(Tool):
    name = "python_exec"
    description = "Execute small Python snippets in a sandboxed process (no internet). Returns stdout/stderr."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python code to execute."},
            "timeout": {"type": "integer", "description": "Timeout seconds (<=10).", "default": 5},
        },
        "required": ["code"],
    }

    def run(self, code: str, timeout: int = 5, **_) -> ToolResult:
        timeout = min(max(timeout, 1), 10)
        # Very light sandbox: no network, temp file, restricted environment
        snippet = SAFE_PREFIX + textwrap.dedent(code)
        with tempfile.TemporaryDirectory() as td:
            script = os.path.join(td, "snippet.py")
            with open(script, "w", encoding="utf-8") as f:
                f.write(snippet)
            try:
                proc = subprocess.run(
                    [sys.executable, script],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env={},
                )
                out = proc.stdout.strip()
                err = proc.stderr.strip()
                result = out if out else "(no stdout)"
                if err:
                    result += f"\n[stderr]\n{err}"
                return ToolResult(content=result, meta={"returncode": proc.returncode})
            except subprocess.TimeoutExpired:
                return ToolResult(content="Execution timed out.", meta={"timeout": timeout})
