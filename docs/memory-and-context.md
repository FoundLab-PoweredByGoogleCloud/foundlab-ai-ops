# Memory and Context

## Three separate memory domains

### 1. ChatGPT personal/project memory
Useful for continuity and preferences. It is not institutional authority.

Projects can use default memory or project-only memory. Project-only memory limits cross-project context, but OpenAI currently documents that ChatGPT Work is not available inside a project configured for project-only memory.

Source:
https://help.openai.com/en/articles/10169521-projects-in-chatgpt

### 2. Codex memories
Codex has its own configurable memory system. Current configuration supports controls including:
- `memories.disable_on_external_context`;
- `memories.generate_memories`;
- `memories.min_rate_limit_remaining_percent`;
- `memories.use_memories`.

OpenAI currently documents that `disable_on_external_context=true` prevents threads using MCP/web/tool search from feeding memory generation, and that memory generation has a configurable minimum remaining rate-limit percentage.

Source:
https://developers.openai.com/codex/config-reference

### 3. FoundLab institutional Memory Bank
Versioned, reviewable memory-as-code in this repository.

Use it for:
- invariants;
- durable decisions;
- terminology;
- workflow rules;
- source/authority pointers.

Do not use it as a copy of:
- current GitHub state;
- current Linear state;
- current cloud runtime state;
- customer-sensitive information;
- personal ChatGPT memory.

## Authority rule

Memory is allowed to accelerate retrieval. It is not allowed to manufacture current state.

If a memory entry points to an external authority and freshness is expired, query that authority before presenting the value as current.
