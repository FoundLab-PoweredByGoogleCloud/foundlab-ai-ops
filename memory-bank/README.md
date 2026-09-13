# Institutional Memory

Directory compatibility name: `memory-bank/`.

In v0.2 the canonical concept is **Institutional Memory** to avoid confusion with provider products that also use the name "Memory Bank".

This directory is versioned institutional memory-as-code. It is not:
- an export of ChatGPT personal memory;
- a copy of Vertex runtime memory;
- a cache of current cloud/provider state.

## Memory domains

### Personal memory
Preferences and continuity managed by the user/product. Not authoritative for repository/cloud state.

### Operational/runtime memory
Short-lived session/agent state. Keep in the runtime or `~/.foundlab-ai-ops/`.

### Institutional memory
Durable, reviewable facts, decisions, invariants, terminology, workflow rules and authority pointers. This directory stores that class.

## Rules

1. Every institutional entry identifies its type and authority.
2. Fast-changing state should be represented by an authority pointer rather than copied here.
3. Stale entries must not be promoted to current truth.
4. Institutional memory cannot silently override Git, GitHub, Linear, Google Drive, GCP or another designated authority.
5. Sensitive/personal memory must not be committed to this public repository.
6. Provider runtime memory is a deployment concern, not the canonical institutional record.

## Lifecycle

Candidate → classify → review → merge → revalidate/supersede.
