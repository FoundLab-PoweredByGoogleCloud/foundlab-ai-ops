# Skill — Incident Triage

## Purpose
Reduce uncertainty during a critical blocker while preserving evidence and minimizing blast radius.

## Workflow
1. Declare the incident question and stop condition.
2. Snapshot authoritative runtime/repository state.
3. Prefer observation before mutation.
4. Form the smallest testable hypothesis.
5. Run one controlled diagnostic step at a time.
6. Preserve commands, timestamps and outcomes.
7. Require review before remote writes; require explicit approval for destructive actions.
8. End with current status, evidence, rollback position and next hypothesis.

## Model policy
Incident classification may justify premium reasoning, but missing evidence must be fixed by retrieval, not by reasoning escalation.
