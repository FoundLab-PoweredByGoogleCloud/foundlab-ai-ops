from __future__ import annotations

from pathlib import Path

import yaml

from .config import repo_root


def recall(query: str) -> list[dict[str, str]]:
    """Search public institutional memory entries deterministically.

    This v0.1 implementation performs a conservative text search over YAML/Markdown.
    It does not infer semantic equivalence and never claims freshness beyond metadata.
    """
    root = repo_root() / "memory-bank"
    needle = query.casefold().strip()
    if not needle:
        return []

    hits: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".yaml", ".yml", ".md"}:
            continue
        text = path.read_text(encoding="utf-8")
        if needle not in text.casefold():
            continue

        item = {
            "path": str(path.relative_to(repo_root())),
            "authority": "repository",
            "freshness": "unknown",
        }
        if path.suffix.lower() in {".yaml", ".yml"}:
            try:
                data = yaml.safe_load(text)
                if isinstance(data, dict):
                    item["freshness"] = str(data.get("freshness", data.get("version", "unknown")))
            except yaml.YAMLError:
                pass
        hits.append(item)
    return hits
