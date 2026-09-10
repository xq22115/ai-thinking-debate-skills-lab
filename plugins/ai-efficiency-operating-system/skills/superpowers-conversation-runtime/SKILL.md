---
name: superpowers-conversation-runtime
description: Use when ordinary ChatGPT work involves debugging, implemented behavior changes, feature implementation, code-review feedback, or creating/editing an agent skill.
---

# Superpowers Conversation Runtime

Thin adapter for `obra/superpowers`: keep its discipline without coding-agent ceremony.

## Route

Stay quiet by default.

- bug/failing test/unexpected behavior -> `systematic-debugging`
- new/changed behavior -> `brainstorming`; settled design -> `test-driven-development`
- approved implementation plan -> `executing-plans` when executable here
- review feedback -> `receiving-code-review`
- skill creation/edit -> `writing-skills`
- completion/fixed/passing -> `verification-before-completion`

## Scale

- `DIRECT`: no process skill.
- `BOUNDED`: one process skill; Goal Contract stays latent unless ambiguity changes action or acceptance.
- `ARCHITECTURAL`: add `task-goal-intelligence`, required process, and verification. Complexity may only upgrade.

## Host truth

Never invent worktrees, subagents, background execution, filesystem access, or test runs. An explicit bounded reversible request supplies action intent; re-confirm only for a material design fork or host requirement.

## Output

Do the work first. Surface results, evidence, blockers, and decisions—not process theater.

Load `references/ordinary-chat-bridge.md` only when routing, host adaptation, or evidence ownership is non-obvious.
