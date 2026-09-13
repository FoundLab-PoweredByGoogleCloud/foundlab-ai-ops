from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .config import load_yaml, repo_root
from .engine import plan as make_plan
from .journal import append_decision
from .memory import recall
from .models import Task
from .quota import load_quota, mode as quota_mode, set_quota

app = typer.Typer(help="FoundLab AI Ops control plane")
quota_app = typer.Typer(help="Manage local quota snapshots")
app.add_typer(quota_app, name="quota")
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
