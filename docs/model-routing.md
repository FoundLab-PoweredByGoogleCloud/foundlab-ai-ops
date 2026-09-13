# Model Routing

Last provider check: **2026-09-12**.

## FoundLab logical router

| Class | Default use | Default reasoning |
| --- | --- | --- |
| Luna | bounded extraction, categorization, repetitive edits | low |
| Terra | exploration, documents, repo scans, routine engineering | low |
| Sol | implementation, architecture, security, complex debugging | medium |
| Astra | frontier ambiguity, hard unresolved bugs, adversarial critical review | low |

The executable version lives in `policies/model-routing.yaml`.

## Current Plus planning ranges

OpenAI currently publishes estimated local messages per five-hour period for Plus as:
- Astra: 5–45;
- Sol: 10–100;
- Terra: 25–200;
- Luna: 250–2,000.

These are estimates, not fixed message quotas. Task size, context, reasoning, Fast mode and multi-step behavior can materially change usage. Weekly limits may also apply.

Source:
https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex

## Escalation test

Escalate only after asking:

1. Is the evidence actually available?
2. Does the executor have access to it?
3. Is the task contract unambiguous enough to execute?
4. Did the prior attempt fail because of reasoning rather than missing input?
5. Is the increased allowance spend justified by task risk/value?

If any of 1–3 is false, fix retrieval/permissions/specification first.

## Worker strategy

Use the more capable model as synthesizer when needed and cheaper logical classes for bounded parallel exploration. Keep concurrency low enough that humans can still attribute changes and evidence to a worker.
