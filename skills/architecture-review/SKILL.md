# Skill — Architecture Review

## Purpose
Evaluate an architecture against explicit invariants, trust boundaries and operational constraints.

## Workflow
1. Identify canonical architecture sources.
2. Enumerate actors, trust boundaries, state and authority.
3. Separate deterministic controls from probabilistic components.
4. Trace failure modes and fail-open/fail-closed behavior.
5. Evaluate identity, secrets, data persistence, observability and rollback.
6. Produce concrete deltas, not a greenfield redesign unless requested.

## Output
Observed architecture, invariant violations, priority-ranked deltas, evidence gaps and residual risk.
