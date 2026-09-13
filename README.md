# FoundLab AI Ops

**Executable governance and operational control plane for human + agent workflows.**

FoundLab AI Ops is a public, versioned baseline for operating AI-assisted engineering with explicit policy, capability, memory, execution, and evidence boundaries.

It is not a prompt dump and it is not an autonomous agent framework. The core is intentionally deterministic.

## Operating model

```text
Task
  |
  v
Memory / Context ---- Skill Registry
        \              /
         v            v
          Policy Engine
               |
               v
       Capability Resolver
               |
               v
      Plugin / Tool Registry
               |
               v
        Execution Adapter
               |
               v
        Evidence + Journal
```

The system follows one governing rule:

> AI proposes. Policy decides. Executors act. Evidence proves.

## What belongs here

- model and reasoning routing policy;
- quota and reserve policy;
- permission and mutation gates;
- source-of-truth rules;
- reusable Skills;
- plugin/capability registry;
- institutional Memory Bank schemas and indexes;
- Codex operating profiles;
- GCP keyless-access patterns;
- task, decision, evidence and capability contracts;
- deterministic CLI checks and planning;
- runbooks and Known Answer Tests.

## What must never be committed

- API keys, OAuth tokens or credentials;
- Google Cloud service-account private keys;
- customer identifiers or private commercial pipeline data;
- production secrets, internal IPs or sensitive resource identifiers;
- exports of personal ChatGPT memory;
- environment files containing secrets.

Use placeholders and local/private configuration for environment-specific values.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"

flops doctor
flops plugins
flops skills
flops quota status
flops plan examples/tasks/repo-audit.yaml
```

## Repository map

```text
src/foundlab_ai_ops/   deterministic Python control plane
policies/              policy-as-code
profiles/              execution profiles
skills/                workflow-as-code
plugins/               capability registry
memory-bank/           institutional memory-as-code
contracts/             JSON Schemas
codex/                 Codex configuration examples
gcp/                   keyless Google Cloud access guidance
runbooks/              operational procedures
examples/              non-sensitive examples
tests/                 policy and engine KATs
```

## Authority model

This repository can be authoritative for durable AI operating policy. It must not be used as a cache of rapidly changing external state.

Examples:

| Question | Authority |
| --- | --- |
| Which AI operating policy is current? | this repository |
| Which PR is open? | GitHub |
| Which backlog item is current? | Linear |
| Which document is approved? | Google Drive / designated document system |
| Which Cloud Run revision is serving? | Google Cloud |
| What personal response style is preferred? | ChatGPT personalization / memory |

Memory is context. It is never allowed to silently override current authoritative evidence.

## Status

**v0.1.0 — Operational Baseline**

The initial release establishes deterministic task planning, policy evaluation, quota state, plugin/skill registries, memory-bank metadata, security defaults, and CI validation.

## License

Apache-2.0. See `LICENSE`.
