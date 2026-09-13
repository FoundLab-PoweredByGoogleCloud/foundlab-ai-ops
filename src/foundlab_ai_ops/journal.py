from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .quota import state_dir


def append_decision(task_payload: dict, decision_payload: dict) -> Path:
    journal = state_dir() / "journal.jsonl"
    canonical = json.dumps(task_payload, sort_keys=True, separators=(",", ":")).encode()
    record = {
        "decision_id": f"aio_{uuid4().hex}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task_hash": "sha256:" + hashlib.sha256(canonical).hexdigest(),
        "task": task_payload,
        "decision": decision_payload,
    }
    with journal.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return journal
