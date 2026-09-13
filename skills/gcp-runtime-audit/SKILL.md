# Skill — GCP Runtime Audit

## Purpose
Inspect Google Cloud runtime state without treating cached memory as live truth.

## Preferred authority
Google Cloud APIs/CLI authenticated with short-lived credentials and least privilege.

## Workflow
1. Confirm project/account/configuration.
2. Confirm effective identity and whether impersonation is active.
3. Inspect target resource metadata.
4. Inspect relevant revisions, logs and metrics.
5. Distinguish configured state from observed runtime behavior.
6. Do not change IAM, deploy, delete or mutate resources under an audit task.

## Security
Persistent service-account keys are outside the supported baseline.
