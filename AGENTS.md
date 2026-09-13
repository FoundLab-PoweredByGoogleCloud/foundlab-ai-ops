# FoundLab AI Ops — Agent Instructions

## Purpose

This repository is the versioned governance layer for FoundLab's human + agent workflows.

## Authority order

When sources conflict, use this precedence unless a task explicitly defines a stricter order:

1. current repository state and versioned policy;
2. authoritative connected systems for their own live state;
3. task-specific evidence supplied for the current run;
4. current conversation instructions;
5. conversation context;
6. memory.

Memory must never silently override current authoritative evidence.

## Default execution policy

- Inspect before modifying.
- Prefer the smallest defensible change.
- Separate observed facts, inference, and unknowns.
- Do not invent missing evidence.
- External writes require explicit authorization.
- Destructive operations require explicit confirmation.
- Never expose, print, persist, or commit secrets.
- Do not weaken tests, gates, IAM, or security controls to make a task pass.
- Verify before declaring completion.

## Engineering

Before changing code:
1. identify the governing policy and relevant skill;
2. inspect adjacent tests and contracts;
3. make a minimal change;
4. run the narrowest relevant verification first;
5. run the repository test suite before completion.

## Model routing

Logical model classes are defined in `policies/model-routing.yaml`.
Do not hard-code provider model IDs into policy logic.

Escalation is permitted for reasoning difficulty. Escalation is not a substitute for missing context, permissions, or evidence.

## Completion contract

Material work must report:
- status;
- sources/evidence inspected;
- changes;
- verification;
- unknowns;
- residual risks;
- next action.

## Repository boundaries

This public repository must not contain:
- credentials or private keys;
- personal memory exports;
- customer-sensitive information;
- production secrets or private resource identifiers;
- transient operational state better queried from its authoritative system.
