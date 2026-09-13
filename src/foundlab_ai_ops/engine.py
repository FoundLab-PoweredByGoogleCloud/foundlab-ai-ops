from __future__ import annotations

from .config import policy
from .models import (
    Complexity,
    ComputeClass,
    Decision,
    DecisionStatus,
    ExecutionMode,
    PermissionCheck,
    Provider,
    Risk,
    Task,
)
from .permissions import evaluate as evaluate_permission
from .quota import QuotaSnapshot, mode


ENGINEERING_TYPES = {
    "architecture",
    "security",
    "implementation",
    "debugging",
    "release",
    "repo_scan",
}


def _compute_class(task: Task) -> tuple[ComputeClass, list[str]]:
    e = task.expected

    if e.repetitive and e.complexity == Complexity.low:
        return ComputeClass.economy, ["bounded repetitive work"]

    if e.adversarial_review or e.unresolved_after_escalation:
        return ComputeClass.frontier, ["explicit escalation/adversarial condition"]

    if task.risk == Risk.critical or e.complexity == Complexity.frontier:
        return ComputeClass.frontier, ["critical risk or frontier complexity"]

    if task.execution.type in {"architecture", "security", "implementation", "debugging", "release"}:
        return ComputeClass.professional, ["complex professional engineering class"]

    if e.complexity == Complexity.high:
        return ComputeClass.professional, ["high complexity"]

    return ComputeClass.balanced, ["routine exploration or general work"]


def _requires_remote_capability(task: Task) -> bool:
    if any(
        [
            task.requirements.web,
            task.requirements.github,
            task.requirements.gcp,
            task.requirements.google_docs,
            task.requirements.linear,
            task.requirements.drive,
            bool(task.requirements.managed_mcp),
        ]
    ):
        return True

    return any(
        request.system not in {"workspace", "shell"}
        for request in task.requested_actions
    )


def _provider(task: Task) -> tuple[Provider, str]:
    routing = policy("provider-routing")
    defaults = routing.get("defaults", {})

    if task.execution.provider_preference is not None:
        return task.execution.provider_preference, "explicit provider preference"

    if (
        task.expected.repetitive
        and task.expected.complexity == Complexity.low
        and not _requires_remote_capability(task)
        and not task.requested_actions
    ):
        return Provider.deterministic, "bounded work can run without an LLM provider"

    # v0.2 managed_mcp currently denotes entries from mcp/google-managed.yaml.
    # A task that requires one of those endpoints must not be routed to local-only
    # deterministic execution.
    if (
        task.requirements.gcp
        or task.requirements.google_docs
        or task.requirements.managed_mcp
    ):
        return Provider.google, "Google authority/capabilities are required"

    return Provider(str(defaults.get("provider", "openai"))), "default agentic provider"


def _provider_compatibility_issue(task: Task, provider: Provider) -> str | None:
    if provider == Provider.deterministic and _requires_remote_capability(task):
        return (
            "deterministic provider is incompatible with required remote "
            "capabilities; select an agentic provider or remove the remote dependency"
        )
    return None


def _execution_mode(task: Task) -> ExecutionMode:
    if task.execution.execution_mode_preference is not None:
        return task.execution.execution_mode_preference
    if task.execution.type in {"bulk", "evaluation", "large_batch"}:
        return ExecutionMode.batch
    if task.execution.type in {"long_running", "deep_research"}:
        return ExecutionMode.background
    if task.expected.latency == "interactive":
        return ExecutionMode.interactive
    if task.expected.latency == "deferred":
        return ExecutionMode.flex
    return ExecutionMode.standard


def _surface(task: Task, provider: Provider, execution_mode: ExecutionMode) -> str:
    if task.execution.surface_preference:
        return task.execution.surface_preference

    routing = policy("provider-routing")
    defaults = routing.get("defaults", {})

    if provider == Provider.deterministic:
        return "local_python"

    if provider == Provider.openai:
        surfaces = defaults.get("openai_surface", {})
        key = "engineering" if task.execution.type in ENGINEERING_TYPES else "general"
        return str(surfaces.get(key, "codex" if key == "engineering" else "openai_api"))

    if execution_mode in {ExecutionMode.batch, ExecutionMode.flex, ExecutionMode.background}:
        return "gemini_api"

    surfaces = defaults.get("google_surface", {})
    key = "engineering" if task.execution.type in ENGINEERING_TYPES else "general"
    return str(surfaces.get(key, "google_coding" if key == "engineering" else "gemini_api"))


def _reasoning(compute_class: ComputeClass) -> str:
    mapping = policy("model-routing")["classes"]
    return str(mapping[compute_class.value]["default_reasoning"])


def _permission_checks(task: Task) -> list[PermissionCheck]:
    return [
        PermissionCheck(
            system=request.system,
            action=request.action,
            result=evaluate_permission(request.system, request.action),
        )
        for request in task.requested_actions
    ]


def _permission_status(checks: list[PermissionCheck]) -> DecisionStatus:
    if any(check.result == "deny" for check in checks):
        return DecisionStatus.deny
    if any(check.result in {"review", "explicit"} for check in checks):
        return DecisionStatus.review
    return DecisionStatus.allow


def plan(task: Task, quota: QuotaSnapshot) -> Decision:
    model_routing = policy("model-routing")
    quota_policy = policy("quota")
    quota_mode = mode(quota, quota_policy)

    compute_class, rationale = _compute_class(task)
    provider, provider_reason = _provider(task)
    rationale.append(provider_reason)
    execution_mode = _execution_mode(task)
    surface = _surface(task, provider, execution_mode)
    reasoning = _reasoning(compute_class)
    max_agents = int(model_routing["defaults"]["max_parallel_agents"])
    profile = "standard"
    permission_checks = _permission_checks(task)
    permission_status = _permission_status(permission_checks)

    if task.risk in {Risk.high, Risk.critical} or task.execution.type == "release":
        profile = "conservative"
        max_agents = 1

    # A hard policy DENY outranks routing incompatibility, quota pressure and
    # other operational blockers. Preserve the strongest prohibition.
    if permission_status == DecisionStatus.deny:
        return Decision(
            decision=DecisionStatus.deny,
            profile="conservative",
            provider=provider,
            surface=surface,
            execution_mode=execution_mode,
            compute_class=compute_class,
            reasoning=reasoning,
            fast_mode=False,
            max_agents=0,
            sandbox="read-only",
            external_writes=False,
            required_sources=_sources(task),
            required_checks=_checks(task),
            managed_mcp=_managed_mcp(task),
            telemetry_required=True,
            permission_checks=permission_checks,
            rationale=[
                *rationale,
                "one or more requested capabilities are denied by policy",
            ],
        )

    compatibility_issue = _provider_compatibility_issue(task, provider)
    if compatibility_issue is not None:
        return Decision(
            decision=DecisionStatus.blocked,
            profile="conservative",
            provider=provider,
            surface=surface,
            execution_mode=execution_mode,
            compute_class=compute_class,
            reasoning=reasoning,
            fast_mode=False,
            max_agents=0,
            sandbox="read-only",
            external_writes=False,
            required_sources=_sources(task),
            required_checks=[*_checks(task), "provider_compatibility"],
            managed_mcp=_managed_mcp(task),
            telemetry_required=True,
            permission_checks=permission_checks,
            rationale=[*rationale, compatibility_issue],
        )

    # The local snapshot is currently scoped to ChatGPT Work/Codex. It must not
    # be presented as a universal live quota for Google or API billing domains.
    if quota_mode == "AMBER":
        rationale.append("local ChatGPT Work/Codex quota snapshot is AMBER")
        if (
            provider == Provider.openai
            and surface == "codex"
            and compute_class == ComputeClass.frontier
            and task.risk != Risk.critical
        ):
            compute_class = ComputeClass.professional
            reasoning = _reasoning(compute_class)
            rationale.append("frontier Codex compute restricted outside critical work")
    elif quota_mode == "RED":
        rationale.append("local ChatGPT Work/Codex quota snapshot is RED")
        if provider == Provider.openai and surface == "codex":
            max_agents = 1
            if task.risk not in {Risk.high, Risk.critical}:
                compute_class = ComputeClass.balanced
                reasoning = _reasoning(compute_class)
                rationale.append("preserving Codex reserve for high-risk work")
    elif quota_mode == "CRITICAL":
        rationale.append("local ChatGPT Work/Codex quota snapshot is CRITICAL")
        if provider == Provider.openai and surface == "codex":
            max_agents = 0
            if task.risk != Risk.critical:
                return Decision(
                    decision=DecisionStatus.blocked,
                    profile="incident",
                    provider=provider,
                    surface=surface,
                    execution_mode=execution_mode,
                    compute_class=ComputeClass.balanced,
                    reasoning="low",
                    fast_mode=False,
                    max_agents=0,
                    sandbox="read-only",
                    external_writes=False,
                    required_sources=_sources(task),
                    required_checks=_checks(task),
                    managed_mcp=_managed_mcp(task),
                    telemetry_required=True,
                    permission_checks=permission_checks,
                    rationale=rationale + ["non-critical Codex work blocked to preserve incident reserve"],
                )
            profile = "incident"

    if task.execution.destructive_operations:
        status = DecisionStatus.review
        rationale.append("destructive operation requires explicit review")
    elif task.execution.remote_writes:
        status = DecisionStatus.review
        rationale.append("remote write requires explicit review")
    elif permission_status == DecisionStatus.review:
        status = DecisionStatus.review
        rationale.append("one or more requested capabilities require review/explicit approval")
    else:
        status = DecisionStatus.allow

    return Decision(
        decision=status,
        profile=profile,
        provider=provider,
        surface=surface,
        execution_mode=execution_mode,
        compute_class=compute_class,
        reasoning=reasoning,
        fast_mode=False,
        max_agents=max_agents,
        sandbox="read-only" if status == DecisionStatus.deny else "workspace-write",
        external_writes=False,
        required_sources=_sources(task),
        required_checks=_checks(task),
        managed_mcp=_managed_mcp(task),
        telemetry_required=True,
        permission_checks=permission_checks,
        rationale=rationale,
    )


def _checks(task: Task) -> list[str]:
    checks = ["quota_guard", "secret_scan", "provider_route"]
    if task.requirements.repositories:
        checks.append("repository_state")
    if task.requested_actions:
        checks.append("permission_guard")
    # Use effective dependencies, not only explicitly declared ones.
    # google_docs implicitly adds developer_knowledge in _managed_mcp().
    if _managed_mcp(task):
        checks.append("mcp_registry")
    return checks


def _managed_mcp(task: Task) -> list[str]:
    required = list(task.requirements.managed_mcp)
    if task.requirements.google_docs and "developer_knowledge" not in required:
        required.append("developer_knowledge")
    return required


def _sources(task: Task) -> list[str]:
    r = task.requirements
    ordered: list[str] = []
    for name, enabled in (
        ("git", r.repositories),
        ("github", r.github),
        ("gcp", r.gcp),
        ("google_developer_knowledge", r.google_docs),
        ("linear", r.linear),
        ("google_drive", r.drive),
        ("web", r.web),
    ):
        if enabled:
            ordered.append(name)
    return ordered
