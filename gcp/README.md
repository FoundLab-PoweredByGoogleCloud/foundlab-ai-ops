# Google Cloud Access and Capability Baseline

## Identity

The supported baseline is keyless wherever practical.

### Local
Prefer:
1. human Google authentication;
2. Application Default Credentials when required;
3. narrowly scoped service-account impersonation for privileged operations.

### Google Cloud runtime
Attach a user-managed service account with least privilege.

### External CI
Prefer Workload Identity Federation / OIDC.

Persistent service-account private keys are outside the supported baseline.

## Managed MCP

Before building a custom adapter, inspect `mcp/google-managed.yaml`.

Prefer:
1. service-specific Google Managed MCP;
2. Cloud CLI MCP only as an explicit escape hatch;
3. custom FoundLab MCP only for domain semantics.

This avoids duplicating provider CRUD APIs and allows Google IAM to remain an enforcement layer.

## Read-only MCP enforcement

Where supported, Google Cloud MCP IAM can deny calls to tools not annotated read-only.

Example policy:
`mcp-readonly-deny-policy.json.example`

Applying IAM policy is itself a privileged operation and is **not** performed automatically by this repository.

## Observability

Gemini CLI can export OpenTelemetry directly to Cloud Logging, Monitoring and Trace. This should feed the FoundLab evidence plane rather than being reimplemented as proprietary telemetry.

See:
- `google/README.md`
- `runbooks/google-execution-plane.md`
- `docs/google-managed-mcp.md`
