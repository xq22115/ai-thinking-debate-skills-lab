---
name: multi-agent-deliberation
description: Route complex tasks through a small active set of genuinely different roles, preserve useful disagreement, and scale toward larger councils only when marginal information gain or consequence justifies it.
---

# Multi-Agent Deliberation

Version: `0.1.1-rc1`

## Objective

Use multiple agents to increase epistemic and capability diversity, not to manufacture agreement or simulate independent execution.

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

Stop debate when execution, measurement, read-back, or targeted testing is more informative than another discussion round, or when marginal information gain collapses.

## Output Contract

Return:
- activated roles and why each was necessary;
- key competing hypotheses;
- unique evidence/findings per role;
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
- endless critique without tests;
- escalating role count after information gain has collapsed;
- treating verbosity, time spent, or role labels as depth/execution evidence.
