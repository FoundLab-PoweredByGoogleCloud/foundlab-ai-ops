from foundlab_ai_ops.engine import plan
from foundlab_ai_ops.models import DecisionStatus, Task
from foundlab_ai_ops.quota import QuotaSnapshot


def task(**overrides):
    payload = {
        "id": "kat",
        "objective": "verify deterministic routing",
        "risk": "medium",
        "execution": {"type": "repo_scan"},
        "requirements": {"repositories": True},
        "expected": {"complexity": "medium"},
    }
    payload.update(overrides)
    return Task.model_validate(payload)


def test_routine_repo_scan_uses_terra():
    decision = plan(task(), QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.allow
    assert decision.model_class == "terra"
    assert decision.fast_mode is False


def test_high_complexity_uses_sol():
    t = task(expected={"complexity": "high"})
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.model_class == "sol"


def test_remote_write_requires_review():
    t = task(execution={"type": "implementation", "remote_writes": True})
    decision = plan(t, QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.review
    assert decision.external_writes is False


def test_critical_quota_blocks_noncritical_work():
    decision = plan(task(), QuotaSnapshot(100, 5))
    assert decision.decision == DecisionStatus.blocked
    assert decision.max_agents == 0


def test_critical_task_survives_critical_quota():
    t = task(risk="critical", execution={"type": "incident"})
    decision = plan(t, QuotaSnapshot(100, 5))
    assert decision.decision in {DecisionStatus.allow, DecisionStatus.review}
