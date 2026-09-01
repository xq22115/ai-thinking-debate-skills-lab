---
name: multi-agent-deliberation
description: Route complex tasks through a small active set of genuinely different roles, preserve useful disagreement, and scale toward larger councils only when marginal information gain or consequence justifies it.
---

# Multi-Agent Deliberation

Version: `0.1.2-rc1`

## Objective

Use multiple agents to increase epistemic and capability diversity, not to manufacture agreement, satisfy a numeric headcount, or simulate independent execution.

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
- unresolved obligation relevant to completion.

Compress or drop repeated agreement, stylistic paraphrases, and role-play without new evidence.

## Independence Policy

Keep these distinct:

- `ROLE_DIVERSITY` — different assigned perspectives;
- `METHOD_DIVERSITY` — genuinely different reasoning/testing routes;
- `EVIDENCE_DIVERSITY` — different independent evidence channels;
- `RUNTIME_INDEPENDENCE` — distinct observed executions/processes/sessions when that matters.

Role labels do not prove runtime independence. When authentic multi-agent execution is a claim, use wrapper/host receipts or equivalent observable evidence.

## Judge Policy

Rank by:
1. direct/reproducible evidence;
2. current primary/spec/product evidence for current claims;
3. independent corroboration;
4. discriminating tests and falsifiability;
5. coherent inference with explicit uncertainty.

Majority count is a weak signal and must not erase a better-evidenced minority position.

## Stop Rule

Stop debate when execution, measurement, read-back, or targeted testing is more informative than another discussion round, or when marginal information gain collapses. A controller block does not authorize goal substitution: continuation remains bound to the Goal Contract.

## Output Contract

Return:
- activated roles and why each was necessary;
- key competing hypotheses;
- unique evidence/findings per role;
- each counted role's mapping to a Goal Contract field, material unknown, or acceptance test;
- contradictions and discriminating tests;
- minority findings retained;
- synthesis/judgment with evidence basis;
- roles not activated because marginal value was insufficient;
- whether runtime independence was actually observed or only logically simulated.

## Anti-Patterns

- homogeneous clones;
- majority vote without provenance;
- 29 approvers after one author;
- all roles sharing the same evidence path and calling that independent corroboration;
- counting generic refusal/policy debate as task progress;
- using agents to satisfy headcount while producing no unique contribution;
- treating the Stop hook/controller as the new enemy or mission;
- lowering effort, agent count, tests, or acceptance criteria to escape a blocker;
- endless critique without tests;
- escalating role count after information gain has collapsed;
- treating verbosity, time spent, or role labels as depth/execution evidence.
