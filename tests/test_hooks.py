from foundlab_ai_ops.hooks import gemini_before_tool


def test_workspace_edit_is_allowed_by_local_policy():
    result = gemini_before_tool(
        {"tool_name": "write_file", "tool_input": {"path": "README.md"}}
    )
    assert result["decision"] == "allow"


def test_shell_deploy_is_blocked_without_explicit_path():
    result = gemini_before_tool(
        {
            "tool_name": "run_shell_command",
            "tool_input": {"command": "gcloud run deploy service --image image"},
        }
    )
    assert result["decision"] == "deny"


def test_generic_mcp_write_is_blocked_pending_review():
    result = gemini_before_tool(
        {"tool_name": "mcp_cloud_run_deploy_service", "tool_input": {}}
    )
    assert result["decision"] == "deny"
