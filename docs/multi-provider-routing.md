# Multi-Provider Routing

Version: 0.2.0

The v0.2 router selects four dimensions independently:

1. **provider** — deterministic, OpenAI, or Google;
2. **surface** — Codex, OpenAI API, Google coding surface, Gemini API, etc.;
3. **execution mode** — interactive, standard, background, flex, or batch;
4. **compute class** — economy, balanced, professional, or frontier.

Provider-specific model names remain deployment/runtime configuration rather than institutional policy.

## Why

Routing only by model conflates:
- reasoning difficulty;
- provider authority;
- latency requirements;
- cost mode;
- tool availability;
- quota domain.

A Cloud Run inspection task should prefer Google authority/capabilities even if another provider has a stronger general model. A bulk evaluation should prefer batch/flex execution rather than consuming an interactive agent quota.

## Examples

### Repository engineering
OpenAI default:
- provider: openai
- surface: codex
- execution_mode: standard

### GCP runtime audit
- provider: google
- surface: google_coding or gemini_api
- managed MCP: Cloud Run + Logging + Monitoring as required

### Bulk evaluation
- execution_mode: batch
- use provider batch API where supported

### Pure mechanical work
- provider: deterministic
- surface: local_python

## Quota isolation

The ChatGPT Work/Codex allowance, OpenAI API billing, Gemini Code Assist/Gemini CLI quota, and Gemini API billing are distinct operational domains. A single global percentage must not be presented as live truth for all providers.
