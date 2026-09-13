from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class QuotaSnapshot:
    five_hour_remaining: int = 100
    weekly_remaining: int = 100


def state_dir() -> Path:
    target = Path.home() / ".foundlab-ai-ops"
    target.mkdir(parents=True, exist_ok=True)
    return target


def state_file() -> Path:
    return state_dir() / "state.json"


def load_quota() -> QuotaSnapshot:
    path = state_file()
    if not path.exists():
        return QuotaSnapshot()
    raw = json.loads(path.read_text(encoding="utf-8"))
    return QuotaSnapshot(
        five_hour_remaining=int(raw.get("five_hour_remaining", 100)),
        weekly_remaining=int(raw.get("weekly_remaining", 100)),
    )


def set_quota(*, five_hour: int, weekly: int) -> QuotaSnapshot:
    if not 0 <= five_hour <= 100 or not 0 <= weekly <= 100:
        raise ValueError("Quota percentages must be between 0 and 100.")
    snapshot = QuotaSnapshot(five_hour, weekly)
    state_file().write_text(
        json.dumps(
            {
                "five_hour_remaining": snapshot.five_hour_remaining,
                "weekly_remaining": snapshot.weekly_remaining,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return snapshot


def mode(snapshot: QuotaSnapshot, policy: dict) -> str:
    weekly = snapshot.weekly_remaining
    thresholds = policy["thresholds"]
    if weekly < int(thresholds["critical_below"]):
        return "CRITICAL"
    if weekly < int(thresholds["red_below"]):
        return "RED"
    if weekly < int(thresholds["amber_below"]):
        return "AMBER"
    return "GREEN"
