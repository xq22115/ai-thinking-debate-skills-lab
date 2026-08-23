# Repository-wide Agent Quality Contract

This file is the short, stable entry point for every agent working anywhere in this repository. More-specific nested `AGENTS.md` files add local constraints; they do not cancel this quality contract unless a higher-priority instruction explicitly requires it.

Canonical operating model: `docs/CONTINUOUS_THINKING_QUALITY_OS.md`.

## Primary objective

Optimize for first-pass correctness, complete task closure, and fewer user correction cycles — not for response speed, response length, token count, or artificial wall-clock delay.

Continuous thinking means **adaptive convergence**: understand → investigate → choose → execute → verify → challenge → release. Never simulate depth by waiting, promising a fixed number of minutes, or producing extra prose.

## Before changing anything

For every non-trivial task, reconstruct the real state before editing:

1. Identify the user's actual outcome, constraints, protected capabilities, and acceptance criteria.
2. Inspect the current repository/runtime state, relevant files, diffs, workflows, dependencies, and prior decisions.
3. Separate verified facts from assumptions and unknowns.
4. Define a falsifiable `done` contract: what observable evidence would prove success and what evidence would disprove it.

Do not patch a local symptom before understanding enough of the surrounding system to avoid regressions.

## Research and experience integration

When the task is current, unfamiliar, ambiguous, high-impact, or repeatedly failing:

- Check current primary documentation and source repositories.
- Add high-signal practitioner evidence (maintainer discussions, issue threads, engineering write-ups, or experienced community reports) when it can reveal operational failure modes not covered by docs.
- Extract the mechanism and conditions that make a technique work; do not cargo-cult commands or copy surface wording.
- Prefer recent evidence when versions, APIs, agent behavior, or platform capabilities may have changed.

Research must change a decision, a hypothesis, a test, or a constraint; otherwise it is noise.

## Multi-path problem solving

Do not lock onto the first plausible interpretation. For material problems, consider the smallest useful set of distinct paths, such as:

- direct/root-cause repair;
- alternative architecture or mechanism;
- reverse/failure-first reasoning;
- compatibility-preserving route;
- rollback/minimal-risk route.

Choose the route with the strongest fit to the acceptance contract and available evidence. Do not multiply agents or techniques when they add no information.

## Two-strike pivot rule

If the same failure class survives two materially similar attempts, repeating that approach is forbidden until the hypothesis changes.

The next attempt must change at least one of:

- root-cause hypothesis;
- mechanism/architecture;
- evidence source or diagnostic instrument;
- execution environment;
- verification method.

Record what the failed attempts disproved so the task does not loop.

## Execution and verification

- Preserve working behavior unless the task explicitly changes it.
- Prefer rollback-friendly, scoped changes.
- Test the requested behavior on the exact revision that will be reported.
- Prefer runtime/user-path evidence over configuration presence; prefer targeted tests over unrelated green CI.
- Use read-back after writes when the task depends on persisted state.
- Add a negative/adversarial check for material fixes: try to falsify the result, exercise a relevant edge case, or reproduce the original failure.
- When practical for complex work, separate builder and evaluator roles. The evaluator must judge against the predeclared acceptance contract and evidence, not the builder's confidence.

A file write, successful command exit, passing unrelated workflow, PR creation, or agent self-report is never sufficient proof by itself.

## Continuity and autonomy

If task history appears incomplete, stale, compacted, interrupted, or contradictory, reconstruct state from the repository, diffs, tests, receipts, logs, and runtime before continuing. Do not trust conversational memory alone.

Do not make the user repeatedly press “continue” for foreseeable work. Continue through the execution chain until the acceptance contract is `PASS`, or until a concrete external dependency makes the task `BLOCKED`. Ask only when a genuinely non-resolvable user decision, permission, credential, or safety boundary is required.

For long or multi-agent GitHub work, use the repository control plane rather than relying on chat memory.

## Release gate

Final status must be one of:

- `PASS` — acceptance criteria verified with evidence on the exact reported state.
- `FAIL` — verification disproved the intended result; continue repairing when possible.
- `BLOCKED` — a specific external dependency prevents further progress; name the blocker and preserve evidence/state.
- `NOT RUN` — a required verification was not executed; never relabel this as success.

Before `PASS`, explicitly check for: scope drift, hidden regressions, unverified assumptions, stale state, and a simpler or more robust route that evidence now favors.

## Adaptive effort

Use the maximum **useful** reasoning and verification effort, not maximum ceremony. Simple tasks should stay simple. Increase decomposition, research, independent evaluation, and testing only as task uncertainty, impact, novelty, or failure history increases.
