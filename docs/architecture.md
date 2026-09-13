# Architecture

FoundLab AI Ops separates six concerns.

## 1. Policy plane
Deterministic rules for routing, quota, permissions, mutation and source authority.

## 2. Execution plane
The Python engine evaluates task manifests and emits bounded execution decisions. Codex, Work, CLIs and future MCP adapters are executors, not policy authorities.

## 3. Capability plane
Plugins, connected apps, CLIs and MCP servers expose capabilities. The registry describes what a capability is authoritative for and which mutations require review.

## 4. Workflow plane
Skills define reusable procedures. A Skill explains how to perform a class of task; it does not grant permission to perform it.

## 5. Knowledge plane
The Memory Bank stores durable institutional context and authority pointers. Live state remains in its authoritative system.

## 6. Evidence plane
The local journal records task hashes and policy decisions. Future adapters may attach provider evidence, hashes and receipts without changing the core authority model.

## Separation rule

- Skill: how to perform work.
- Policy: what is allowed.
- Plugin/capability: what can be accessed.
- Memory: what durable context is known.
- Engine: what execution decision follows.
- Evidence: what proves what happened.
