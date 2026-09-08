---
name: multi-agent-deliberation
description: Route complex tasks through a small active set of genuinely different roles, preserve useful disagreement, and scale toward larger councils only when marginal information gain or consequence justifies it.
---

# Multi-Agent Deliberation

Version: `0.2.0-rc1`

## Objective

Use multiple agents to increase epistemic and capability diversity, not to manufacture agreement, satisfy a numeric headcount, simulate independent execution, or let social dynamics substitute for evidence.

## Role Pool vs Active Set

Treat the 30-role design as a **coverage pool**. Activate only roles that add at least one of:

- an independent evidence channel;
- a materially different hypothesis or method;
- a required domain capability;
- adversarial/falsification pressure;
- an independent verification duty;
- a distinct integration/compatibility risk view.

Do not activate clones merely to increase headcount.

## Routing

- Tier 0: 1 agent for deterministic, low-uncertainty tasks.
- Tier 1: 2–4 independent approaches/review roles when a second method can change the decision.
- Tier 2: 5–9 roles for competing hypotheses, red team, evidence audit, compatibility and integration.
- Tier 3: 10–18 specialists for cross-domain, security, high uncertainty, or deployment risk.
- Tier 4: up to 30 roles only while distinct responsibilities and positive marginal information gain remain.

Escalate when:
- critical unknowns remain;
- high-quality sources conflict;
- decision consequence is high;
- independent subproblems can be investigated safely in parallel;
- a minority hypothesis remains plausible and discriminating tests exist.

De-escalate when:
- new roles repeat existing evidence/methods;
- execution/testing has higher expected information gain than discussion;
- merge/synthesis overhead exceeds expected insight;
- acceptance criteria are already directly testable.

Do not de-escalate merely to escape a blocker, reduce requested reasoning effort, or make an unmet acceptance gate easier to pass.

## Contribution Gate

A numeric agent count is never sufficient evidence that multi-agent deliberation occurred or helped the task.

Every activated agent that is counted toward a requested or configured council must have:

- a distinct assigned causal role;
- a unique evidence, test, artifact, implementation, diagnosis, falsification, or verification contribution;
- an explicit mapping from that contribution to ROOT_GOAL, HARD_CONSTRAINTS, a material unknown, or ACCEPTANCE_TESTS;
- a result that can affect the plan, verdict, implementation, or confidence.

An agent whose only output is generic refusal, policy/ethics discussion, agreement, encouragement, restatement, or commentary does **not** count unless that analysis is itself part of the user's requested task.

The coordinator/judge must reject zero-information-gain participants rather than using them to satisfy headcount. If five roles are requested, five logically distinct review duties may be defined, but **five independent runtime agents may be claimed only when the host exposes actual independent executions and receipts prove them**. Never convert logical roles into a false runtime-independence claim.

## Blocker / Goal Separation

A Stop hook, controller response, unavailable route, permission/capability state, tool failure, or retry condition is `CURRENT_BLOCKER`, not a replacement for `ROOT_GOAL`.

When a participant is blocked:

- preserve ROOT_GOAL and GOAL_SIGNATURE;
- choose the highest-value goal-advancing action still available;
- change method, layer, instrument, decomposition, evidence path, or execution route before changing the goal;
- do not spend the council on defeating, weakening, killing, gaming, or string-matching around the controller merely to exit work;
- do not substitute a council about why the task cannot be done for concrete progress on the portions that can be advanced;
- do not lower the requested agent budget, reasoning effort, tests, or acceptance criteria merely to make the blocker disappear.

Controller analysis counts only when diagnosing or modifying that controller is itself an authorized, task-relevant objective; even then, it remains bound to the original Goal Contract and observable acceptance tests.

## Message Policy

Always retain:
- new evidence with provenance;
- decisive contradiction;
- discriminating test;
- blocking risk;
- minority hypothesis with strong evidence;
- capability/permission uncertainty that affects execution;
- unresolved obligation relevant to completion;
- a material confidence revision and its evidence delta.

Compress or drop repeated agreement, stylistic paraphrases, and role-play without new evidence.

## Independence Policy

Keep these distinct:

- `ROLE_DIVERSITY` — different assigned perspectives;
- `METHOD_DIVERSITY` — genuinely different reasoning/testing routes;
- `EVIDENCE_DIVERSITY` — different independent evidence channels;
- `RUNTIME_INDEPENDENCE` — distinct observed executions/processes/sessions when that matters.

Role labels do not prove runtime independence. When authentic multi-agent execution is a claim, use wrapper/host receipts or equivalent observable evidence.

## Productive Disagreement / Anti-Sycophancy Policy

Agreement is an outcome to be earned, not an optimization target.

Rules:

1. Agents must state their initial hypothesis or uncertainty **before** reading a peer's final conclusion when practical.
2. An agent may revise after seeing new evidence, but every material revision must identify the evidence or argument that changed its state.
3. `I agree` without a new evidence delta, corrected warrant, discriminating test, or explicit resolution of a crux is zero-information agreement.
4. Preserve a minority branch when its evidence quality exceeds its vote count.
5. Do not reward social smoothness, confidence, repeated consensus, or deference to a supposedly stronger agent.
6. If consensus arrives unusually early while critical uncertainty remains, trigger one targeted dissenter/falsifier pass rather than another agreement round.
7. Do not force agents to defend an assigned stance after decisive counterevidence; stance assignment is temporary stress testing, not identity.

## Judge Policy

Rank claims by:

1. direct/reproducible evidence;
2. current primary/spec/product evidence for current claims;
3. independent corroboration;
4. discriminating tests and falsifiability;
5. coherent inference with explicit uncertainty.

Majority count is a weak signal and must not erase a better-evidenced minority position.

### Bias-resistant adjudication

For material judgments, the judge should resist known conversational and presentation biases:

- **position/order bias** — do not prefer an argument because it appeared first/last;
- **verbosity bias** — length is not evidence strength;
- **bandwagon bias** — agent count is not epistemic weight;
- **confidence/style bias** — assertiveness, fluency, wit, or rhetorical force are not correctness;
- **shared-reasoning contamination** — do not let the judge merely echo the council's dominant narrative;
- **follow-up persuasion bias** — a later rebuttal is not automatically stronger because it is framed as a correction.

When consequence and cost justify it, use one or more of these checks:

1. **Blind labels:** score candidate claims as A/B/... without prestige/model/role metadata.
2. **Independent first score:** judge the evidence graph before reading the council's vote tally or consensus statement.
3. **Order swap:** re-evaluate after reversing candidate order; a material verdict flip is a bias warning.
4. **Length-normalized summary:** compare equivalent compact claim/evidence summaries before rewarding detail.
5. **Evidence-only pass:** temporarily hide rhetorical framing and inspect claim → support/attack/defeater relations.
6. **Minority audit:** explicitly test the strongest minority claim against the winner.
7. **Meta-judge separation:** for high-impact decisions, prefer a fresh-context evaluator over the same debaters grading their own exchange when practical.

A judge must record the decisive evidence or crux. `The majority agreed` is never an adequate final justification.

## Argument-Graph Adjudication

For non-linear debates, flattening everything into one prose summary can hide dependencies. When the dispute is complex, judge a compact graph containing:

- claim nodes;
- support edges;
- attack/contradiction edges;
- dependency/warrant edges;
- defeater/counterexample edges;
- evidence obligations;
- unresolved cruxes.

Prefer the position whose decisive claims survive the strongest relevant attacks with the best evidence, not the position with the most text or supporters.

## Stop Rule

Stop debate when execution, measurement, read-back, or targeted testing is more informative than another discussion round, or when marginal information gain collapses. A controller block does not authorize goal substitution: continuation remains bound to the Goal Contract.

Do **not** stop merely because all agents agree. Consensus while material evidence obligations remain open is not completion.

## Output Contract

Return:
- activated roles and why each was necessary;
- key competing hypotheses;
- unique evidence/findings per role;
- each counted role's mapping to a Goal Contract field, material unknown, or acceptance test;
- contradictions and discriminating tests;
- minority findings retained;
- synthesis/judgment with decisive evidence/crux;
- judge-bias checks used when material;
- roles not activated because marginal value was insufficient;
- whether runtime independence was actually observed or only logically simulated.

## Anti-Patterns

- homogeneous clones;
- majority vote without provenance;
- 29 approvers after one author;
- all roles sharing the same evidence path and calling that independent corroboration;
- early consensus treated as proof;
- judge reads vote totals before evidence and copies the plurality;
- rewarding the longest or most polished response;
- forced stance defense after decisive counterevidence;
- counting generic refusal/policy debate as task progress;
- using agents to satisfy headcount while producing no unique contribution;
- treating the Stop hook/controller as the new enemy or mission;
- lowering effort, agent count, tests, or acceptance criteria to escape a blocker;
- endless critique without tests;
- escalating role count after information gain has collapsed;
- treating verbosity, time spent, or role labels as depth/execution evidence.

## Evidence Note

Recent multi-agent evaluation research reports that sycophancy and social convergence can reduce debate reliability, and that multi-agent judging can amplify position, verbosity, chain-of-thought, and bandwagon biases. Treat these findings as design evidence, not as a guarantee that any single debiasing trick removes the problem. Bias checks should be benchmarked against simpler independent-judge baselines.
