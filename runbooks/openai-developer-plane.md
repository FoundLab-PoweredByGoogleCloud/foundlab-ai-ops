# Runbook — OpenAI Developer Plane

Last checked against official OpenAI developer documentation: 2026-09-12.

## Desired-state rule

Keep Skills and governance policy versioned in Git. Hosted OpenAI resources are deployment/runtime state.

## Skills

OpenAI exposes project-scoped Skills and immutable Skill Versions. Publish only after:
1. repository validation;
2. review of skill contents;
3. secret scan;
4. explicit target project selection.

Do not put an OpenAI API key in this repository or a Skill bundle.

## Agents SDK

Use blocking input guardrails when a policy must run before an expensive model or side-effecting tool can begin. Parallel guardrails optimize latency but can already consume tokens before a tripwire fires.

Map FoundLab decisions to:
- input guardrails for task admission;
- tool guardrails for FoundLab-owned function tools/local MCP;
- human-in-the-loop approval for writes;
- tracing for evidence.

## Remote MCP

Remote MCP is a capability transport, not an authority bypass. Apply:
- minimal tool exposure;
- FoundLab permission policy;
- provider authentication/IAM;
- explicit approvals for writes.

## Official references

- https://developers.openai.com/api/reference/go/resources/skills
- https://openai.github.io/openai-agents-python/guardrails/
- https://openai.github.io/openai-agents-python/mcp/
- https://openai.github.io/openai-agents-python/tracing/
