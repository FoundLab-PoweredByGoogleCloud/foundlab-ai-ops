from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .adapters.codex import diagnose as diagnose_codex
from .adapters.gcp import diagnose as diagnose_gcp
from .config import load_yaml, repo_root
from .engine import plan as make_plan
from .journal import append_decision
from .memory import recall
from .models import Task
from .permissions import evaluate as evaluate_permission
from .quota import load_quota, mode as quota_mode, set_quota
from .sources import authority_for, known_topics

app = typer.Typer(help="FoundLab AI Ops control plane")
quota_app = typer.Typer(help="Manage local quota snapshots")
gcp_app = typer.Typer(help="Google Cloud diagnostics")
codex_app = typer.Typer(help="Codex diagnostics")
app.add_typer(quota_app, name="quota")
app.add_typer(gcp_app, name="gcp")
app.add_typer(codex_app, name="codex")
console = Console()


@app.command()
def doctor() -> None:
    """Run deterministic local readiness checks."""
    checks = {
        "python": sys.version_info >= (3, 11),
        "repository": (repo_root() / "policies").is_dir(),
        "git": shutil.which("git") is not None,
        "gcloud": shutil.which("gcloud") is not None,
        "codex": shutil.which("codex") is not None,
    }
    table = Table(title="FoundLab AI Ops — Doctor")
    table.add_column("Check")
    table.add_column("Result")
    for name, ok in checks.items():
        table.add_row(name, "PASS" if ok else "NOT FOUND")
    console.print(table)
    if not checks["python"] or not checks["repository"]:
        raise typer.Exit(code=1)


@app.command("plan")
def plan_command(task_file: Path) -> None:
    """Evaluate a task manifest and emit an execution decision."""
    try:
        payload = load_yaml(task_file)
        task = Task.model_validate(payload["task"])
    except (KeyError, ValidationError, ValueError) as exc:
        console.print(f"[red]Invalid task manifest:[/red] {exc}")
        raise typer.Exit(code=2)

    snapshot = load_quota()
    decision = make_plan(task, snapshot)
    output = decision.model_dump(mode="json")
    append_decision(task.model_dump(mode="json"), output)
    console.print_json(json.dumps(output))


@app.command("authorize")
def authorize(system: str, action: str) -> None:
    """Evaluate one declared capability against FoundLab policy."""
    console.print(
        {
            "system": system,
            "action": action,
            "policy": evaluate_permission(system, action),
            "note": "Provider IAM and product permissions still apply.",
        }
    )


@app.command("source")
def source(topic: str | None = None) -> None:
    """Resolve the authority for a topic, or list known topics."""
    if topic is None:
        console.print(known_topics())
        return
    try:
        console.print({"topic": topic, "authority": authority_for(topic)})
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=2)


@app.command("plugins")
def plugins_command() -> None:
    """List declared plugin capabilities."""
    data = load_yaml(repo_root() / "plugins" / "registry.yaml")
    table = Table(title="Plugin Registry")
    table.add_column("Plugin")
    table.add_column("Type")
    table.add_column("Authority")
    for name, entry in data.get("plugins", {}).items():
        table.add_row(name, str(entry.get("type", "")), ", ".join(entry.get("authority_for", [])))
    console.print(table)


@app.command("skills")
def skills_command() -> None:
    """List registered reusable skills."""
    data = load_yaml(repo_root() / "skills" / "registry.yaml")
    table = Table(title="Skill Registry")
    table.add_column("Skill")
    table.add_column("Version")
    table.add_column("Risk")
    for name, entry in data.get("skills", {}).items():
        table.add_row(name, str(entry.get("version", "")), str(entry.get("risk_class", "")))
    console.print(table)


@app.command("recall")
def recall_command(query: str) -> None:
    """Search the institutional Memory Bank without inventing semantic matches."""
    hits = recall(query)
    if not hits:
        console.print("No institutional memory match.")
        return
    console.print_json(json.dumps(hits))


@gcp_app.command("doctor")
def gcp_doctor() -> None:
    """Inspect local gcloud identity configuration without exposing credentials."""
    result = diagnose_gcp().to_dict()
    console.print_json(json.dumps(result))
    if result.get("persistent_key_risk"):
        console.print(
            "[yellow]Warning:[/yellow] GOOGLE_APPLICATION_CREDENTIALS points to a JSON file. "
            "Prefer short-lived/impersonated credentials where practical."
        )


@codex_app.command("doctor")
def codex_doctor(config: Path | None = None) -> None:
    """Inspect Codex security-relevant configuration without modifying it."""
    result = diagnose_codex(config).to_dict()
    console.print_json(json.dumps(result))


@quota_app.command("status")
def quota_status() -> None:
    snapshot = load_quota()
    policy = load_yaml(repo_root() / "policies" / "quota.yaml")
    console.print(
        {
            "five_hour_remaining": snapshot.five_hour_remaining,
            "weekly_remaining": snapshot.weekly_remaining,
            "mode": quota_mode(snapshot, policy),
            "note": "Manual snapshot; not a claim of live ChatGPT telemetry.",
        }
    )


@quota_app.command("set")
def quota_set(
    five_hour: int = typer.Option(..., min=0, max=100),
    weekly: int = typer.Option(..., min=0, max=100),
) -> None:
    snapshot = set_quota(five_hour=five_hour, weekly=weekly)
    console.print({"saved": True, **snapshot.__dict__})


if __name__ == "__main__":
    app()
