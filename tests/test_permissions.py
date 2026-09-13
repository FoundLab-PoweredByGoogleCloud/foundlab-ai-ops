from foundlab_ai_ops.permissions import evaluate


def test_default_and_system_permissions():
    assert evaluate("github", "read") == "allow"
    assert evaluate("github", "write") == "review"
    assert evaluate("gcp", "iam_change") == "deny"
    assert evaluate("gcp", "destructive") == "explicit"


def test_unknown_action_defaults_to_review():
    assert evaluate("unknown-system", "custom-action") == "review"
