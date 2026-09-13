# FoundLab GCP MCP — Capability Specification

Status: **planned / not implemented in v0.1**.

## Objective

Expose narrow, typed Google Cloud capabilities to agents without granting arbitrary shell execution or bypassing IAM.

## Identity

Preferred:
- local: authenticated human + short-lived service-account impersonation;
- Cloud Run: attached user-managed service account;
- external CI: Workload Identity Federation.

No persistent service-account private key is required by this design.

## Read tools

- `gcp_project_get`
- `cloudrun_service_get`
- `cloudrun_revisions_list`
- `cloudrun_logs_query`
- `monitoring_metrics_query`
- `iam_policy_explain`

## Mutation tools

Mutations must be split into plan/apply.

- `deploy_plan` — produce a dry-run/change set and hash;
- `deploy_apply` — accept an authorized change-set hash;
- `rollback_plan`;
- `rollback_apply`.

IAM mutation is outside the default capability set.

## Required gate ordering

```text
MCP request
   |
   v
typed input validation
   |
   v
FoundLab policy evaluation
   |
   v
provider IAM
   |
   v
operation
   |
   v
evidence / audit record
```

## Non-goal

Do not expose `gcloud <arbitrary string>` as an MCP tool.
