import json

from foundlab_ai_ops.adapters.gemini import diagnose


def _write_settings(tmp_path, payload):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_doctor_warns_when_yolo_not_explicitly_disabled(tmp_path, monkeypatch):
    monkeypatch.setattr("foundlab_ai_ops.adapters.gemini.shutil.which", lambda _: None)
    path = _write_settings(
        tmp_path,
        {
            "general": {"defaultApprovalMode": "default"},
            "security": {
                "environmentVariableRedaction": {"enabled": True}
            },
            "telemetry": {"enabled": False},
        },
    )

    result = diagnose(path)
    assert result.yolo_disabled is None
    assert any("disableYoloMode" in warning for warning in result.warnings)


def test_doctor_warns_defensively_on_yolo_approval_mode(tmp_path, monkeypatch):
    monkeypatch.setattr("foundlab_ai_ops.adapters.gemini.shutil.which", lambda _: None)
    path = _write_settings(
        tmp_path,
        {
            "general": {"defaultApprovalMode": "yolo"},
            "security": {
                "disableYoloMode": True,
                "environmentVariableRedaction": {"enabled": True},
            },
            "telemetry": {"enabled": False},
        },
    )

    result = diagnose(path)
    assert result.yolo_disabled is True
    assert any("yolo" in warning.casefold() for warning in result.warnings)


def test_doctor_accepts_safe_yolo_posture(tmp_path, monkeypatch):
    monkeypatch.setattr("foundlab_ai_ops.adapters.gemini.shutil.which", lambda _: None)
    path = _write_settings(
        tmp_path,
        {
            "general": {"defaultApprovalMode": "default"},
            "security": {
                "disableYoloMode": True,
                "environmentVariableRedaction": {"enabled": True},
            },
            "telemetry": {"enabled": True, "logPrompts": False},
        },
    )

    result = diagnose(path)
    assert result.yolo_disabled is True
    assert not any("disableYoloMode" in warning for warning in result.warnings)
    assert not any("approval" in warning.casefold() for warning in result.warnings)
