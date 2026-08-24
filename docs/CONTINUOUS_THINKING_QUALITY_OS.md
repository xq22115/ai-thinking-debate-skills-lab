# Continuous Thinking Quality OS

Version: 3.0.0  
Status: Canonical repository quality policy  
Historical snapshot preserved: `../CONTINUOUS_THINKING_QUALITY_OS_v1.0.0.md`  
Machine-readable profile: `../control-plane/ai-system/configs/continuous-thinking-global.json`

## Purpose

The goal is not to make an agent appear to think longer. The goal is to reduce correction loops, false completion, context drift, shallow fixes, confirmation bias, repeated use of a failing method, and self-evaluation bias.

Continuous thinking is an **adaptive evidence-bound convergence system**:

> reconstruct state → define a default-fail acceptance contract → model causality → resolve decision-critical unknowns → research if needed → internalize expert experience → compare causally distinct paths → execute → verify → fresh-context/adversarially evaluate → learn → release

Quality is measured by observable task closure and reduced human rework, not elapsed time, hidden-reasoning claims, token usage, source count, or the number of agents involved.

## 1. First-pass quality target

A strong run should maximize:

- correct understanding of the real objective;
- preservation of existing working behavior;
- root-cause coverage rather than symptom patching;
- current domain knowledge when the environment changes quickly;
- runtime/read-back evidence;
- explicit handling of uncertainty and blockers;
- completion in the same task without unnecessary user babysitting;
- resistance to partial completion and self-confirmation.

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
8. **System/causal model** — the smallest useful explanation of how the requested effect is produced from trigger to observable outcome.
9. **Decision-critical unknowns** — facts that could materially change the chosen fix, architecture, or verdict.

Do not start by editing the first file that mentions the symptom. For bugs, configuration, automation, and agent orchestration, inspect enough surrounding state to understand the failure chain from trigger through persistence/execution to user-visible effect.

If the conversation or task history seems incomplete, compacted, stale, interrupted, or contradictory, reconstruct from repository state, diffs, tests, logs, receipts, runtime state, and the current branch before continuing.

## 3. Default-fail acceptance contract

For non-trivial tasks, define `done` before the solution is locked in. Every hard criterion begins in `UNSATISFIED`; nothing is implicitly satisfied because the answer sounds plausible or an implementation exists.

Each criterion should contain:

- `criterion_id`;
- behavioral statement;
- whether the criterion is hard;
- observable test/read-back;
- state: `UNSATISFIED`, `SATISFIED`, `BLOCKED`, or `NOT_APPLICABLE`;
- evidence IDs that support the state.

A hard criterion can become `SATISFIED` only when observable evidence is tied to that criterion. A file write, zero exit code, PR, green unrelated CI, agent self-report, or the satisfaction of a different requirement is insufficient.

`PASS` requires every hard criterion to be `SATISFIED`. Direct contradictory evidence overrides a pass. Missing required verification is `NOT RUN`, not success. This prevents one checked box from standing in for a multi-part task.

Examples of behavioral criteria:

- the original failure can no longer be reproduced under the same relevant conditions;
- the requested user path succeeds end-to-end;
- the written value can be read back from the actual persistence layer;
- the exact target revision passes the relevant tests;
- a negative/edge case does not regress;
- required status checks correspond to the requested behavior, not an unrelated workflow.

When builder/evaluator separation is available, they should receive the same predeclared acceptance contract. This prevents a builder from redefining `done` after seeing its own output.

## 4. Deep reasoning router

Reasoning depth is adaptive. It is never represented by a fixed waiting time, fixed source quota, or fixed agent count.

### Simple

Low uncertainty, low impact, reversible, familiar. Use: understand → execute → verify.

### Material

Multi-file, current, integration-sensitive, externally visible, ambiguous, or non-trivial failure risk. Add:

- explicit system/causal model;
- decision-critical unknown ledger;
- at least one meaningful competing route or falsification path;
- targeted research where current knowledge matters;
- read-back or stronger verification;
- contradiction/adversarial check;
- evidence-bound acceptance criteria.

### Critical

Repeated failure, high impact, expensive rollback, security/reliability relevance, cross-system orchestration, or long-horizon autonomy. Add:

- fresh-context evaluator or structural builder/evaluator separation;
- stronger runtime/end-to-end testing;
- persistent evidence artifacts/checkpoints;
- explicit recovery/rollback design;
- stagnation detection and forced pivoting;
- final review of remaining risk and invalidation conditions.

Escalate effort when evidence demands it. Remove scaffolding that no longer adds measurable information.

The existing ten-lane control plane is a compatibility/execution topology, not the definition of deep reasoning and not a quality score. Ten shallow copies are not better than a smaller set of causally distinct investigations. Do not use lane count as proof of depth.

## 5. Information-gain rule

At each material decision point, prefer the next action that has the highest **decision value**:

- resolves a high-impact unknown;
- falsifies or supports the leading causal hypothesis;
- distinguishes two plausible mechanisms;
- tests the exact user-visible path;
- removes a blocker that gates all later work.

Do not optimize for visible activity, number of tool calls, number of agents, or amount of prose.

A failed action is useful only if it produces new information. Record the evidence delta: what the failure ruled out, strengthened, or changed.

## 6. Research and expert-experience integration

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
- **portable lesson** — what should be reused on future tasks;
- **invalidation condition** — what future version/environment change would make the lesson unsafe to reuse.

The point is to transform practitioner experience into a reusable decision rule, not paste forum wording into the next answer.

### Research stop rule

Stop research when:

- additional sources are unlikely to change the chosen route;
- the important failure modes are represented;
- the decision-critical unknowns are resolved or explicitly bounded;
- the acceptance test is clear enough to execute.

Never use a fixed source count as evidence of depth.

## 7. Multi-path reasoning without ritual overhead

Material problems should not be locked to the first plausible route. Consider only the distinct paths that can reveal different information, for example:

- direct root-cause repair;
- alternative architecture/mechanism;
- reverse engineering from observed behavior;
- failure-first or adversarial analysis;
- compatibility-preserving/minimal-change route;
- rollback-oriented route;
- independent implementation or evaluation path.

Strategy diversity is causal, not lexical. Renaming a plan, changing a suffix, moving the same logic to another wrapper, or repeating the same mechanism with different wording does not count as a distinct path.

Choose using evidence and the acceptance contract. Do not force a fixed number of paths, agents, debates, or rounds when they do not increase information.

## 8. Stagnation detection and two-strike pivot

Repeated failure must create information.

A run is **stagnating** when a new attempt repeats essentially the same hypothesis, mechanism, evidence source, environment, and verification method without producing a meaningful evidence delta.

If the same failure class remains after **two materially similar attempts**, a third similar retry is prohibited until at least one major dimension changes:

- root-cause hypothesis;
- mechanism or architecture;
- diagnostic instrument;
- evidence/source family;
- execution environment;
- verification method.

Each failed attempt should preserve: observed failure, evidence delta, what the attempt disproved, and the major dimension that will change next. A retry that only changes wording, waits longer, or repeats the same tool call is not a new method.

## 9. Fresh-context builder–evaluator separation

Agents are often lenient toward their own work. For material or critical tasks, the builder should not be the sole final evaluator when separation is practical.

Prefer a **fresh-context evaluator**. Give it:

- the predeclared acceptance contract;
- the actual diff/artifacts/current state;
- raw or referenced verification evidence;
- protected capabilities and relevant constraints.

Do not treat the builder's confidence, summary, or claim of completion as evidence. The evaluator should preferably be read-only while grading so evaluation cannot silently repair the target and then grade the repaired result.

The evaluator should:

- inspect the real output/runtime rather than only the builder's summary;
- try the user path and relevant edge cases;
- search for missing depth, stubs, regressions, and “looks complete” behavior;
- fail the result if any hard criterion remains below threshold;
- identify unresolved high-impact unknowns;
- provide concrete evidence that the builder can act on.

When a separate evaluator is unavailable, emulate this structurally: finish implementation, reset to the acceptance contract and evidence, and deliberately attempt to falsify the result before reporting success.

## 10. Execution discipline

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

For layered systems, reason explicitly across:

> configured → registered → loaded → executed → observable effect

A lower layer cannot prove a higher layer.

## 11. Verification ladder

Prefer stronger evidence when available:

1. **End-to-end user-path/runtime verification** on the target state.
2. **Targeted integration or functional tests** that exercise the changed behavior.
3. **Read-back** from the real persistence/configuration layer after writes.
4. **Unit/static checks** tied to the requested behavior.
5. **Diff/config inspection**.
6. **Documentation or agent self-report**.

Lower levels cannot replace an available higher level when the user asked for actual behavior.

For material fixes, include at least one relevant negative/adversarial check when practical: reproduce the old failure, probe an edge case, break an assumption, or test a nearby regression surface.

## 12. Deep reasoning receipt gate

For material control-plane runs, a `PASS` receipt must include machine-checkable reasoning-quality evidence in addition to ordinary execution evidence.

The receipt must record:

- task class;
- objective/system model;
- causal hypothesis or explanatory model;
- unresolved high-impact unknowns;
- evidence delta from investigation/failure;
- stagnation/pivot state;
- verification level;
- adversarial/falsification check;
- research stop reason.

A `PASS` is fail-closed when:

- any high-impact unknown remains unresolved;
- the research state is blocked;
- reasoning-quality evidence is missing;
- the verifier/adjudicator has only weak inspection-level evidence where read-back/integration/runtime evidence is available;
- direct evidence contradicts the claimed result.

The existing receipt schema/finalizer/adjudicator enforce these v2.1 reasoning-quality fields. The v3 default-fail acceptance model is additionally machine-defined in `continuous-thinking-global.json` and protected against repository drift by `validate_continuous_thinking_global.py`. Do not claim that a downstream product has loaded the profile until that consumer is verified.

## 13. Anti-false-completion barrier

Never declare success from any single weak signal, including:

- a file was written;
- a setting is visible;
- a command exited zero;
- CI is green but does not test the requested behavior;
- an agent said it succeeded;
- a branch/PR exists;
- enough time elapsed;
- a large source count was collected;
- many agents agreed;
- the answer sounds complete.

Final status must be explicit:

- `PASS` — every hard acceptance criterion is verified on the exact reported state, with no unresolved high-impact unknown on the claimed outcome and no direct contradictory evidence.
- `FAIL` — verification disproved the result; continue repair when possible.
- `BLOCKED` — a concrete external dependency prevents further progress.
- `NOT RUN` — required verification was not executed.

Do not convert `NOT RUN` or uncertainty into `PASS`.

## 14. Same-task autonomy and continuity

The user should not have to repeatedly press “continue” for predictable next steps.

Within the current task, proceed through inspection, research, implementation, verification, repair, and final evaluation until reaching `PASS` or a concrete `BLOCKED` state, subject to tool, permission, safety, and context limits.

For long tasks, externalize a compact checkpoint before context quality degrades. Preserve:

- goal;
- acceptance contract;
- current state;
- completed work;
- open unknowns;
- failed routes and what they disproved;
- evidence index;
- protected capabilities;
- next highest-value action.

When accumulated context becomes stale, contradictory, or biasing, start a fresh context from this checkpoint plus current repository/runtime evidence instead of carrying every prior token forward. Continuity means preserving state and causality, not preserving unlimited conversation text.

Ask the user only when a genuinely non-resolvable decision, credential, permission, or boundary is required. Otherwise choose the most defensible path, state assumptions, and keep going.

For long-running/multi-agent GitHub work, externalize state and evidence through the repository control plane rather than depending on chat memory.

## 15. Learning loop

After a failure or successful repair, capture only durable lessons that should change future behavior:

- root cause;
- misleading symptom or assumption;
- diagnostic that revealed the truth;
- solution mechanism;
- verification that proved it;
- conditions where the lesson should or should not be reused;
- invalidation condition or freshness trigger.

Do not preserve every transient thought. Durable memory should contain invariants, decisions, failure patterns, and proven runbooks — not stale dead ends or private chain-of-thought.

## 16. Output discipline

Keep the final answer compact enough to use, but complete enough to verify.

Separate when relevant:

- **FACT** — directly verified;
- **INFERENCE** — conclusion supported by evidence;
- **UNKNOWN/BLOCKER** — not yet verified or externally blocked.

Report what actually changed, what was verified, what failed during the run if it affected the final design, and the remaining risk. Do not expose private chain-of-thought as a substitute for evidence.

## 17. Evidence basis for v3.0.0

This version incorporates current agent-engineering practice and observed operational failure modes:

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world* (2026) — repository knowledge as a system of record, mechanical feedback loops, and adding missing capabilities/guardrails instead of merely asking an agent to try harder.
- OpenAI, *The next evolution of the Agents SDK* (2026-04-15) — durable execution, snapshots/rehydration, sandboxed tool use, and harnesses aligned to model-native operation.
- OpenAI, *A shared playbook for trustworthy third party evaluations* (2026) — harness choice, tools, state preservation, retries, and evidence materially affect observed capability.
- Anthropic, *Harness design for long-running application development* (2026-03-24) — planner/generator/evaluator separation, pre-agreed contracts, fresh evaluation, runtime testing, and strategic pivoting.
- Anthropic, `anthropics/cwc-long-running-agents` — default-FAIL acceptance criteria, structured handoffs, and fresh-context/read-only evaluation patterns for long-running work.
- Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands* (2026-04-08) — harness assumptions must be revisited as model capability changes; durable interfaces should outlive temporary scaffolding.
- Anthropic, *Demystifying evals for AI agents* (2026-01-09) — rigorous end-to-end evals reduce reactive repair loops.
- GitHub, *Evaluating performance and efficiency of the GitHub Copilot agentic harness across models and tasks* (2026-06-25) — harness design materially changes effectiveness and efficiency; more orchestration is not automatically better.
- Maintainer/community reports about long-run drift, retry spirals, context/tool bloat, and state replay are used as failure-mode discovery signals, not as proof; any technique taken from them must still be verified against the target environment.

These references justify design principles; they never replace local/runtime verification.

## Success metric

The system succeeds when the user needs fewer repair rounds because the agent:

- understands more before acting;
- converts the real goal into default-fail behavioral criteria;
- chooses investigations by information gain rather than visible activity;
- changes method when evidence disproves a route;
- incorporates current expert experience without cargo-culting it;
- uses fresh-context evaluation to counter self-confirmation;
- verifies real behavior instead of configuration appearance;
- refuses `PASS` while any hard criterion or high-impact unknown remains unresolved;
- finishes foreseeable work without repeated prompting.
