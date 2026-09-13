from foundlab_ai_ops.compiler import codex_baseline, gemini_baseline


def test_codex_baseline_enables_secret_name_exclusions():
    text = codex_baseline()
    assert "ignore_default_excludes = false" in text
    assert 'approval_policy = "on-request"' in text


def test_gemini_baseline_enables_redaction_and_disables_prompt_logging():
    config = gemini_baseline()
    assert config["security"]["environmentVariableRedaction"]["enabled"] is True
    assert config["telemetry"]["logPrompts"] is False
    assert config["hooks"]["BeforeTool"]
