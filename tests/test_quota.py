from foundlab_ai_ops.quota import QuotaSnapshot, mode


POLICY = {
    "thresholds": {
        "amber_below": 60,
        "red_below": 30,
        "critical_below": 10,
    }
}


def test_quota_modes():
    assert mode(QuotaSnapshot(100, 100), POLICY) == "GREEN"
    assert mode(QuotaSnapshot(100, 59), POLICY) == "AMBER"
    assert mode(QuotaSnapshot(100, 29), POLICY) == "RED"
    assert mode(QuotaSnapshot(100, 9), POLICY) == "CRITICAL"
