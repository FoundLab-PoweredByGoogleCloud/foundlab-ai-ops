from __future__ import annotations

from .config import policy
from .models import Complexity, Decision, DecisionStatus, Risk, Task
from .quota import QuotaSnapshot, mode


def _base_model_class(task: Task) -> tuple[str, list[str]]:
    e = task.expected
    rationale: list[str] = []

    if e.repetitive and e.complexity == Complexity.low:
        return "luna", ["bounded repetitive work"]

    if e.adversarial_review or e.unresolved_after_escalation:
        return "astra", ["explicit escalation/adversarial condition"]

    if task.risk == Risk.critical or e.complexity == Complexity.frontier:
        return "astra", ["critical risk or frontier complexity"]

    if task.execution.type in {"architecture", "security", "implementation", "debugging", "release"}:
        return "sol", ["complex professional engineering class"]

    if e.complexity == Complexity.high:
        return "sol", ["high complexity"]

    return "terra", ["routine exploration or general work"]


def plan(task: Task, quota: QuotaSnapshot) -> Decision:
    routing = policy("model-routing")
    quota_policy = policy("quota")
    quota_mode = mode(quota, quota_policy)

    model_class, rationale = _base_model_class(task)
    reasoning = routing["classes"][model_class]["default_reasoning"]
    max_agents = int(routing["defaults"]["max_parallel_agents"])
    profile = "standard"

    if task.risk in {Risk.high, Risk.critical} or task.execution.type == "release":
        profile = "conservative"
        max_agents = 1

    if quota_mode == "AMBER":
        rationale.append("weekly quota is AMBER")
        if model_class == "astra" and task.risk != Risk.critical:
            model_class, reasoning = "sol", "medium"
            rationale.append("Astra restricted outside critical work")
    elif quota_mode == "RED":
        rationale.append("weekly quota is RED")
        max_agents = 1
        if task.risk not in {Risk.high, Risk.critical}:
            model_class, reasoning = "terra", "low"
            rationale.append("preserving reserve for high-risk work")
    elif quota_mode == "CRITICAL":
        rationale.append("weekly quota is CRITICAL")
        max_agents = 0
        if task.risk != Risk.critical:
            return Decision(
                decision=DecisionStatus.blocked,
                profile="incident",
                model_class="terra",
                reasoning="low",
                fast_mode=False,
                max_agents=0,
                sandbox="read-only",
                external_writes=False,
                required_sources=_sources(task),
                required_checks=["quota_guard"],
                rationale=rationale + ["non-critical work blocked to preserve incident reserve"],
            )
        profile = "incident"

    if task.execution.destructive_operations:
        status = DecisionStatus.review
        rationale.append("destructive operation requires explicit review")
    elif task.execution.remote_writes:
        status = DecisionStatus.review
        rationale.append("remote write requires explicit review")
    else:
        status = DecisionStatus.allow

    checks = ["quota_guard", "secret_scan"]
    if task.requirements.repositories:
        checks.append("repository_state")

    return Decision(
        decision=status,
        profile=profile,
        model_class=model_class,
        reasoning=reasoning,
        fast_mode=False,
        max_agents=max_agents,
        sandbox="workspace-write" if status != DecisionStatus.blocked else "read-only",
        external_writes=False,
        required_sources=_sources(task),
        required_checks=checks,
        rationale=rationale,
    )


def _sources(task: Task) -> list[str]:
    r = task.requirements
    ordered: list[str] = []
    for name, enabled in (
        ("git", r.repositories),
        ("github", r.github),
        ("gcp", r.gcp),
        ("linear", r.linear),
        ("google_drive", r.drive),
        ("web", r.web),
    ):
        if enabled:
            ordered.append(name)
    return ordered
