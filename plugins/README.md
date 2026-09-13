# Plugins and Capabilities

This directory describes external capabilities independently from any single ChatGPT account.

A plugin/connected app may be installed in one environment and absent in another. Therefore connection state is runtime state and must not be hard-coded as institutional truth.

## Capability rules

- Register authority separately from permission.
- Read capability does not imply write capability.
- Write capability does not imply destructive capability.
- Provider IAM remains authoritative for actual access.
- A FoundLab policy denial must not be bypassed merely because the provider would permit the action.

Future private capabilities should prefer narrow typed tools over arbitrary shell/API execution.
