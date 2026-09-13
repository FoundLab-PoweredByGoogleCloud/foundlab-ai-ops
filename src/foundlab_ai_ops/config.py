from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    explicit = os.getenv("FOUNDLAB_AI_OPS_HOME")
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if (root / "policies").is_dir():
            return root
        raise RuntimeError("FOUNDLAB_AI_OPS_HOME does not contain policies/")

    candidates = [Path.cwd(), *Path.cwd().parents, Path(__file__).resolve().parents[2]]
    for candidate in candidates:
        if (candidate / "policies" / "model-routing.yaml").exists():
            return candidate
    raise RuntimeError(
        "Could not locate FoundLab AI Ops repository. "
        "Run inside the repo or set FOUNDLAB_AI_OPS_HOME."
    )


def load_yaml(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    with target.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle) or {}
    if not isinstance(value, dict):
        raise ValueError(f"Expected mapping in {target}")
    return value


def policy(name: str) -> dict[str, Any]:
    return load_yaml(repo_root() / "policies" / f"{name}.yaml")
