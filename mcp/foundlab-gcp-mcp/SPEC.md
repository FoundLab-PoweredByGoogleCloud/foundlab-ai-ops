# FoundLab Domain MCP — Scope Specification

Status: **domain-specific only; generic GCP wrapper rejected in v0.2**.

## Decision

Google Cloud now provides managed remote MCP servers for Cloud Run, BigQuery, Spanner, Logging, Monitoring, Trace, Pub/Sub, IAM, Resource Manager, Cloud Quotas, Cloud CLI and many other products.

Therefore FoundLab AI Ops MUST NOT implement a generic provider wrapper for capabilities already available through a suitable Google Managed MCP.

See:
- `mcp/google-managed.yaml`
- `docs/google-managed-mcp.md`

## Remaining FoundLab MCP scope

A future custom MCP is justified for **FoundLab semantics**, for example:

- `authority_release_plan`
- `authority_release_verify`
- `rex_runtime_evidence_bundle`
- `decision_journal_verify`
- `institutional_policy_check`
- `change_set_authorize`
- cross-provider evidence correlation.

These are not ordinary Google Cloud CRUD operations.

## Gate ordering

```text
typed FoundLab request
        |
        v
FoundLab policy
        |
        v
human review when required
        |
        v
provider-native capability / managed MCP
        |
        v
provider IAM
        |
        v
operation
        |
        v
normalized evidence
```

## Non-goals

- arbitrary `gcloud <string>` proxy;
- replacement for Google Managed MCP;
- storage of persistent provider credentials;
- bypass of IAM or provider approval controls;
- silent deployment or IAM mutation.
