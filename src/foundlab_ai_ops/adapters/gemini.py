from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class GoogleCodingDiagnostics:
    gemini_installed: bool
    gemini_binary: str | None = None
    gemini_version: str | None = None
    antigravity_installed: bool = False
    antigravity_binary: str | None = None
    antigravity_version: str | None = None
    settings_found: bool = False
    approval_mode: str | None = None
    environment_redaction: bool | None = None
    telemetry_enabled: bool | None = None
    telemetry_target: str | None = None
    telemetry_log_prompts: bool | None = None
    before_tool_guard_present: bool = False
    warnings: list[str] | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _version(binary: str | None, label: str, warnings: list[str]) -> str | None:
    if not binary:
        return None
    try:
        result = subprocess.run(
            [binary, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return (result.stdout or result.stderr).strip() or None
    except subprocess.TimeoutExpired:
        warnings.append(f"{label} --version timed out")
        return None


def diagnose(settings_path: Path | None = None) -> GoogleCodingDiagnostics:
    warnings: list[str] = []

    gemini_binary = shutil.which("gemini")
    antigravity_binary = shutil.which("agy")

    gemini_version = _version(gemini_binary, "gemini", warnings)
    antigravity_version = _version(antigravity_binary, "agy", warnings)

    if gemini_binary and antigravity_binary:
        warnings.append(
            "Both Gemini CLI and Antigravity CLI are installed; select the surface "
            "that matches the current Google entitlement and task."
        )
    elif not gemini_binary and not antigravity_binary:
        warnings.append("Neither Gemini CLI nor Antigravity CLI was found on PATH.")

    path = settings_path or (Path.home() / ".gemini" / "settings.json")
    if not path.exists():
        warnings.append("Gemini CLI settings.json not found")
        return GoogleCodingDiagnostics(
            gemini_installed=gemini_binary is not None,
            gemini_binary=gemini_binary,
            gemini_version=gemini_version,
            antigravity_installed=antigravity_binary is not None,
            antigravity_binary=antigravity_binary,
            antigravity_version=antigravity_version,
            settings_found=False,
            warnings=warnings,
        )

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        warnings.append(f"Could not parse Gemini settings: {exc}")
        return GoogleCodingDiagnostics(
            gemini_installed=gemini_binary is not None,
            gemini_binary=gemini_binary,
            gemini_version=gemini_version,
            antigravity_installed=antigravity_binary is not None,
            antigravity_binary=antigravity_binary,
            antigravity_version=antigravity_version,
            settings_found=True,
            warnings=warnings,
        )

    general = data.get("general", {})
    security = data.get("security", {})
    redaction = security.get("environmentVariableRedaction", {})
    telemetry = data.get("telemetry", {})
    hooks = data.get("hooks", {})
    before_tool = hooks.get("BeforeTool", [])

    approval_mode = general.get("defaultApprovalMode")
    env_redaction = redaction.get("enabled")

    if approval_mode == "auto_edit":
        warnings.append("defaultApprovalMode auto_edit permits automatic edit tools")
    if env_redaction is not True:
        warnings.append("environment variable secret redaction is not explicitly enabled")
    if telemetry.get("enabled") is True and telemetry.get("logPrompts", True) is True:
        warnings.append("telemetry is enabled with prompt logging; review data policy")

    return GoogleCodingDiagnostics(
        gemini_installed=gemini_binary is not None,
        gemini_binary=gemini_binary,
        gemini_version=gemini_version,
        antigravity_installed=antigravity_binary is not None,
        antigravity_binary=antigravity_binary,
        antigravity_version=antigravity_version,
        settings_found=True,
        approval_mode=approval_mode,
        environment_redaction=env_redaction,
        telemetry_enabled=telemetry.get("enabled"),
        telemetry_target=telemetry.get("target"),
        telemetry_log_prompts=telemetry.get("logPrompts"),
        before_tool_guard_present=bool(before_tool),
        warnings=warnings,
    )
