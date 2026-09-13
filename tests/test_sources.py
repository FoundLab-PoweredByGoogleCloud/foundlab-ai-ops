from foundlab_ai_ops.sources import authority_for


def test_authority_resolution():
    assert authority_for("pull_request_state") == "github"
    assert authority_for("cloud_runtime") == "gcp"
    assert authority_for("personal_preferences") == "chatgpt_memory"
