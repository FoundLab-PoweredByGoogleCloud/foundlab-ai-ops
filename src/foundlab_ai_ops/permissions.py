from __future__ import annotations

from typing import Literal

from .config import policy

PermissionResult = Literal["allow", "review", "deny", "explicit"]


def evaluate(system: str, action: str) -> PermissionResult:
    data = policy("permissions")
    systems = data.get("systems", {})
    defaults = data.get("defaults", {})

    entry = systems.get(system, {})
    if action in entry:
        result = entry[action]
    elif action in {"read", "write", "destructive"}:
        result = defaults.get(action, "review")
    else:
        result = "review"

    if result not in {"allow", "review", "deny", "explicit"}:
        raise ValueError(f"Invalid permission result for {system}.{action}: {result}")
    return result
