# Runbook — Google Execution Plane

Last checked against official Google documentation: 2026-09-12.

## 1. Determine the valid coding surface

Do not assume Gemini CLI is the correct entitlement for every account.

Current Google documentation states:
- Gemini Code Assist Standard/Enterprise continue to support Gemini CLI;
- individual / Google AI Pro / Ultra coding users affected by the 2026-06-18 change should use Antigravity / Antigravity CLI.

Record the selected runtime surface before installing project configuration.

## 2. Authenticate without persistent service-account keys

For Google Cloud inspection, prefer user ADC and narrowly scoped service-account impersonation where appropriate.

## 3. Enable Developer Knowledge

Use the Google Developer Knowledge MCP for current official Google developer documentation.

Official endpoint:

```text
https://developerknowledge.googleapis.com/mcp
```

Prefer ADC for Google Cloud environments. Do not commit API keys into Gemini settings.

## 4. Install generated Gemini CLI baseline only after review

```bash
flops compile gemini --output PATH_TO_CANDIDATE_SETTINGS
flops google doctor --settings PATH_TO_CANDIDATE_SETTINGS
```

The candidate:
- uses normal approval mode;
- sets `security.disableYoloMode=true`;
- enables environment-variable redaction;
- enables GCP telemetry with prompt logging disabled;
- installs a BeforeTool policy hook.

Treat a missing/false `disableYoloMode` as a security warning even when the default approval mode is not YOLO.

## 5. Prefer managed MCP

Start read-heavy:
- Developer Knowledge;
- Cloud Run;
- Logging;
- Monitoring;
- Trace;
- BigQuery/Spanner only where required.

Keep Cloud CLI MCP as an escape hatch because it can execute mutating gcloud/bq commands.

## 6. Enforce read-only at Google IAM when required

Google Cloud MCP supports an IAM deny condition based on the MCP tool `isReadOnly` attribute for supported servers. See `gcp/mcp-readonly-deny-policy.json.example`.

This is stronger than relying only on prompt instructions.

## 7. Telemetry

Gemini CLI supports OpenTelemetry export to Cloud Logging, Monitoring and Trace and emits request, token, tool, model-routing and agent-run telemetry.

FoundLab baseline:
- telemetry enabled;
- GCP target;
- CLI auth for local telemetry where appropriate;
- `logPrompts=false` unless explicitly approved.

## Official references

- https://docs.cloud.google.com/gemini/docs/codeassist/gemini-cli
- https://docs.cloud.google.com/gemini/docs/quotas
- https://docs.cloud.google.com/mcp/supported-products
- https://docs.cloud.google.com/mcp/prevent-read-write-tool-use
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/connect-to-the-knowledge-mcp-server
- https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/reference.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/telemetry.md
