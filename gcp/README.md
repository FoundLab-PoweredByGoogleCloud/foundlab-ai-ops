# Google Cloud Access Baseline

The supported baseline is keyless wherever practical.

## Local workstation

Preferred:
1. authenticate the human identity;
2. use Application Default Credentials when application libraries require them;
3. impersonate a narrowly scoped user-managed service account for privileged operations.

Do not place service-account private key JSON files in this repository or in agent prompts.

## Google Cloud runtime

Attach a user-managed service account with least privilege to the workload. Use the runtime's native identity/ADC path.

## External CI/CD

Prefer Workload Identity Federation / OIDC over persistent service-account keys.

See `local-auth.md` for a placeholder-based setup pattern.
