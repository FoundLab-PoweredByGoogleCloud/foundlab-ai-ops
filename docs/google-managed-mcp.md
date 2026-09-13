# Google Managed MCP

Last checked against official Google Cloud documentation: 2026-09-12.

Google Cloud provides managed remote MCP servers for many products. FoundLab therefore does not build a generic GCP wrapper when an official service-specific MCP exists.

Desired-state endpoints are tracked in `mcp/google-managed.yaml`.

## Selection rule

```text
service-specific managed MCP
        ↓
Cloud CLI MCP (escape hatch)
        ↓
custom FoundLab MCP only for FoundLab domain semantics
```

## Security

Managed MCP does not remove governance:
- OAuth scopes still apply;
- IAM still applies;
- server toolsets should be minimized;
- FoundLab permission policy remains an independent gate;
- write-capable tools require review or explicit authorization.

The Cloud Run MCP, for example, exposes both read and deploy tools. Therefore merely connecting the server is not equivalent to authorizing deployment.

## FoundLab custom MCP

The remaining custom MCP scope is domain-specific:
- authority/release plan;
- evidence bundle composition;
- REX/Authority Core invariant verification;
- policy receipts;
- cross-provider decision/evidence correlation.

It is explicitly not a generic `gcloud(anything)` proxy.
