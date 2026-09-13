from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class GcpDiagnostics:
    installed: bool
    project: str | None = None
    account: str | None = None
    impersonation: str | None = None
    application_credentials_env: str | None = None
    persistent_key_risk: bool = False
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _gcloud(*args: str) -> str:
    result = subprocess.run(
        ["gcloud", *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def diagnose() -> GcpDiagnostics:
    if shutil.which("gcloud") is None:
        return GcpDiagnostics(installed=False)

    credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    persistent_key_risk = False
    if credential_path:
        path = Path(credential_path).expanduser()
        persistent_key_risk = path.suffix.lower() == ".json"

    try:
        project = _gcloud("config", "get-value", "project")
        account = _gcloud("config", "get-value", "account")
        impersonation = _gcloud(
            "config", "get-value", "auth/impersonate_service_account"
        )
        return GcpDiagnostics(
            installed=True,
            project=None if project in {"", "(unset)"} else project,
            account=None if account in {"", "(unset)"} else account,
            impersonation=None if impersonation in {"", "(unset)"} else impersonation,
            application_credentials_env=credential_path,
            persistent_key_risk=persistent_key_risk,
        )
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        return GcpDiagnostics(
            installed=True,
            application_credentials_env=credential_path,
            persistent_key_risk=persistent_key_risk,
            error=str(exc),
        )
