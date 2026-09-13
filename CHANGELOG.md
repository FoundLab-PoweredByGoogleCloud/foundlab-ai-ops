# Changelog

## 0.2.1 — Codex Review Remediation

- prevent managed-MCP tasks from being routed to deterministic/local-only execution;
- block explicit deterministic-provider overrides when remote capabilities are required;
- validate explicit surface overrides against the selected provider registry;
- preserve hard permission DENY precedence over provider-compatibility BLOCKED;
- require the MCP registry check for implicit Developer Knowledge dependencies;
- hard-disable Gemini CLI YOLO mode in the generated baseline;
- make `flops google doctor` warn when YOLO is not explicitly disabled;
- defensively warn if a settings file presents YOLO as the approval mode;
- add regression KATs for every Codex review finding;
- require asynchronous agent review completion before merging policy/control-plane changes.

## 0.2.0 — Multi-Provider Control Plane

- replaced OpenAI-specific logical model routing with provider-neutral compute classes;
- added deterministic/OpenAI/Google provider routing;
- added interactive/standard/background/flex/batch execution modes;
- added provider and managed-MCP registries;
- added Google Developer Knowledge and Google Cloud managed MCP integration model;
- added Gemini CLI security/telemetry diagnostics;
- added Codex and Gemini configuration compilers;
- added Gemini CLI BeforeTool FoundLab policy hook;
- separated ChatGPT Work/Codex quota state from Google/API usage domains;
- documented OpenAI Skills API, Agents SDK guardrails/tracing and remote MCP as deployment targets;
- narrowed custom FoundLab GCP MCP scope to FoundLab domain semantics;
- added Google MCP IAM read-only deny-policy example;
- expanded JSON Schemas and Known Answer Tests for multi-provider decisions.

## 0.1.0 — Operational Baseline

- deterministic Python policy engine and CLI;
- logical model/reasoning routing;
- quota reserve policy and local snapshots;
- permission and mutation governance;
- source-of-truth resolver;
- plugin/capability registry;
- reusable Skills;
- institutional Memory Bank;
- Codex and GCP diagnostics;
- GCP MCP capability specification;
- JSON Schema contracts;
- security baseline, runbooks and CI validation;
- Known Answer Tests for routing, quota, permissions and authority.
