# OpenAI Operations Manual

Last verified against official OpenAI documentation: **2026-09-12**.

This file records product-specific operational guidance. Provider behavior changes; re-check the linked official sources before changing policy.

## Surfaces

Use ordinary Chat as the control plane for planning, critique, prompt design, source selection and inexpensive discovery.

Use Work when the outcome is a substantial multi-step deliverable that benefits from orchestration across files/apps/tools.

Use Codex for repository, terminal, test, implementation and software-engineering workflows.

The FoundLab policy is to define the outcome and boundaries before starting expensive agentic execution.

## Shared Work/Codex allowance

OpenAI documents that Work and Codex share the allowance included with eligible plans. Depending on plan, both five-hour and weekly windows can apply. A new five-hour window begins when the first Work/Codex message is sent after the prior window has ended.

Operational consequence:
- do not start a fresh window with low-value discovery;
- use ordinary chat or deterministic scripts for cheap preparation;
- reserve Work/Codex for bounded execution.

Official source:
https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex

## Current model classes

The logical classes in this repository mirror the current Work/Codex product family but remain provider-ID independent:

- Luna — focused, repetitive, high-volume work;
- Terra — everyday work, exploration and routine engineering;
- Sol — complex professional work;
- Astra — the hardest unfamiliar or escalated problems.

The current OpenAI guidance explicitly positions these models along that capability/efficiency curve.

Do not escalate merely because the necessary source, file, permission or context is missing.

Official sources:
https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex
https://help.openai.com/en/articles/20001354-gpt-5-6

## Reasoning

Higher reasoning can consume more allowance. Start at the lowest level that reliably meets the task contract and escalate only when the failure is genuinely reasoning-related.

For Codex, supported reasoning values are model-dependent; the configuration reference currently documents `minimal | low | medium | high | xhigh`.

Official source:
https://developers.openai.com/codex/config-reference

## Fast mode

Fast mode is a latency choice, not a quality requirement. FoundLab policy keeps it off by default and enables it only when interactive latency materially changes the outcome.

## Preflight

Before critical Work/Codex execution:
1. verify quota state in Settings → Usage;
2. verify the selected task manifest and mutation policy;
3. verify authoritative sources are accessible;
4. verify Codex workspace/sandbox/approval settings;
5. verify no secret-bearing environment has been exposed unnecessarily.

The local `flops quota` snapshot is deliberately manual until a supported telemetry integration exists.
