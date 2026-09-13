from __future__ import annotations

import shutil
import subprocess
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class CodexDiagnostics:
    installed: bool
    version: str | None = None
    config_found: bool = False
    approval_policy: str | None = None
    sandbox_mode: str | None = None
    secret_name_exclusions_enabled: bool | None = None
    fast_mode_pinned: bool | None = None
    memory_external_context_guard: bool | None = None
    warnings: list[str] | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def diagnose(config_path: Path | None = None) -> CodexDiagnostics:
    warnings: list[str] = []
    installed = shutil.which("codex") is not None
    version = None

    if installed:
        try:
            result = subprocess.run(
                ["codex", "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
            version = (result.stdout or result.stderr).strip() or None
        except subprocess.TimeoutExpired:
            warnings.append("codex --version timed out")

    path = config_path or (Path.home() / ".codex" / "config.toml")
    if not path.exists():
        warnings.append("Codex config.toml not found")
        return CodexDiagnostics(
            installed=installed,
            version=version,
            config_found=False,
            warnings=warnings,
        )

    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        warnings.append(f"Could not parse Codex config: {exc}")
        return CodexDiagnostics(
            installed=installed,
            version=version,
            config_found=True,
            warnings=warnings,
        )

    shell_policy = data.get("shell_environment_policy", {})
    ignore_default = shell_policy.get("ignore_default_excludes")
    secret_exclusions = None if ignore_default is None else (ignore_default is False)

    features = data.get("features", {})
    memories = data.get("memories", {})

    if ignore_default is not False:
        warnings.append(
            "Automatic KEY/SECRET/TOKEN name exclusions are not explicitly enabled."
        )
    if data.get("sandbox_mode") == "danger-full-access":
        warnings.append("sandbox_mode is danger-full-access")
    if data.get("approval_policy") == "never":
        warnings.append("approval_policy is never")
    if features.get("fast_mode") is True:
        warnings.append("fast_mode is pinned on")

    return CodexDiagnostics(
        installed=installed,
        version=version,
        config_found=True,
        approval_policy=data.get("approval_policy"),
        sandbox_mode=data.get("sandbox_mode"),
        secret_name_exclusions_enabled=secret_exclusions,
        fast_mode_pinned=features.get("fast_mode"),
        memory_external_context_guard=memories.get("disable_on_external_context"),
        warnings=warnings,
    )
