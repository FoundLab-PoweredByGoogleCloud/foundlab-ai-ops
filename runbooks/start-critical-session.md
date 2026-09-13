# Runbook — Start a Critical Session

1. Run `flops doctor`.
2. Record the current quota snapshot with `flops quota set`.
3. Identify the authoritative systems required for the task.
4. Create or review a task manifest.
5. Run `flops plan <task.yaml>`.
6. Verify the selected profile, logical model class, reasoning level, mutation policy and required sources.
7. Retrieve missing evidence before escalating reasoning.
8. Execute the task.
9. Verify acceptance criteria.
10. Preserve material evidence and residual risk in the task output/journal.

Do not begin a costly agentic session with discovery that can be completed cheaply in ordinary chat or deterministic tooling.
