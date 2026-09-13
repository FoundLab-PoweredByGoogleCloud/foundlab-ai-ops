# Memory Bank

The Memory Bank is **institutional memory-as-code**. It is not an export of ChatGPT memory and it is not a cache of live provider state.

## Memory classes

- **Personal memory** — user preferences and continuity. Keep in the product's personal memory layer, not here.
- **Operational memory** — local, short-lived execution state. Keep under `~/.foundlab-ai-ops/` or the authoritative external system.
- **Institutional memory** — durable, reviewable facts, decisions, invariants, terminology and authority pointers. This repository may store these.

## Rules

1. Every institutional memory entry must identify its type and authority.
2. Fast-changing state should be represented by an authority pointer, not copied here.
3. A stale entry must never be promoted to current truth.
4. Memory cannot silently override Git, GitHub, Linear, Google Drive, GCP or another designated authority.
5. Sensitive or personal memory must not be committed to this public repository.

## Recommended entry types

- architectural_fact
- decision
- invariant
- glossary
- workflow
- authority_pointer
- assumption

## Lifecycle

Candidate → classify → review → merge → periodically revalidate or supersede.
