from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", "dist", "build"}
TEXT_EXTENSIONS = {
    ".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt", ".ini", ".cfg", ".sh", ".ps1"
}

SECRET_PATTERNS = {
    "private-key-header": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai-like-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "google-api-key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}


def files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        yield path


def validate_structured(path: Path) -> None:
    if path.suffix in {".yaml", ".yml"}:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    elif path.suffix == ".json":
        json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix == ".toml":
        with path.open("rb") as handle:
            tomllib.load(handle)


def validate_examples() -> list[str]:
    failures: list[str] = []
    schema_path = ROOT / "contracts" / "task.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    for path in sorted((ROOT / "examples" / "tasks").glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        for error in validator.iter_errors(payload):
            location = ".".join(str(item) for item in error.absolute_path)
            failures.append(
                f"{path.relative_to(ROOT)}: schema error at {location or '<root>'}: {error.message}"
            )
    return failures


def scan_secrets(path: Path) -> list[str]:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    return [name for name, pattern in SECRET_PATTERNS.items() if pattern.search(text)]


def main() -> int:
    failures: list[str] = []
    for path in files():
        try:
            validate_structured(path)
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: parse error: {exc}")
        for finding in scan_secrets(path):
            failures.append(f"{path.relative_to(ROOT)}: possible secret: {finding}")

    failures.extend(validate_examples())

    if failures:
        print("Repository validation failed:")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("Repository validation PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
