# Plugins, Skills and MCP

Last provider check: **2026-09-12**.

## Plugins

OpenAI currently defines a plugin as a package that may include Skills, connected apps, app templates, or combinations of these. Connected apps remain subject to provider authorization, workspace controls, supported read/write actions and approval requirements.

Source:
https://help.openai.com/en/articles/20001256-plugins-in-codex

FoundLab therefore separates:
- plugin/capability registration;
- provider connection state;
- FoundLab permission policy;
- provider IAM.

Installation never grants institutional authority by itself.

## Skills

OpenAI defines Skills as reusable/shareable workflows that may include instructions, examples, resources and code. Personal Skills availability varies by plan/workspace/product surface; Codex support can differ from ChatGPT.

Source:
https://help.openai.com/en/articles/20001066

FoundLab stores portable Skills in this repository regardless of whether a particular product surface supports native installation.

A Skill tells an executor **how** to work. It does not grant permission to perform a mutation.

## MCP

Current Codex MCP documentation supports local STDIO servers and Streamable HTTP servers. HTTP connections can use bearer-token and OAuth authentication.

Source:
https://developers.openai.com/codex/mcp

FoundLab MCP design rules:
- prefer narrow typed tools over arbitrary shell execution;
- separate read, plan, apply and destructive capabilities;
- expose provider authority without bypassing provider IAM;
- keep credentials outside prompts and repository state;
- preserve a policy gate before write-capable operations.

## GCP target

The planned GCP MCP is intentionally not a `gcloud(anything)` wrapper. See `mcp/foundlab-gcp-mcp/SPEC.md`.
