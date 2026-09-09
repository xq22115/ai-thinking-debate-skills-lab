---
name: superpowers-conversation-runtime
description: Use when an ordinary ChatGPT task involves debugging, changing implemented behavior, implementing a feature, applying code-review feedback, or creating/editing an agent skill.
---

# Superpowers Conversation Runtime

A thin host adapter for `obra/superpowers`. Preserve Superpowers discipline without importing coding-agent ceremony into ordinary chat.

## Dispatch

Stay quiet by default; do not announce skill names unless the user asks.

- bug, failing test, unexpected behavior -> `systematic-debugging`
- new or changed behavior -> `brainstorming`; after design is settled -> `test-driven-development`
- approved implementation plan -> `executing-plans` only when the host can actually execute it
- review feedback -> `receiving-code-review`
- skill creation/edit -> `writing-skills`
- completion/fixed/passing claim -> `verification-before-completion`

## Ceremony scaling

- `DIRECT`: no Superpowers process skill.
- `BOUNDED`: one process skill; keep the Goal Contract latent unless ambiguity changes the action or acceptance test.
- `ARCHITECTURAL`: combine `task-goal-intelligence` with the needed Superpowers process and verification. Complexity may upgrade, never silently downgrade.

## Host truth

Never invent worktrees, subagents, background execution, filesystem access, or tests that did not run. An explicit request to perform bounded reversible work counts as action intent; extra confirmation is only for a material design fork or host/tool requirement.

## Output

Do the work first. Surface decisions, evidence, blockers, and results—not process theater.

Read `references/ordinary-chat-bridge.md` when routing, capability adaptation, or evidence ownership is non-obvious.
