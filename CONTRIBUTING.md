# Contributing

## Principles

Changes to this repository may influence human + agent execution. Treat policy changes as production changes.

## Pull requests

A pull request should state:
- problem;
- proposed change;
- affected policy/skill/plugin/memory contract;
- verification performed;
- compatibility or migration impact;
- security implications.

## Policy changes

For changes to model routing, permissions, mutation policy, quota behavior or authority precedence:
1. add or update a Known Answer Test;
2. document the behavioral delta;
3. avoid coupling logical policy to one provider-specific model ID unless the file is explicitly a deployment profile.

## Memory changes

Institutional memory must be durable, non-sensitive and traceable to an authority. Do not commit transient live state merely for convenience.

## Security

Never include real credentials, tokens, customer secrets or sensitive infrastructure identifiers in issues, examples, tests or pull requests.
