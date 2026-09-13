# Google Execution Plane

FoundLab AI Ops treats Google as a first-class execution and capability provider.

## Coding surfaces

At runtime, determine which Google coding surface is valid for the user's current entitlement:
- Gemini CLI remains documented for Gemini Code Assist Standard/Enterprise;
- affected individual/Google AI Pro/Ultra users were moved to Antigravity/Antigravity CLI from 2026-06-18.

Do not hard-code one Google coding surface globally.

## Gemini CLI baseline

The generated/example settings intentionally:
- use default approval mode rather than auto-edit/yolo;
- enable environment-variable redaction;
- enable OpenTelemetry export to GCP;
- disable prompt-body telemetry by default;
- install a BeforeTool hook that delegates mutation decisions to `flops`.

Install only after review:

```bash
flops compile gemini --output ~/.gemini/settings.json
flops google doctor
```

## Observability

Gemini CLI can export OpenTelemetry logs, metrics and traces to Google Cloud. The official telemetry includes API request count/latency, token usage, tool calls, model routing and agent-run metrics.

FoundLab's default is to keep `telemetry.logPrompts=false` unless an explicit data policy permits prompt logging.

## Managed MCP

Use `mcp/google-managed.yaml` as the desired-state catalog. Prefer service-specific MCP servers over Cloud CLI MCP, and prefer managed MCP over a custom provider wrapper.

## Official Google developer skills

Use Google-maintained developer/cloud skills where available. FoundLab Skills should focus on domain workflow and policy rather than duplicating generic Google documentation.
