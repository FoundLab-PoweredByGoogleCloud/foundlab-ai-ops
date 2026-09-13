from foundlab_ai_ops.engine import plan
from foundlab_ai_ops.models import (
    ComputeClass,
    DecisionStatus,
    ExecutionMode,
    Provider,
    Task,
)
from foundlab_ai_ops.quota import QuotaSnapshot


def task(**overrides):
    payload = {
        "id": "kat",
        "objective": "verify deterministic multi-provider routing",
        "risk": "medium",
        "execution": {"type": "repo_scan"},
        "requirements": {"repositories": True},
        "expected": {"complexity": "medium"},
    }
    payload.update(overrides)
    return Task.model_validate(payload)


def test_routine_repo_scan_uses_openai_codex_balanced():
    decision = plan(task(), QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.allow
    assert decision.provider == Provider.openai
    assert decision.surface == "codex"
    assert decision.compute_class == ComputeClass.balanced
    assert decision.fast_mode is False


def test_high_complexity_uses_professional_compute():
    t = task(expected={"complexity": "high"})
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.compute_class == ComputeClass.professional


def test_gcp_requirement_routes_google():
    t = task(requirements={"repositories": True, "gcp": True})
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.provider == Provider.google
    assert decision.surface == "google_coding"


def test_managed_mcp_only_disqualifies_deterministic_routing():
    t = task(
        execution={"type": "general"},
        requirements={"managed_mcp": ["logging"]},
        expected={"complexity": "low", "repetitive": True},
    )
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.provider == Provider.google
    assert decision.surface != "local_python"
    assert "mcp_registry" in decision.required_checks


def test_explicit_deterministic_provider_is_blocked_for_managed_mcp():
    t = task(
        execution={"type": "general", "provider_preference": "deterministic"},
        requirements={"managed_mcp": ["logging"]},
        expected={"complexity": "low", "repetitive": True},
    )
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.blocked
    assert decision.provider == Provider.deterministic
    assert decision.surface == "local_python"
    assert decision.max_agents == 0
    assert "provider_compatibility" in decision.required_checks
    assert "mcp_registry" in decision.required_checks


def test_google_docs_adds_developer_knowledge_mcp_and_registry_check():
    t = task(requirements={"google_docs": True})
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.provider == Provider.google
    assert "developer_knowledge" in decision.managed_mcp
    assert "google_developer_knowledge" in decision.required_sources
    assert "mcp_registry" in decision.required_checks


def test_bulk_routes_batch_mode():
    t = task(execution={"type": "bulk", "provider_preference": "google"})
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.execution_mode == ExecutionMode.batch
    assert decision.surface == "gemini_api"


def test_remote_write_requires_review():
    t = task(execution={"type": "implementation", "remote_writes": True})
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.review
    assert decision.external_writes is False


def test_critical_quota_blocks_noncritical_codex_work():
    decision = plan(task(), QuotaSnapshot(100, 5))
    assert decision.decision == DecisionStatus.blocked
    assert decision.provider == Provider.openai
    assert decision.surface == "codex"
    assert decision.max_agents == 0


def test_google_task_is_not_misrepresented_as_same_chatgpt_quota_domain():
    t = task(requirements={"gcp": True})
    decision = plan(t, QuotaSnapshot(100, 5))
    assert decision.provider == Provider.google
    assert decision.decision != DecisionStatus.blocked


def test_critical_task_survives_critical_quota():
    t = task(risk="critical", execution={"type": "incident"})
    decision = plan(t, QuotaSnapshot(100, 5))
    assert decision.decision in {DecisionStatus.allow, DecisionStatus.review}
