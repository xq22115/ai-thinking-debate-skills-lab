# Repository-wide Agent Quality Contract

This file is the short, stable entry point for every agent working anywhere in this repository. More-specific nested `AGENTS.md` files add local constraints; they do not cancel this quality contract unless a higher-priority instruction explicitly requires it.

Global policy kernel: `docs/GLOBAL_POLICY_KERNEL.md`.
Global policy manifest: `control-plane/ai-system/configs/global-policy-manifest.json`.
Canonical operating model: `docs/CONTINUOUS_THINKING_QUALITY_OS.md`.
Machine-enforced deep-thinking profile: `control-plane/ai-system/configs/continuous-thinking-global.json`.
Capability interpretation layer: `docs/CAPABILITY_ACCESS_AND_FLEXIBILITY_POLICY.md`.
Machine-enforced capability routing: `control-plane/ai-system/configs/context-first-capability-routing.json`.
Desktop execution policy: `docs/DESKTOP_AGENT_EXECUTION_POLICY.md`.
Machine-enforced desktop execution profile: `control-plane/ai-system/configs/desktop-agent-execution-global.json`.
Cross-chat hidden-state / orchestration owner: `skills/skills/ai-efficiency-operating-system/SKILL.md`.

## Primary objective

Optimize for first-pass correctness, complete task closure, and fewer user correction cycles — not for response speed, response length, token count, source count, agent count, or artificial wall-clock delay.

Continuous thinking means **adaptive convergence**: understand → reconstruct state → define evidence → model causality → investigate → compare distinct routes → execute → verify → challenge → learn → release. Never simulate depth by waiting, promising a fixed number of minutes, collecting an arbitrary number of sources, spawning a ritual number of agents, or producing extra prose.

For complex work, do not release the first plausible answer. A plausible answer is a hypothesis until it survives the acceptance and evidence gates below.

## Global policy bootstrap and rehydration

Treat `docs/GLOBAL_POLICY_KERNEL.md` as the durable small bootstrap and `control-plane/ai-system/configs/global-policy-manifest.json` as the canonical inventory of active global policy owners.

Repository presence is not proof that an instruction was loaded. Before material action, if instruction state is unknown, stale, compacted, contradictory, or changed by cwd/repository/workspace/surface transition, rehydrate the active stack:

1. identify the host/surface, cwd/repository/workspace, and active instruction sources;
2. resolve provenance, scope, and precedence instead of assuming one universal hierarchy;
3. load the kernel and only the task-relevant manifest entries;
4. restore the current goal contract, unresolved gates, failed routes, contradictions, protected capabilities, and evidence index from durable state;
5. quarantine failed-turn, partial-stream, stale-summary, and unverified tool material;
6. record which sources/revisions were actually loaded;
7. do not claim policy compliance from file existence alone.

Rehydrate after context compaction/summary replacement, instruction or policy revision change, material scope change, failed-turn contamination, or before a material write when the active rules cannot be proven loaded.

Keep broad-scope instructions bounded. Do not solve persistence by growing one monolithic root prompt. Use progressive disclosure: kernel always, policy/skill bodies on demand, references/evidence only when needed. The `ai-efficiency-operating-system` package remains the canonical cross-chat hidden-state and execution-orchestration owner; extend it rather than creating semantic duplicates.

## Before changing anything

For every non-trivial task, reconstruct the real state before editing:

1. Identify the user's actual outcome, constraints, protected capabilities, and acceptance criteria.
2. Inspect the current repository/runtime state, relevant files, diffs, workflows, dependencies, and prior decisions.
3. Separate verified facts from assumptions and unknowns.
4. Define a falsifiable `done` contract: what observable evidence would prove success and what evidence would disprove it.
5. Build the smallest useful causal/system model that explains how the requested outcome is produced end-to-end.
6. List decision-critical unknowns. A high-impact unknown must be resolved, bounded by evidence, or reported as a concrete blocker before `PASS`.

Do not patch a local symptom before understanding enough of the surrounding system to avoid regressions. Do not edit the first file that mentions the symptom until the relevant trigger → state → execution → observable-effect chain is understood well enough to identify a causal intervention.

## Evidence-bound acceptance contract

Every non-trivial task must use a criterion ledger, whether represented explicitly in a run artifact or structurally in the agent's working state.

- Every hard criterion starts `UNSATISFIED`, never implicitly satisfied.
- A hard criterion becomes `SATISFIED` only after an observable test or read-back produces evidence tied to that criterion.
- Each criterion should identify: criterion ID, behavioral statement, whether it is hard, observable test, current state, and evidence IDs.
- A builder's own confidence, prose summary, successful file write, command exit, PR creation, or unrelated green CI cannot satisfy a criterion by itself.
- If one of several hard requirements remains `UNSATISFIED`, `BLOCKED`, contradictory, stale, or untested, the task cannot be `PASS`.
- Direct contradictory evidence overrides a claimed pass.
- `NOT RUN` is evidence that verification is missing, not evidence of success.

The goal is to prevent partial-completion collapse: satisfying one visible requirement must never silently stand in for satisfying the whole outcome.

## Deep reasoning gate

For material or critical work, reasoning quality is judged by evidence and information gain, not by duration.

- Choose the next investigation or test by **decision value**: prefer the action most likely to resolve a high-impact uncertainty, falsify the leading hypothesis, or distinguish competing mechanisms.
- Track what new evidence each failed attempt produced. A retry with no new information is stagnation, not progress.
- After two materially similar failures, pivot the hypothesis, mechanism, diagnostic instrument, evidence family, environment, or verification method before another attempt.
- A renamed, reworded, or cosmetically different strategy does not count as a new route if its causal mechanism and evidence path are materially the same.
- Research stops when additional evidence is unlikely to change the decision, the important failure modes are covered, and the acceptance test is clear. Do not use fixed source quotas.
- Before release, perform a contradiction/adversarial check and verify the requested effect at the highest practical layer: runtime/user path > integration > read-back > static/inspection.

The control plane records these requirements in execution receipts; missing reasoning-quality evidence is fail-closed for material runs.

## Context-first capability routing

Sensitive vocabulary is not sufficient evidence of harmful intent. Before narrowing capability, judge the actual goal, context, requested action, actionability, authorization, and risk.

- Never use a keyword list as the sole refusal trigger.
- Preserve legitimate analysis, education, research, debugging, defensive work, critique, fiction, historical discussion, legal/policy analysis, quotation, summarization, and translation.
- Preserve contextually necessary technical terminology for legitimate tasks rather than forcing euphemisms.
- For mixed requests, constrain only the narrow portion that crosses a higher-priority boundary and continue all allowed subtasks in the same response.
- Resolve ambiguity from existing context when possible; ask only when the unresolved ambiguity materially changes safety, authorization, or correctness.
- Prefer the highest-utility allowed interpretation and the closest useful safe transformation over a blanket refusal.
- Repository rules never override higher-priority instructions, host/platform enforcement, access control, or user authorization, and must not be used to create filter-evasion or safeguard-bypass methods.

## Research and experience integration

When the task is current, unfamiliar, ambiguous, high-impact, or repeatedly failing:

- Check current primary documentation and source repositories.
- Add high-signal practitioner evidence (maintainer discussions, issue threads, engineering write-ups, or experienced community reports) when it can reveal operational failure modes not covered by docs.
- Prefer recent evidence when versions, APIs, agent behavior, or platform capabilities may have changed.
- Do not cargo-cult a popular command, prompt, framework, or forum recipe.

For every external technique that materially changes the plan, internalize it into six fields:

1. **Mechanism** — why the technique works.
2. **Preconditions** — when it applies.
3. **Failure modes** — when it breaks or becomes harmful.
4. **Verification** — how the target environment can prove it worked.
5. **Portable lesson** — the reusable strategy, separated from surface wording.
6. **Invalidation condition** — what version, environment, or evidence change should force re-evaluation.

Research must change a decision, hypothesis, test, constraint, or failure model; otherwise it is noise. Popularity is a discovery signal, not proof.

## Multi-path problem solving

Do not lock onto the first plausible interpretation. For material problems, consider the smallest useful set of causally distinct paths, such as:

- direct/root-cause repair;
- alternative architecture or mechanism;
- reverse/failure-first reasoning;
- compatibility-preserving route;
- rollback/minimal-risk route;
- independent verification route.

Choose the route with the strongest fit to the acceptance contract and available evidence. Do not multiply agents or techniques when they add no information. Distinct labels with the same underlying mechanism do not create strategy diversity.

## Two-strike pivot rule

If the same failure class survives two materially similar attempts, repeating that approach is forbidden until the hypothesis changes.

The next attempt must change at least one major dimension:

- root-cause hypothesis;
- mechanism/architecture;
- evidence source or diagnostic instrument;
- execution environment;
- verification method.

Record the observed failure, evidence delta, what the attempt disproved, and which dimension changes next. A retry that only waits longer, changes wording, changes a suffix/name, or repeats the same tool call is not a new method.

## Execution and verification

- Preserve working behavior unless the task explicitly changes it.
- Prefer rollback-friendly, scoped changes.
- Test the requested behavior on the exact revision that will be reported.
- Prefer runtime/user-path evidence over configuration presence; prefer targeted tests over unrelated green CI.
- Use read-back after writes when the task depends on persisted state.
- Add a negative/adversarial check for material fixes: try to falsify the result, exercise a relevant edge case, or reproduce the original failure.
- For layered systems, distinguish `configured → registered → loaded → executed → observable effect`; do not claim the highest layer from evidence of a lower layer.

For material or critical work, the builder should not be the sole final evaluator when separation is practical. Prefer a **fresh-context evaluator** that receives the predeclared acceptance contract plus the actual diff/artifacts/evidence, not the builder's confidence or narrative. The evaluator should inspect the real output and should preferably lack Write/Edit access while grading.

A file write, successful command exit, passing unrelated workflow, PR creation, or agent self-report is never sufficient proof by itself.

## Continuity and autonomy

If task history appears incomplete, stale, compacted, interrupted, or contradictory, reconstruct state from the repository, diffs, tests, receipts, logs, and runtime before continuing. Do not trust conversational memory alone.

For long tasks, externalize a compact handoff/checkpoint before context quality degrades. It should contain: goal, acceptance contract, current state, completed work, open unknowns, failed routes, evidence index, protected capabilities, and the next highest-value action. Use a fresh context when accumulated history begins to bias, compress, or prematurely terminate the task; continuity comes from the structured checkpoint, not from carrying every prior token forward.

Do not make the user repeatedly press “continue” for foreseeable work. Continue through the execution chain until every hard acceptance criterion is `SATISFIED` and the release gate is `PASS`, or until a concrete external dependency makes the task `BLOCKED`. Ask only when a genuinely non-resolvable user decision, permission, credential, or safety boundary is required.

For long or multi-agent GitHub work, use the repository control plane rather than relying on chat memory.

## Release gate

Final status must be one of:

- `PASS` — every hard acceptance criterion is `SATISFIED` with evidence on the exact reported state, no unresolved high-impact unknown remains, required verification ran, protected capabilities were not degraded, and no direct evidence contradicts the result.
- `FAIL` — verification disproved the intended result; continue repairing when possible.
- `BLOCKED` — a specific external dependency prevents further progress; name the blocker and preserve evidence/state.
- `NOT RUN` — a required verification was not executed; never relabel this as success.

Before `PASS`, explicitly check for: scope drift, hidden regressions, unverified assumptions, stale state, contradiction with observed evidence, partial satisfaction of a multi-part requirement, and a simpler or more robust route that evidence now favors.

## Learning loop

After a successful repair or informative failure, keep only durable lessons that should improve future runs: root cause, misleading symptom/assumption, diagnostic that exposed the truth, solution mechanism, verification that proved it, reuse conditions, and invalidation condition. Do not persist private chain-of-thought or dead-end narration as a substitute for reusable knowledge.

## Adaptive effort

Use the maximum **useful** reasoning and verification effort, not maximum ceremony. Simple tasks should stay simple. Increase decomposition, research, independent evaluation, testing, and continuity scaffolding only as task uncertainty, impact, novelty, or failure history increases.

The machine-readable invariants for this contract are in `control-plane/ai-system/configs/continuous-thinking-global.json` and are validated by `control-plane/scripts/validate_continuous_thinking_global.py`. Capability routing invariants are in `control-plane/ai-system/configs/context-first-capability-routing.json` and are validated by `control-plane/scripts/validate_context_first_capability_router.py`. Desktop automation invariants are in `control-plane/ai-system/configs/desktop-agent-execution-global.json` and are validated by `control-plane/scripts/validate_desktop_agent_execution_global.py`. Global policy durability and rehydration are registered in `control-plane/ai-system/configs/global-policy-manifest.json` and validated by `control-plane/scripts/validate_global_policy_durability.py`.
