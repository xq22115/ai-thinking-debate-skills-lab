---
name: skill-authoring-engine
description: Build or improve reusable agent skills and skill packs in this repository. Use for SKILL.md authoring, trigger design, scripts/references/evals, GitHub Copilot skill packaging, custom-agent integration, host portability, registry updates, and skill validation.
---

# Skill Authoring Engine — GitHub Copilot Projection

## Trigger

Use for creating, editing, refactoring, porting, registering, or validating reusable agent skills and skill packs in this repository. Do not use for ordinary documentation or code changes that do not create a reusable skill capability.

Before authoring or changing a skill:

1. Read the repository root `AGENTS.md`.
2. Read the canonical contract at `skills/skills/skill-authoring-engine/SKILL.md`.
3. Inspect existing skills and registries before creating a new semantic owner.
4. For current GitHub Copilot packaging facts, prefer current GitHub documentation over remembered syntax.
5. Keep the GitHub-specific projection thin; portable logic belongs in the canonical skill.

For complex authoring, use adaptive specialist decomposition from the canonical skill. The coordinator keeps final ownership, independent research/review may run in parallel, and overlapping writes must be serialized.

For GitHub Copilot project skills, keep this path shape:

`.github/skills/<skill-name>/SKILL.md`

A skill may include referenced Markdown, scripts, examples, or other resources in its own directory when useful.

When a dedicated Copilot custom agent improves discoverability or role separation, add a profile under:

`.github/agents/<agent-name>.agent.md`

Do not claim that an account-level or local personal skill was installed merely because repository files exist. Personal Copilot CLI skills live in `~/.copilot/skills` or `~/.agents/skills` and require installation/read-back in that environment.

## Verification

Verification must be layered: validate the package structure, routing/trigger behavior, registry discovery, persisted write read-back, and host-live execution separately. A lower layer cannot stand in for a higher one.

Completion requires repository read-back plus the strongest available behavior test. If a host-live run is unavailable, report that layer as `NOT_RUN` or `UNVERIFIED`.
