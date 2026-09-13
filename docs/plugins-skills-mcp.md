# Plugins, Skills and MCP

Version: 0.2.0

## Plugins / connected apps

Connected apps expose account-scoped capabilities. Connection state is runtime state; Git stores policy and capability metadata, not OAuth secrets.

Installing an app never grants FoundLab institutional authority by itself.

## Skills

Skills are workflow source.

FoundLab stores portable Skills in Git and treats provider-native skill systems as deployment targets.

Current targets include:
- Codex/local skill consumption;
- OpenAI Skills API with immutable Skill Versions;
- Google-maintained developer/cloud skills where available.

FoundLab should not duplicate generic provider documentation as custom Skills when the provider maintains an authoritative skill/knowledge source.

## MCP

MCP is capability transport.

For Google Cloud, prefer official managed MCP servers. For OpenAI agents, remote/local MCP can expose those capabilities subject to authentication and approvals.

### Selection order

```text
service-specific managed MCP
        ↓
provider generic MCP / CLI escape hatch
        ↓
FoundLab custom MCP for FoundLab-only semantics
```

## Defense in depth

A tool call may need to pass all applicable layers:

1. FoundLab deterministic policy;
2. executor approval mode/hook/guardrail;
3. connected app or MCP authentication;
4. provider IAM;
5. cloud/repository protections;
6. evidence recording.

## Tool minimization

Do not expose every available MCP tool to every agent. Restrict servers/toolsets to what the task requires.

## Sources

OpenAI:
- https://developers.openai.com/api/reference/go/resources/skills
- https://openai.github.io/openai-agents-python/mcp/
- https://openai.github.io/openai-agents-python/guardrails/

Google:
- https://docs.cloud.google.com/mcp/supported-products
- https://docs.cloud.google.com/mcp/prevent-read-write-tool-use
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/connect-to-the-knowledge-mcp-server
