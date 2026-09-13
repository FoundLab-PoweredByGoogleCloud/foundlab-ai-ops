from __future__ import annotations

import json
import sys

from .permissions import evaluate


def _system_action(tool_name: str, tool_input: dict) -> tuple[str, str]:
    if tool_name.startswith("mcp_"):
        # MCP tool names are server/tool specific. Unknown writes are never
        # auto-approved by the FoundLab hook.
        return "mcp", "write"

    if tool_name in {"write_file", "replace"}:
        return "workspace", "write"

    if tool_name == "run_shell_command":
        command = str(tool_input.get("command", "")).casefold()
        destructive_markers = [
            " rm ",
            "del ",
            "remove-item",
            "git push",
            "git reset --hard",
            "terraform apply",
            "gcloud run deploy",
            "gcloud projects add-iam-policy-binding",
        ]
        if any(marker in f" {command}" for marker in destructive_markers):
            return "shell", "destructive"
        return "shell", "write"

    return "workspace", "read"


def gemini_before_tool(payload: dict) -> dict:
    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        tool_input = {}

    system, action = _system_action(tool_name, tool_input)
    result = evaluate(system, action)

    if result == "deny":
        return {
            "decision": "deny",
            "reason": f"FoundLab policy denied {system}.{action}",
        }

    if result in {"review", "explicit"}:
        # A hook cannot manufacture human approval. Deny the automatic call and
        # force the agent/user to use an explicitly authorized path.
        return {
            "decision": "deny",
            "reason": (
                f"FoundLab policy requires {result} authorization for "
                f"{system}.{action}; automatic tool execution was blocked."
            ),
        }

    return {"decision": "allow"}


def run_gemini_before_tool() -> int:
    try:
        payload = json.load(sys.stdin)
        result = gemini_before_tool(payload)
        sys.stdout.write(json.dumps(result))
        return 0
    except Exception as exc:
        # Fail closed for a policy hook. Gemini hook exit code 2 blocks target action.
        sys.stderr.write(f"FoundLab policy hook failure: {exc}")
        return 2
