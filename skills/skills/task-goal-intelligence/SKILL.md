---
name: task-goal-intelligence
description: Recover latent user intent, maintain a live goal belief graph, choose high-information observations, detect intent shifts, search long-tail evidence, and verify completion against the user's actual end state.
---

# Task Goal Intelligence

Version: `2.0.0`

## Trigger

Activate for any substantive task where misunderstanding the target, entity, constraints, hidden requirements, prior context, or completion condition could materially change the result. Escalate automatically for ambiguous, long-horizon, research-heavy, multi-tool, local-system, coding, planning, comparison, troubleshooting, or cross-chat tasks.

## Objective

Maximize **goal fidelity × information gain × verified completion**, not visible reasoning volume.

The skill must answer five questions before serious execution:

1. What outcome is the user actually trying to obtain?
2. Which exact entity/system/state owns that outcome?
3. What requirements are explicit, inferred, uncertain, or obsolete?
4. What observation would most reduce decision-critical uncertainty next?
5. What evidence would prove the requested end state is truly reached?

## Phase A — Recover the Goal Contract

Build:

- `ROOT_GOAL`
- `DESIRED_END_STATE`
- `HARD_CONSTRAINTS`
- `NEGATIONS`
- `PROTECTED_CAPABILITIES`
- `TARGET_IDENTITY`
- `UNDERLYING_PURPOSE`
- `PREFERENCE_PROFILE`
- `ACCEPTANCE_TESTS`
- `DECISION_CRITICAL_UNKNOWNS`
- `ASSUMPTION_LEDGER`

Use exact user wording and corrections as primary evidence, but do not stop there. Ground target identity against tools/runtime/repository/workspace evidence when available.

## Phase B — Build the Intent Belief Graph

Represent the working interpretation as a graph with evidence and confidence.

Nodes: outcomes, explicit requirements, inferred preferences, negative constraints, target entities, dependencies, causal owners, acceptance evidence, open unknowns, assumptions, obsolete constraints, provenance.

Edges: requires, supports, contradicts, depends_on, owned_by, verified_by, supersedes, derived_from.

Do not convert a low-confidence inferred preference into a hard requirement.

## Phase C — Candidate Goal Competition

If ambiguity can change the action, keep up to three materially different candidate goals.

Score candidates using:

- literal wording and corrections;
- durable context/preferences;
- environment/entity evidence;
- causal ownership;
- explicit constraint compatibility;
- acceptance coverage;
- underlying purpose;
- contradictions;
- unsupported assumption cost.

Eliminate candidates with evidence, not preference.

## Phase D — 10-Lens Target Lock

Primary five:

1. literal intent;
2. environment/entity identity;
3. acceptance evidence backward;
4. causal dependency owner;
5. reverse/failure model.

Escalation five:

6. counterfactual;
7. exclusion of neighboring targets;
8. cross-source consistency;
9. purpose/value fit;
10. latest-turn intent delta.

Distinctness matters more than count. Rephrasing the same argument is one lens.

## Phase E — Information-Gain Router

For each unresolved fact estimate:

`decision_value ≈ impact_if_wrong × uncertainty × discrimination_power / observation_cost`

Use this to choose the next tool call, search, inspection, test, or clarification.

Rules:

- prefer reliable tool/history/runtime evidence when it can resolve the ambiguity;
- never ask the user to repeat known information;
- clarification can occur at any phase;
- if clarification is necessary, ask one discriminating question rather than a broad request for clarification;
- stop researching an unknown once it can no longer change the decision or acceptance verdict.

## Phase F — Deep / Long-Tail Search

For research-heavy tasks activate 20+ materially different lanes as needed:

- canonical specification;
- repository source;
- configs/schemas/defaults;
- release/changelog history;
- commit archaeology;
- issues;
- PR discussions/reviews;
- tests/fixtures;
- benchmark methods/raw results;
- dataset cards/eval sets;
- papers/citation chaining;
- maintainer design comments;
- respected practitioner implementations;
- production postmortems;
- negative/failure evidence;
- reverted/abandoned approaches;
- migration/version conflicts;
- competing implementations;
- reverse search from errors/symbols/files;
- long-term reproducible user reports;
- prompt/config archaeology;
- package/release metadata;
- benchmark counterexamples/hidden-test-like cases;
- niche signals reached through citation, maintainer, commit, or dependency links.

Rare evidence is useful only when it changes the interpretation, resolves a contradiction, reveals an undocumented implementation detail, or exposes a failure mode. Obscurity is not authority.

## Phase G — Intent Shift Handling

On every new user message compute a semantic delta:

- refinement;
- correction;
- added constraint;
- priority change;
- target/entity change;
- route preference change;
- acceptance change;
- related-goal pivot;
- full task switch;
- restatement only.

Mark superseded constraints `OBSOLETE`. Do not let stale requirements survive because they appeared earlier in the conversation.

## Phase H — Plan Only After Convergence

A detailed plan may start only after sufficient convergence on root goal, target identity, hard constraints, protected capabilities, critical unknowns, and acceptance tests.

Every material step must map to a goal node, hard constraint, material unknown, or acceptance test. An unmapped step is a likely distraction.

## Phase I — Completion Audit

Before PASS, compare actual evidence against the original Goal Contract and current Intent Belief Graph.

Prefer an independent judge/reviewer when practical. Hard requirements have veto power. Self-report is never sufficient evidence of completion.

Measure:

- target identity verified;
- hard requirement coverage;
- acceptance-test coverage;
- protected capability preservation;
- unresolved assumption/contradiction count;
- stale-constraint violations;
- final drift check.

## User-Specific Operating Bias

When this skill is used for the current user's tasks:

- favor concise visible output but deep internal evidence gathering;
- recover relevant recent work before creating duplicate solutions;
- prioritize GitHub and Notion relevance probes when available;
- use Hugging Face/papers/datasets for behavioral and benchmark evidence when available;
- prefer respected maintainers, researchers, practitioners, real issues/PRs, postmortems, regressions, and negative evidence over marketing summaries;
- preserve requested capability rather than solving problems by silently removing features;
- treat repeated dissatisfaction as evidence that an earlier target assumption may be wrong; restart from the Goal Contract instead of patching the same interpretation.

## Output Contract

For substantive work, final reporting should expose only useful state, not hidden chain-of-thought:

- original target;
- material interpretation/correction made;
- what was actually completed;
- strongest evidence;
- acceptance status;
- unresolved blocker or uncertainty;
- one non-obvious finding when it can materially change the result.

## Anti-Patterns

- paraphrase the user once and call that understanding;
- plan before target/entity convergence;
- assume hidden intent as fact;
- ask broad clarification when tools can resolve it;
- ask the user to repeat known context;
- keep obsolete constraints active after a correction;
- search 20 synonyms and call that 20 methods;
- equate stars, popularity, or obscurity with truth;
- ignore negative evidence or reverted approaches;
- declare success from agent self-report;
- solve the wrong problem perfectly.
