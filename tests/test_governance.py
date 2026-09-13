from foundlab_ai_ops.engine import plan
from foundlab_ai_ops.models import DecisionStatus, Task
from foundlab_ai_ops.quota import QuotaSnapshot


def make_task(action: str):
    return Task.model_validate(
        {
            "id": "governance-kat",
            "objective": "verify capability policy",
            "risk": "medium",
            "requirements": {"gcp": True},
            "requested_actions": [{"system": "gcp", "action": action}],
        }
    )


def test_denied_capability_denies_plan():
    decision = plan(make_task("iam_change"), QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.deny
    assert decision.sandbox == "read-only"


def test_review_capability_requires_review():
    decision = plan(make_task("deploy"), QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.review
    assert decision.external_writes is False


def test_allowed_capability_can_plan():
    decision = plan(make_task("inspect"), QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.allow


def test_denied_capability_precedes_provider_compatibility_block():
    task = Task.model_validate(
        {
            "id": "deny-precedence-kat",
            "objective": "preserve hard policy denial",
            "risk": "medium",
            "execution": {
                "type": "general",
                "provider_preference": "deterministic",
            },
            "requirements": {"gcp": True},
            "requested_actions": [
                {"system": "gcp", "action": "iam_change"}
            ],
        }
    )
    decision = plan(task, QuotaSnapshot(100, 100))
    assert decision.decision == DecisionStatus.deny
    assert decision.sandbox == "read-only"
    assert decision.max_agents == 0
