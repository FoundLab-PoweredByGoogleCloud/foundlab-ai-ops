# Architecture

Version: 0.2.0

FoundLab AI Ops is an authority, routing and evidence layer above provider-native execution surfaces.

## 1. Policy plane

Deterministic rules for:
- provider routing;
- compute class;
- execution mode;
- quota/reserve;
- permissions;
- mutation boundaries;
- source authority.

The policy plane must not require an LLM to decide whether an LLM/tool is allowed to run.

## 2. Provider plane

### Deterministic
Python, scripts, CI and validators for work that does not require probabilistic reasoning.

### OpenAI
Chat, Work, Codex, Responses API, Skills API and Agents SDK.

### Google
Gemini/Google coding surfaces, Gemini API, Google Managed MCP, Developer Knowledge, Agent Registry and Google Cloud observability.

Provider-specific model IDs are resolved at deployment/runtime. Institutional policy uses provider-neutral compute classes.

## 3. Capability plane

Capabilities can come from:
- native tools;
- connected apps/plugins;
- provider APIs;
- managed remote MCP;
- FoundLab custom MCP.

Selection rule:

```text
provider-native typed capability
        ↓
managed service MCP
        ↓
controlled generic escape hatch
        ↓
custom implementation
```

Custom implementation is justified only where FoundLab domain semantics are missing.

## 4. Workflow plane

Skills are versioned workflows. A Skill defines **how**, not **whether**.

A single repository Skill can have multiple deployment targets:
- local/Codex;
- OpenAI Skills API;
- Google/CLI skill/plugin formats;
- future provider runtimes.

## 5. Knowledge plane

Three distinct memory classes:

1. personal memory — preferences/continuity;
2. operational memory — short-lived execution state;
3. institutional memory — Git-versioned invariants, decisions, terminology and authority pointers.

Current external state remains at its authoritative provider.

## 6. Enforcement plane

FoundLab policy should be enforced as close to side effects as possible.

Examples:
- Gemini CLI `BeforeTool` hook;
- OpenAI Agents SDK blocking/task/tool guardrails;
- ChatGPT/plugin permission controls;
- Google Cloud IAM and MCP IAM deny conditions;
- repository/branch protection.

No single enforcement layer is assumed sufficient.

## 7. Evidence plane

Evidence should converge without forcing all providers into one runtime.

```text
FoundLab journal
OpenAI tracing/provider usage
Gemini CLI OpenTelemetry
Google Cloud logs/metrics/traces
Git/GitHub/CI evidence
        ↓
normalized evidence records
```

## Separation rule

- **Policy:** what is allowed.
- **Router:** where/how work should execute.
- **Skill:** how to perform it.
- **Capability:** what external operation is available.
- **Memory:** what durable context is known.
- **Executor:** performs the operation.
- **Evidence:** proves what happened.
