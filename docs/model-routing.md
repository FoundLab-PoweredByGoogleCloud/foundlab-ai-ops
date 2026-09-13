# Compute and Model Routing

Version: 0.2.0

The core policy no longer treats provider model names as universal architecture.

## Provider-neutral classes

| Compute class | Intent | Default reasoning |
| --- | --- | --- |
| economy | bounded, repetitive, high-volume | low |
| balanced | exploration, routine engineering | low |
| professional | architecture, implementation, security, hard debugging | medium |
| frontier | hardest unfamiliar/escalated/adversarial work | low, then escalate |

OpenAI's current Work/Codex family maps conceptually:

```text
Luna  -> economy
Terra -> balanced
Sol   -> professional
Astra -> frontier
```

That mapping is stored as compatibility metadata, not as the universal router.

## Routing dimensions

A task is routed by:

1. authority/capability requirements;
2. provider;
3. surface;
4. execution mode;
5. compute class;
6. reasoning effort;
7. approval boundary.

## Escalation test

Before increasing compute/reasoning:

1. Is required evidence available?
2. Is the authoritative system reachable?
3. Is the task contract unambiguous?
4. Did the prior attempt fail because of reasoning?
5. Is the increased cost/quota justified?

Missing input is a retrieval problem, not a reasoning problem.

## Quota domains

Do not merge these into one fake percentage:
- ChatGPT Work/Codex allowance;
- OpenAI API usage/billing;
- Gemini Code Assist/Gemini CLI quota;
- Gemini API usage/billing.

Provider-specific telemetry may be normalized for reporting while preserving its original quota domain.
