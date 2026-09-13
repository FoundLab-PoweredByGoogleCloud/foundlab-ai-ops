# FoundLab AI Ops

**Multi-provider governance and operational control plane for human + agent workflows.**

FoundLab AI Ops is a public, versioned baseline for operating AI-assisted engineering across OpenAI, Google and deterministic local tooling with explicit policy, capability, memory, execution and evidence boundaries.

It is not a prompt dump and it is not an autonomous agent framework. The core remains intentionally deterministic.

## Operating model

```text
                        TASK
                         |
                         v
                 FoundLab AI Ops
                  Policy Engine
                         |
       +-----------------+------------------+
       |                 |                  |
       v                 v                  v
  Deterministic       OpenAI             Google
  Python/scripts   Chat/Work/Codex   Gemini/Antigravity
                  Responses/Agents      Gemini API
       |                 |                  |
       +-----------------+------------------+
                         |
                         v
                 Capability Plane
        Plugins / Skills / Managed MCP / APIs
                         |
                         v
                  Evidence Plane
          journal / traces / OTEL / provider logs
```

The governing rule is:

> AI proposes. Policy decides. Executors act. Evidence proves.

## v0.2 decision contract

The router now decides:

- **provider** — deterministic, OpenAI, Google;
- **surface** — Codex, OpenAI API, Google coding surface, Gemini API, etc.;
- **execution mode** — interactive, standard, background, flex, batch;
- **compute class** — economy, balanced, professional, frontier;
- **capabilities** — plugin/API/MCP requirements;
- **approval boundary** — allow, review, explicit, deny;
- **telemetry requirement**.

Provider-specific model IDs are runtime mappings, not institutional policy.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"

flops doctor

flops codex doctor
flops google doctor
flops gcp doctor

flops providers
flops plugins
flops skills
flops mcp list
flops source

flops authorize github write
flops authorize gcp deploy

flops quota set --five-hour 100 --weekly 100
flops quota status

flops plan examples/tasks/repo-audit.yaml
flops plan examples/tasks/gcp-runtime-audit.yaml
```

Generate reviewed configuration candidates without overwriting existing files:

```bash
flops compile codex --output ./candidate-codex.toml
flops compile gemini --output ./candidate-gemini-settings.json
```

## Repository map

```text
src/foundlab_ai_ops/   deterministic control plane
policies/              policy-as-code
providers/             provider capability metadata
profiles/              execution profiles
agents/                bounded execution profiles
skills/                workflow-as-code
plugins/               connected-app capability registry
mcp/                   managed/custom MCP desired state
memory-bank/           institutional memory-as-code (compatibility path)
contracts/             JSON Schemas
codex/                 Codex examples
google/                Gemini/Google examples
gcp/                   Google Cloud IAM/auth patterns
docs/                  architecture and provider manuals
runbooks/              operational procedures
examples/              non-sensitive task manifests
tests/                 Known Answer Tests
```

## Capability strategy

Do not rebuild provider capabilities unnecessarily.

For Google Cloud:

```text
service-specific Google Managed MCP
                ↓
Cloud CLI MCP as controlled escape hatch
                ↓
custom FoundLab MCP only for FoundLab domain semantics
```

For OpenAI:

```text
Git Skill/policy source
        ↓
FoundLab validation
        ↓
OpenAI Skill / Agents / Responses deployment target
        ↓
provider tracing + FoundLab evidence
```

## Memory model

The concept previously called Memory Bank is now explicitly **Institutional Memory**.

Three domains remain separate:

- personal memory — ChatGPT/product continuity and preferences;
- operational memory — short-lived local/runtime state;
- institutional memory — versioned decisions, invariants, terminology and authority pointers in Git.

The existing `memory-bank/` path is retained in v0.2 for compatibility.

## Authority model

| Question | Authority |
| --- | --- |
| AI operating policy | this repository |
| Repository state | Git |
| PR state | GitHub |
| Backlog | Linear |
| Approved document | designated document system |
| Cloud runtime/logs/metrics/traces | Google Cloud |
| Current Google developer docs | Developer Knowledge MCP |
| Runtime agent discovery | Google Agent Registry when deployed |
| Personal preferences | product memory/personalization |

Memory cannot silently override current authoritative evidence.

## Security posture

- read can be automatic where explicitly classified read-only;
- remote writes require review;
- destructive operations are denied or explicitly authorized;
- Codex secret-name exclusions are expected to be enabled;
- Gemini CLI environment-variable redaction is expected to be enabled;
- provider approval modes are not replaced by FoundLab policy;
- Google Cloud IAM remains authoritative for cloud access;
- Google Managed MCP can additionally be constrained using MCP IAM attributes;
- persistent GCP service-account private keys are outside the supported baseline;
- prompt bodies are not included in Gemini telemetry by default in the generated FoundLab baseline.

See [SECURITY.md](SECURITY.md).

## Manuals

- [Architecture](docs/architecture.md)
- [Multi-provider routing](docs/multi-provider-routing.md)
- [OpenAI operations](docs/openai-operations.md)
- [OpenAI developer plane](docs/openai-developer-plane.md)
- [Google execution plane](google/README.md)
- [Google Managed MCP](docs/google-managed-mcp.md)
- [Codex governance](docs/codex-governance.md)
- [Plugins, Skills and MCP](docs/plugins-skills-mcp.md)
- [Memory and context](docs/memory-and-context.md)
- [Prompt/task contracts](docs/prompt-contracts.md)

Provider-specific manuals record the date official documentation was last checked. Provider behavior is not assumed immutable.

## Status

**v0.2.1 — Codex Review Remediation**

Implemented in this release:
- multi-provider task routing;
- provider-neutral compute classes;
- execution-mode routing;
- Google Managed MCP desired-state registry;
- Gemini CLI diagnostics and config compiler;
- Gemini BeforeTool FoundLab policy hook;
- OpenAI/Google provider registry;
- Google/ChatGPT quota-domain separation in decisions;
- managed-MCP task requirements;
- GCP MCP read-only deny-policy example;
- expanded schemas and KATs;\n- post-v0.2 Codex review findings remediated with regression tests and explicit Gemini YOLO disable.

## License

Apache-2.0. See `LICENSE` and `NOTICE`.
