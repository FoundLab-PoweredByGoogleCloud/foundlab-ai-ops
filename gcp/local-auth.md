# Local GCP Authentication

Example only. Replace placeholders locally; never commit real identifiers if they are sensitive.

```bash
gcloud auth login

gcloud config configurations create foundlab-ai-ops

gcloud config set project PROJECT_ID

gcloud config set auth/impersonate_service_account \
  AI_OPS_READ_SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com
```

For ADC-based client libraries:

```bash
gcloud auth application-default login \
  --impersonate-service-account=AI_OPS_READ_SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com
```

## Separation of authority

Use distinct service accounts for read-only inspection and deployment. Do not grant broad Editor/Owner roles merely to simplify agent access.

A proposed deployment should be separated into:
- plan/dry-run;
- review;
- apply using a separately authorized identity.
