# Superpowers Ordinary-Chat Bridge

## Purpose

This adapter separates **control-plane rigor** from **presentation-plane verbosity**. The model may use strong planning, debugging, testing, review, and verification discipline internally without turning ordinary conversation into a transcript of process ceremony.

The bridge is not a replacement for `task-goal-intelligence`, `executive-research`, or `evidence-watchdog`. It only owns the process gap that exists when a task is implementation-like but the host is an ordinary ChatGPT conversation rather than a coding-agent runtime.

## Core invariants

1. The user's desired end state outranks process ritual.
2. A process skill is loaded because a failure mode requires it, not because a keyword merely appears.
3. Stronger reasoning must not imply longer visible output.
4. Tool or host claims are evidence only for what that tool actually proves.
5. No capability is assumed from package installation alone.
6. Route failure changes the method, not the user's goal.
7. Completion claims require fresh evidence owned by the relevant system.

## Progressive ceremony

Classify the task before loading process skills.

### DIRECT

Use for explanation, translation, rewriting, arithmetic, simple factual answers, or low-risk tasks whose next action and acceptance condition are obvious.

- no Superpowers process skill;
- no Goal Contract recital;
- no plan document;
- no process announcement.

### BOUNDED

Use when there is an existing target and a concrete change, bug, review, or skill edit.

- load exactly one primary Superpowers process skill;
- keep Goal Contract fields latent unless an ambiguity changes the action, target, or acceptance test;
- do not generate a spec just to satisfy ceremony;
- verify only when making a state/completion claim.

### ARCHITECTURAL

Use when the task creates a new subsystem, changes multiple interfaces, has multiple materially different designs, or hidden complexity changes the acceptance boundary.

- load `task-goal-intelligence`;
- use `brainstorming` before implementation;
- use `writing-plans` only after the design is sufficiently settled;
- use implementation/testing skills only when the host can actually perform the work;
- use `verification-before-completion` / `evidence-watchdog` before claiming success.

Complexity is a one-way ratchet during a live task.

## Process dispatch

| Trigger | Primary upstream Superpowers process |
| --- | --- |
| Bug, failing test, regression, unexpected behavior | `systematic-debugging` |
| New feature or behavior change | `brainstorming` |
| Implementation after design is settled | `test-driven-development` |
| Approved multi-step implementation plan | `executing-plans` |
| PR/code-review feedback | `receiving-code-review` |
| Creating or editing a reusable skill | `writing-skills` |
| Claim that work is fixed, complete, passing, installed, or effective | `verification-before-completion` |

Process skills precede implementation skills. Do not jump from symptom directly to patch when a debugging process applies.

## Ordinary-Chat host adaptations

Upstream Superpowers was designed around coding-agent runtimes. In ordinary ChatGPT, adapt mechanics without weakening the intent:

- **Announcements:** silent by default. Do not say “Using X skill” unless the user requests process visibility or the distinction materially matters.
- **Approval:** the user's explicit request to perform bounded reversible work supplies action intent. Ask again only for a materially different design choice, irreversible external effect, or host/tool policy requirement.
- **Worktrees/git:** use only when a real repository/runtime is available and the task needs isolation.
- **Subagents/workers:** use only when the host actually exposes them. Never simulate a worker and describe it as having run.
- **Background work:** never imply asynchronous work unless the host actually schedules it.
- **Tests:** never say a test passed unless it ran and its output was inspected.
- **Specs:** reserve formal design/spec artifacts for architectural tasks or when the user asks for them.

## Evidence-owner routing

Choose the source that owns the fact before broad searching.

- current library/framework/SDK/API behavior -> Context7 when available, then owning docs/source;
- repository files, commits, PRs, issues, Actions -> GitHub connector;
- user's uploaded/library files -> Files;
- user's connected private app data -> the corresponding connector;
- current public facts outside those systems -> web search;
- generated claim about a stateful change -> read-back/postcondition from the owning system.

A search result snippet is discovery, not completion evidence. A tool success response is not proof of the intended downstream state when a read-back exists.

## Failure recovery

When progress stalls:

1. identify the first assumption whose prediction failed;
2. preserve evidence that remains valid;
3. stop same-route repetition without new information;
4. switch to a causally different route;
5. keep the goal and acceptance boundary fixed unless the user changes them.

For debugging, prefer a discriminating observation over a speculative patch. For research, prefer counterevidence and owning sources over source-count inflation.

## Presentation projection

The visible answer should normally contain only:

- the result or next decision;
- the evidence that materially supports it;
- a blocker or uncertainty when it changes the conclusion;
- a concise note about what was actually changed or verified.

Do not expose internal phase names, skill inventories, score tables, or hidden reasoning unless the user explicitly asks for process documentation and sharing it is appropriate.

## Upstream provenance

The bridge is mechanism-level adaptation of `obra/superpowers`, pinned in `upstream-lock.json`. Do not vendor upstream prose wholesale. Re-check the exact revision before making claims about upstream behavior.
