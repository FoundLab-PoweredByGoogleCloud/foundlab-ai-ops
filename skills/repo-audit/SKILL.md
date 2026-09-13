# Skill — Repository Audit

## Purpose
Establish what actually exists in a repository before proposing changes.

## Inputs
- repository/worktree;
- task objective;
- optional candidate ref.

## Authority
1. Git object state;
2. files in the selected ref/worktree;
3. CI evidence;
4. GitHub remote metadata;
5. conversation context;
6. memory.

## Workflow
1. Resolve repository, ref and working-tree state.
2. Inventory relevant source, tests, config, generated outputs and evidence.
3. Identify duplicated or historical copies before treating files as canonical.
4. Trace claims to concrete paths, symbols or commits.
5. Separate observed, inferred and unknown.
6. Produce findings before recommending mutation.

## Mutation policy
Read-only unless the task separately authorizes changes.

## Output
Status, scope inspected, material findings, unknowns, risks, and next action.
