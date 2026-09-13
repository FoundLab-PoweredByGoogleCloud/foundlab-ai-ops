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

The governing rule is:

> AI proposes. Policy decides. Executors act. Evidence proves.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"

flops doctor
flops codex doctor
flops gcp doctor

flops plugins
flops skills
flops source
flops authorize github write

flops quota set --five-hour 100 --weekly 100
flops quota status

flops recall "memory"
flops plan examples/tasks/repo-audit.yaml
```

## What belongs here

- model and reasoning routing policy;
- quota and reserve policy;
- permission and mutation gates;
- source-of-truth rules;
- reusable Skills;
- plugin/capability registry;
- institutional Memory Bank schemas and indexes;
- Codex operating profiles and diagnostics;
- GCP keyless-access patterns and diagnostics;
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

## Repository map

```text
src/foundlab_ai_ops/   deterministic Python control plane
policies/              policy-as-code
profiles/              execution profiles
agents/                bounded execution profiles
skills/                workflow-as-code
plugins/               capability registry
memory-bank/           institutional memory-as-code
contracts/             JSON Schemas
codex/                 Codex configuration examples
gcp/                   keyless Google Cloud access guidance
mcp/                   typed MCP capability specifications
docs/                  operating manuals and architecture
runbooks/              operational procedures
examples/              non-sensitive examples
tests/                 policy and engine KATs
```

## Core contracts

- **Skill** — how to perform a class of work.
- **Policy** — what is allowed.
- **Plugin/capability** — what external system or action is available.
- **Memory** — durable context and authority pointers.
- **Engine** — what execution decision follows from task + policy + quota.
- **Evidence** — what proves what happened.

## Authority model

This repository can be authoritative for durable AI operating policy. It must not be used as a cache of rapidly changing external state.

| Question | Authority |
| --- | --- |
| Which AI operating policy is current? | this repository |
| Which PR is open? | GitHub |
| Which backlog item is current? | Linear |
| Which document is approved? | Google Drive / designated document system |
| Which Cloud Run revision is serving? | Google Cloud |
| What personal response style is preferred? | ChatGPT personalization / memory |

Memory is context. It is never allowed to silently override current authoritative evidence.

## Manuals

- [Architecture](docs/architecture.md)
- [OpenAI operations](docs/openai-operations.md)
- [Model routing](docs/model-routing.md)
- [Codex governance](docs/codex-governance.md)
- [Plugins, Skills and MCP](docs/plugins-skills-mcp.md)
- [Memory and context](docs/memory-and-context.md)
- [Prompt/task contracts](docs/prompt-contracts.md)
- [Google Cloud access](gcp/README.md)
- [Planned GCP MCP](mcp/foundlab-gcp-mcp/SPEC.md)

The OpenAI-specific manuals record the date on which official provider documentation was last checked. Provider behavior is not assumed to be immutable.

## Security posture

The baseline is deliberately conservative:

- read can be automatic;
- writes require review;
- destructive operations are denied or require explicit authorization;
- Codex shell secret-name exclusions are expected to be enabled;
- `danger-full-access` is not a normal operating mode;
- GCP persistent service-account keys are outside the supported baseline;
- external live state must be queried from its authority rather than trusted from memory.

See [SECURITY.md](SECURITY.md).

## Status

**v0.1.0 — Operational Baseline**

The initial release establishes deterministic task planning, model/quota routing, capability-policy evaluation, authority resolution, local audit journaling, plugin/skill registries, memory-bank metadata, Codex/GCP diagnostics, security defaults, schemas, CI validation, and initial Known Answer Tests.

## License

Apache-2.0. See `LICENSE` and `NOTICE`.
