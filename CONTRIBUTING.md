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

## Merge gate

For policy, routing, permission, security, executor configuration or control-plane changes, do not merge solely because CI is green.

Required before merge:
1. repository validation PASS;
2. test suite PASS;
3. configured asynchronous agent review has completed;
4. zero unresolved P1/P2 findings from that review;
5. any material finding is fixed with a regression test or explicitly dispositioned before merge.

If an automated review arrives after a merge, open an immediate remediation change rather than treating the prior CI result as sufficient.

## Policy changes

For changes to model routing, permissions, mutation policy, quota behavior or authority precedence:
1. add or update a Known Answer Test;
2. document the behavioral delta;
3. avoid coupling logical policy to one provider-specific model ID unless the file is explicitly a deployment profile.

## Memory changes

Institutional memory must be durable, non-sensitive and traceable to an authority. Do not commit transient live state merely for convenience.

## Security

Never include real credentials, tokens, customer secrets or sensitive infrastructure identifiers in issues, examples, tests or pull requests.
