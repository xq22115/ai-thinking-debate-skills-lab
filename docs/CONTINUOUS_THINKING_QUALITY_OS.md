# Continuous Thinking Quality OS

Version: 2.0.0  
Status: Canonical repository quality policy  
Historical snapshot preserved: `../CONTINUOUS_THINKING_QUALITY_OS_v1.0.0.md`

## Purpose

The goal is not to make an agent appear to think longer. The goal is to reduce correction loops, false completion, context drift, shallow fixes, and repeated use of a failing method.

Continuous thinking is implemented as an **adaptive convergence system**:

> reconstruct state → define evidence → research if needed → compare distinct paths → execute → verify → adversarially challenge → learn → release

Quality is measured by observable task closure, not elapsed time, hidden-reasoning claims, token usage, or the number of agents involved.

## 1. First-pass quality target

A strong run should maximize:

- correct understanding of the real objective;
- preservation of existing working behavior;
- root-cause coverage rather than symptom patching;
- current domain knowledge when the environment changes quickly;
- runtime/read-back evidence;
- explicit handling of uncertainty and blockers;
- completion in the same task without unnecessary user babysitting.

The optimization target is **fewer future correction rounds**.

## 2. Task-state reconstruction before action

Before a material change, create a working model of the system. At minimum determine:

1. **Outcome** — what the user actually wants to become true.
2. **Current state** — what is true now, from the system itself rather than memory alone.
3. **Scope** — files, components, services, settings, actors, and environments involved.
4. **Dependencies** — upstream/downstream behavior that can invalidate a local fix.
5. **Protected capabilities** — working behavior that must not be degraded.
6. **Known failure evidence** — errors, logs, reproduction steps, failing tests, stale state, or previous attempts.
7. **Acceptance contract** — observable conditions that constitute `PASS` and observations that would falsify success.

Do not start by editing the first file that mentions the symptom. For bugs, configuration, automation, and agent orchestration, inspect enough surrounding state to understand the failure chain.

If the conversation or task history seems incomplete, compacted, stale, interrupted, or contradictory, reconstruct from repository state, diffs, tests, logs, receipts, runtime state, and the current branch before continuing.

## 3. Acceptance contract before implementation

For non-trivial tasks, define `done` before the solution is locked in.

A good contract is behavioral and falsifiable. Examples:

- the original failure can no longer be reproduced under the same relevant conditions;
- the requested user path succeeds end-to-end;
- the written value can be read back from the actual persistence layer;
- the exact target revision passes the relevant tests;
- a negative/edge case does not regress;
- required status checks correspond to the requested behavior, not an unrelated workflow.

When builder/evaluator separation is available, they should agree on the contract before implementation. This prevents a builder from redefining `done` after seeing its own output.

## 4. Research and expert-experience integration

Research is mandatory when knowledge is likely stale, the domain is unfamiliar, the platform changed recently, the problem is repeatedly failing, or expert operational experience could materially alter the solution.

Use a layered evidence model:

1. current primary documentation and release information;
2. source repositories, issues, pull requests, changelogs, and maintainer discussions;
3. high-signal practitioner reports and engineering/community discussions;
4. direct local/runtime evidence from the target environment.

Do not treat popularity as proof. Community experience is valuable for discovering failure modes, hidden constraints, workflows, and practical tricks that documentation omits; those claims still need validation against the actual task.

### Internalize, do not copy

For every technique that changes the plan, extract:

- **mechanism** — why it works;
- **preconditions** — when it applies;
- **failure modes** — when it breaks;
- **verification** — how to know it worked;
- **portable lesson** — what should be reused on future tasks.

The reusable lesson matters more than the exact prompt or command that produced it.

## 5. Multi-path reasoning without ritual overhead

Material problems should not be locked to the first plausible route. Consider only the distinct paths that can reveal different information, for example:

- direct root-cause repair;
- alternative architecture/mechanism;
- reverse engineering from observed behavior;
- failure-first or adversarial analysis;
- compatibility-preserving/minimal-change route;
- rollback-oriented route;
- independent implementation or evaluation path.

Choose using evidence and the acceptance contract. Do not force a fixed number of paths, agents, debates, or rounds when they do not increase information.

## 6. Two-strike pivot rule

Repeated failure must create information.

If the same failure class remains after **two materially similar attempts**, a third similar retry is prohibited until at least one major dimension changes:

- root-cause hypothesis;
- mechanism or architecture;
- diagnostic instrument;
- evidence/source family;
- execution environment;
- verification method.

Record what each failed attempt disproved. A retry that only changes wording, waits longer, or repeats the same tool call is not a new method.

This rule exists to stop the common cycle of “修 → 還是不行 → 再修同一層 → 還是不行”.

## 7. Adaptive effort router

Do not confuse maximal ceremony with maximal quality.

### Low uncertainty / low impact

Use a short path: understand → execute → verify.

### Medium uncertainty, multi-file, current, or integration work

Add state reconstruction, targeted research, explicit acceptance criteria, regression checks, and read-back.

### High uncertainty, high impact, repeated failure, or long-horizon work

Add independent evaluation, broader failure analysis, stronger runtime testing, persistent state/evidence artifacts, alternative hypotheses, and explicit recovery/rollback planning.

Escalate effort when evidence demands it. Remove scaffolding that no longer adds measurable value.

## 8. Builder–evaluator separation

Agents are often lenient toward their own work. For material tasks, separate generation from judgment when practical.

The evaluator should:

- receive the acceptance contract independently;
- inspect the real output/runtime rather than only the builder's summary;
- try the user path and relevant edge cases;
- search for missing depth, stubs, regressions, and “looks complete” behavior;
- fail the result if any hard criterion is below threshold;
- provide concrete evidence that the builder can act on.

When a separate evaluator is unavailable, emulate this structurally: finish the implementation, then re-open the task from the acceptance contract and attempt to falsify it before reporting success.

## 9. Execution discipline

For software, configuration, automation, and agent tasks:

- inspect before modifying;
- preserve existing capabilities unless explicitly changing them;
- prefer scoped, rollback-friendly changes;
- avoid destructive shortcuts as a substitute for understanding;
- use the strongest relevant native tool before adding new dependencies;
- keep writes conflict-aware and read the current version before replacement;
- test on the exact state/revision that will be reported;
- use the actual target environment when environment differences matter.

Configuration presence is not runtime behavior. Registration is not activation. A script existing is not proof it executed. A PR existing is not proof it works.

## 10. Verification ladder

Prefer stronger evidence when available:

1. **End-to-end user-path/runtime verification** on the target state.
2. **Targeted integration or functional tests** that exercise the changed behavior.
3. **Read-back** from the real persistence/configuration layer after writes.
4. **Unit/static checks** tied to the requested behavior.
5. **Diff/config inspection**.
6. **Documentation or agent self-report**.

Lower levels cannot replace an available higher level when the user asked for actual behavior.

For material fixes, include at least one relevant negative/adversarial check when practical: reproduce the old failure, probe an edge case, break an assumption, or test a nearby regression surface.

## 11. Anti-false-completion barrier

Never declare success from any single weak signal, including:

- a file was written;
- a setting is visible;
- a command exited zero;
- CI is green but does not test the requested behavior;
- an agent said it succeeded;
- a branch/PR exists;
- enough time elapsed;
- the answer sounds complete.

Final status must be explicit:

- `PASS` — acceptance criteria verified on the exact reported state.
- `FAIL` — verification disproved the result; continue repair when possible.
- `BLOCKED` — a concrete external dependency prevents further progress.
- `NOT RUN` — required verification was not executed.

Do not convert `NOT RUN` or uncertainty into `PASS`.

## 12. Same-task autonomy and continuity

The user should not have to repeatedly press “continue” for predictable next steps.

Within the current task, proceed through inspection, research, implementation, verification, repair, and final evaluation until reaching `PASS` or a concrete `BLOCKED` state, subject to tool, permission, safety, and context limits.

Ask the user only when a genuinely non-resolvable decision, credential, permission, or boundary is required. Otherwise choose the most defensible path, state assumptions, and keep going.

For long-running/multi-agent GitHub work, externalize state and evidence through the repository control plane rather than depending on chat memory.

## 13. Learning loop

After a failure or successful repair, capture only durable lessons that should change future behavior:

- root cause;
- misleading symptom or assumption;
- diagnostic that revealed the truth;
- solution mechanism;
- verification that proved it;
- conditions where the lesson should or should not be reused.

Do not preserve every transient thought. Durable memory should contain invariants, decisions, failure patterns, and proven runbooks — not stale dead ends.

## 14. Output discipline

Keep the final answer compact enough to use, but complete enough to verify.

Separate when relevant:

- **FACT** — directly verified;
- **INFERENCE** — conclusion supported by evidence;
- **UNKNOWN/BLOCKER** — not yet verified or externally blocked.

Report what actually changed, what was verified, what failed during the run if it affected the final design, and the remaining risk. Do not expose private chain-of-thought as a substitute for evidence.

## 15. Evidence basis for v2.0.0

This version incorporates lessons from 2026 agent-engineering practice, including:

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world* — short stable agent entry points, progressive disclosure, repository knowledge as system of record, first-class plans, and mechanical verification.
- OpenAI, *Codex-maxxing for long-running work* (2026-06-22) — durable workspaces, continuity, verifiable decomposition, and long-running delegation.
- OpenAI, *How OpenAI uses Codex* — persistent `AGENTS.md`, strong environment setup, issue-like task definition, and Best-of-N where useful.
- Anthropic, *Harness design for long-running application development* (2026-03-24) — planner/generator/evaluator separation, pre-agreed sprint contracts, runtime evaluator testing, strategic pivoting, and removal of scaffolding that stops adding value.
- GitHub, 2026 agent validation guidance — test/lint/security/quality validation and rerunning the original analysis before considering an agent-generated fix ready.
- OpenAI Developer Community, July 2026 practitioner discussions — keep root `AGENTS.md` short and stable, reconstruct repository state when task history is incomplete, and avoid oversized instruction blobs that consume context without improving decisions.

These references are evidence for design principles, not authority to bypass local verification.

## Success metric

The system succeeds when the user needs fewer repair rounds because the agent:

- understands more before acting;
- changes method when evidence disproves a route;
- incorporates current expert experience without cargo-culting it;
- verifies real behavior instead of configuration appearance;
- finishes foreseeable work without repeated prompting;
- reports `PASS` only when the evidence supports it.
