# Skill — Release Gate

## Purpose
Determine whether a uniquely identified candidate satisfies declared release gates.

## Required inputs
- candidate identifier;
- release policy/gates;
- repository or artifact evidence.

## Workflow
1. Resolve candidate identity unambiguously.
2. Resolve required gates from versioned policy.
3. Inspect or execute the narrowest trustworthy verification.
4. Validate evidence provenance.
5. Report every failed, missing, or not-run gate.
6. Return GO, NO_GO, PARTIAL, or BLOCKED.

## Stop conditions
- candidate cannot be uniquely identified;
- required evidence is unavailable;
- source conflict cannot be resolved.

## Mutation policy
Read-only by default. A release decision never implies deployment authorization.
