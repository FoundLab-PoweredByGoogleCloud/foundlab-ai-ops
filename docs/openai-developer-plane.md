# OpenAI Developer Plane

Last checked against official OpenAI developer documentation: 2026-09-12.

FoundLab AI Ops treats Chat/Work/Codex as only one part of the OpenAI execution plane.

## Skills API

OpenAI exposes project-scoped Skills with create/list/get/delete operations and immutable Skill Versions. The repository remains the desired source; deployment tooling can publish versioned Skill bundles without making the hosted copy the only authority.

## Agents SDK

The Agents SDK supports guardrails, MCP integration and tracing. Blocking input guardrails can complete before expensive agent execution begins, which makes them suitable for quota/cost and authorization preflight.

## Responses / hosted capabilities

Responses supports tool choice including remote MCP tools and skill references in current API surfaces. Hosted agent/environment resources should be treated as deployment targets, not replacements for versioned policy in Git.

## FoundLab rule

```text
repo policy / skill source
       ↓
flops validation
       ↓
provider deployment target
       ↓
provider tracing / evidence
```

Provider-hosted configuration is runtime state; Git remains the durable desired-state authority.
