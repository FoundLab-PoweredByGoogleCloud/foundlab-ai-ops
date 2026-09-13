from __future__ import annotations

from .config import policy


def authority_for(topic: str) -> str:
    data = policy("sources")
    authority = data.get("authority", {})
    if topic not in authority:
        raise KeyError(f"No authority registered for topic: {topic}")
    return str(authority[topic])


def known_topics() -> dict[str, str]:
    data = policy("sources")
    return {str(k): str(v) for k, v in data.get("authority", {}).items()}
