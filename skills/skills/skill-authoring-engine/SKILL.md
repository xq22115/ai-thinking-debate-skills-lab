---
name: skill-authoring-engine
description: Design, create, refactor, validate, and register reusable AI agent skills or skill packs. Use when a task asks to build or improve SKILL.md-based capabilities, custom agent skills, portable skill packages, or host-specific projections for GitHub Copilot, Claude/Agent Skills, OpenAI/Codex-style agent runtimes, or similar systems.
---

# Skill Authoring Engine

## Purpose

Turn a requested capability into a small, testable, discoverable, host-aware skill package instead of a monolithic prompt.

This skill owns the authoring lifecycle. It may use an upstream writing-skills method as a process aid, but this package remains the repository's canonical skill-authoring contract.

## Trigger

Use this skill when the requested outcome materially includes one or more of:

- create a new agent skill or skill pack;
- rewrite or improve an existing `SKILL.md`;
- split a monolithic skill into progressive-disclosure resources;
- add scripts, references, examples, evals, manifests, or host adapters to a skill;
- port a skill between GitHub Copilot, Claude/Agent Skills, OpenAI/Codex-style runtimes, IDE agents, or MCP-backed systems;
- diagnose why a skill is not discovered, triggered, loaded, executed, or verified.

Do not invoke for ordinary coding, documentation, or prompt editing that does not create a reusable capability.

## Core invariant

`SKILL_EXISTS != SKILL_WORKS`

Track the chain separately:

`REQUESTED_CAPABILITY -> DISCOVERABLE -> SELECTED -> LOADED -> EXECUTED -> OBSERVABLE_EFFECT -> VERIFIED`

Repository presence proves only the first layers.

## Authoring pipeline

### 1. Reconstruct the real capability request

Define:

- user outcome;
- target host(s);
- trigger examples and non-trigger examples;
- required tools and permissions;
- expected artifacts or state changes;
- protected existing behavior;
- acceptance tests;
- unknowns that can change the design.

Search the repository before creating a new skill. Prefer extending an existing semantic owner over creating a duplicate.

### 2. Build a Skill Contract

Before writing prose, capture:

- `name` — lowercase, hyphenated, stable identifier;
- `description` — what the skill does and when it should activate;
- `inputs` — information the skill expects;
- `outputs` — concrete artifact/state/result;
- `host assumptions` — GitHub, filesystem, shell, MCP, browser, sandbox, etc.;
- `side effects` — writes, commands, PRs, external mutations;
- `verification` — observable checks;
- `failure states` — BLOCKED, NOT_RUN, unsupported host, permission gap;
- `rollback` — how to undo material mutations.

### 3. Choose the smallest useful package shape

Default structure:

```
<skill-name>/
  SKILL.md
  references/        # only when detail would bloat the routing surface
  scripts/           # only for deterministic or machine-checkable work
  tests/ or evals/   # when trigger/behavior regressions matter
  assets/            # only when the runtime consumes them
```

Keep `SKILL.md` as a thin routing and execution contract. Put long examples, host matrices, schemas, or deep procedures in `references/`.

Do not create empty directories or ceremonial files.

### 4. Use adaptive multi-agent authoring when complexity justifies it

A coordinator owns the final package. Specialist roles are spawned only when they add independent information or reduce coupling.

Useful roles:

- **capability-architect** — converts the request into a Skill Contract;
- **trigger-designer** — designs positive, negative, ambiguous, and collision cases;
- **implementation-author** — writes the package and deterministic helpers;
- **host-compatibility-reviewer** — checks current target-host requirements;
- **adversarial-verifier** — tries to make the skill mis-trigger, overreach, or claim unsupported success;
- **registry-integrator** — registers the capability and checks discovery paths;
- **merge-integrator** — resolves overlapping edits and verifies the exact merged revision.

Parallelize independent work such as host research, trigger-case generation, and adversarial review. Serialize writes that touch the same file or registry entry.

Do not use a fixed number of agents as a quality proxy.

### 5. Write trigger semantics before implementation detail

The `description` must distinguish:

- when the skill should activate;
- when it should not;
- the domain/outcome it owns;
- collisions with neighboring skills.

For material skills, create at least:

- positive trigger cases;
- negative cases;
- ambiguous cases;
- neighboring-skill collision cases;
- unsupported-host or missing-permission cases.

### 6. Separate portable logic from host projection

Portable skill logic must not silently depend on one runtime.

Host-specific packaging belongs in adapters or projections such as:

- GitHub Copilot: `.github/skills/<name>/SKILL.md`, optional `.github/agents/*.agent.md`;
- personal Copilot CLI skill: `~/.copilot/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md`;
- Claude/Agent Skills: target runtime's supported skills directory;
- OpenAI/Codex-style runtimes: current supported plugin/skill packaging;
- MCP-backed runtimes: tools and server capabilities remain separate from skill prose.

Verify current official host requirements before installation because these surfaces change quickly.

### 7. Add deterministic machinery only where it helps

Use scripts for checks that should not depend on model judgment, for example:

- frontmatter validation;
- name/path consistency;
- referenced-resource existence;
- schema validation;
- trigger fixture linting;
- manifest/registry consistency;
- generated artifact comparison.

A script exit code is evidence about that check only; it is not proof of host activation.

### 8. Register the capability

Update the narrowest authoritative registry or manifest used by the host/control plane.

Registration should expose at least:

- canonical skill path;
- host projection paths;
- status;
- trigger owner;
- validation entrypoint;
- compatibility or activation caveats.

Avoid copying the same semantic owner into multiple competing registries.

### 9. Verify in layers

Minimum verification ladder for a material skill:

1. static structure validates;
2. trigger fixtures pass;
3. references/scripts resolve;
4. registry discovers the skill;
5. host-specific projection is syntactically valid;
6. fresh-context run selects the skill for positive cases;
7. fresh-context run rejects negative/collision cases;
8. intended behavior executes with real tools when required;
9. resulting artifact/state is read back;
10. exact reported revision is rechecked after merge.

Use `NOT_RUN` when a layer was not executed.

### 10. Release only with a compact evidence receipt

Report:

- exact skill name and paths;
- changed revision/branch;
- validations actually executed;
- trigger coverage;
- host-live status;
- unresolved blockers or unverified layers.

Never convert repository presence, generated prose, a successful write, or a green unrelated workflow into a host-live claim.

## Quality rules

- Prefer one semantic owner per capability.
- Prefer progressive disclosure over giant `SKILL.md` files.
- Prefer executable validation for deterministic invariants.
- Prefer fresh-context trigger evaluation over self-review.
- Prefer current official host docs for packaging facts.
- Preserve working behavior unless the request explicitly changes it.
- Do not bury tool permissions or side effects in prose.
- Do not hard-code a vendor/model unless the capability truly requires it.
- Do not create fake multi-agent diversity by cloning the same prompt.
- Do not mark a skill `STABLE` from visible fixtures alone.

## Completion gate

The skill-authoring task is complete only when the requested capability is represented by the correct package, is registered where required, and every claimed verification layer has evidence on the exact reported revision.
