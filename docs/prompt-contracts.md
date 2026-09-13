# Prompt and Task Contracts

Long prompts are not automatically good prompts. FoundLab optimizes for reduced degrees of freedom.

## Contract

A critical task should define:

```markdown
# OUTCOME
The verifiable state that should exist at completion.

# SOURCE OF TRUTH
Authoritative sources in precedence order.

# SCOPE
Included and excluded work.

# CONSTRAINTS
Technical, security, legal and operational boundaries.

# MUTATION POLICY
What may be read, changed locally, changed remotely, or never changed.

# ACCEPTANCE CRITERIA
Objective completion conditions.

# VERIFICATION
Commands, tests, provider evidence or artifact checks.

# OUTPUT
Exact reporting contract.

# STOP CONDITIONS
Conditions that force BLOCKED/UNKNOWN rather than guessing.
```

## Anti-patterns

Avoid substituting persona language for execution constraints.

Bad:
> Be the world's greatest architect and do not make mistakes.

Better:
> Candidate commit must be resolved exactly. Remote writes are denied. Return BLOCKED if required evidence is missing. Run the declared verification before GO.

## Machine-readable tasks

Use `contracts/task.schema.json` and the examples under `examples/tasks/` when execution needs to pass through the Python policy engine.
