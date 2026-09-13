# Security Policy

## Baseline

FoundLab AI Ops is public. Treat every committed byte as permanently public.

Never commit:
- API keys, bearer tokens, OAuth credentials or session cookies;
- Google Cloud service-account private keys;
- private SSH keys or signing keys;
- customer identifiers or confidential commercial data;
- production environment files;
- exports of personal ChatGPT memory;
- internal-only infrastructure details that create unnecessary attack surface.

## Cloud authentication

Preferred patterns:
- Application Default Credentials for local development;
- user authentication plus service-account impersonation for privileged local operations;
- attached user-managed service accounts for Google Cloud runtimes;
- Workload Identity Federation for external CI/CD.

Persistent service-account JSON keys are not part of the supported baseline.

## Agent permissions

Use defense in depth:
1. FoundLab policy;
2. agent/tool permission layer;
3. provider IAM.

Read access may be automatic where appropriate. Writes require a review gate. Destructive operations require explicit authorization and should be denied by default.

## Reporting

Do not open a public issue containing a vulnerability, secret, credential, or sensitive exploit detail. Use the repository owner's private security reporting channel when available.
