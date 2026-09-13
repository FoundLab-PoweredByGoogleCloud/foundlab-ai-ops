# Codex Governance

Last provider check: **2026-09-12**.

## AGENTS.md

Codex currently discovers a global instruction file under the Codex home and then project instructions from repository root down toward the working directory. `AGENTS.override.md` takes precedence over `AGENTS.md` at a given level. The default combined project instruction limit is currently 32 KiB.

Source:
https://developers.openai.com/codex/guides/agents-md

Policy:
- global AGENTS: reusable personal/team working agreement;
- repository AGENTS: repository-wide invariant and verification rules;
- nested override: only when a subtree genuinely requires different behavior.

Do not turn AGENTS files into project history dumps.

## Sandbox and approvals

The current Codex configuration reference documents:
- `approval_policy`;
- `sandbox_mode = read-only | workspace-write | danger-full-access`;
- configurable agent concurrency;
- model reasoning settings.

FoundLab baseline:
- `approval_policy = "on-request"`;
- `sandbox_mode = "workspace-write"` for routine implementation;
- use `read-only` for audit/release inspection where mutation is unnecessary;
- do not make `danger-full-access` a default.

Source:
https://developers.openai.com/codex/config-reference

## Secret-bearing environment

A particularly important current default is `shell_environment_policy.ignore_default_excludes=true`, which keeps variables with names containing KEY, SECRET or TOKEN before other filters run. Setting it to false enables those automatic secret-name exclusions.

FoundLab baseline explicitly sets:

```toml
[shell_environment_policy]
ignore_default_excludes = false
```

Source:
https://developers.openai.com/codex/config-reference

## Parallelism

The current configuration supports `agents.max_concurrent_threads_per_session`. FoundLab keeps a low default because parallel agents multiply usage and increase attribution/merge complexity.
