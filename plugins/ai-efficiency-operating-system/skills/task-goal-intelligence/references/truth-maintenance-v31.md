# Truth Maintenance v3.1 — Native Progressive Reference

This reference preserves the current mainline Task Goal Intelligence v3.1 semantics inside the v4 native package without expanding the thin router back into a monolithic prompt.

The deterministic owner remains `control-plane/scripts/task_goal_state_engine.py`; this reference tells the runtime router when and how those semantics apply.

## Field-sensitive authority

Do not rank every signal on one global ladder. Authority depends on the field being changed.

- **Normative goal fields**: current explicit user request/correction owns root goal, desired end state, hard constraints, negations, protected capabilities, and acceptance tests.
- **Mutable factual fields**: current owning-system/runtime/repository read-back owns state, target identity, version, capability and other externally observable facts.
- **Preferences**: current explicit preference outranks older durable preference; preference ranks routes but does not manufacture facts.
- **Hypotheses/evidence**: retrieval, summaries, practitioner claims, model inference and experiments may change the causal model or route; they do not silently rewrite normative user intent.

A stale summary is cache, not authority. A weaker same-value source may corroborate an existing fact but cannot downgrade the authority of the active value. `RETRACT`/`OVERRIDE` must have sufficient authority for the field being changed.

Keep unresolved contradictions explicit rather than averaging them into false certainty.

## Assumption-based truth maintenance

Derived conclusions carry dependency edges to the premise(s) that support them.

When a valid correction, override, retract or fresh contradictory fact arrives:

1. identify the affected premise/goal/factual nodes;
2. verify field authority before mutation;
3. mark superseded nodes `OBSOLETE`;
4. invalidate dependent conclusions, route assumptions and completion claims;
5. preserve unaffected nodes/evidence;
6. recompute only the affected subgraph;
7. resume from the nearest still-valid native phase.

`EXAMPLE` and `DISTRACTOR` are non-binding. External evidence can falsify a route or causal assumption but cannot directly mutate normative goal fields.

## Structured uncertainty

Classify a material unknown before choosing who/what resolves it:

- `specification` → current task contract or one discriminating user clarification when genuinely needed;
- `target_identity` → owning repository/runtime identity read-back;
- `environment_state` → owning-runtime observation;
- `capability` → harmless executable capability probe;
- `evidence` → independent corroboration plus source grading;
- `model` → competing hypotheses, counterexamples, holdouts, fresh-context evaluator;
- `temporal` → fresh timestamped source or runtime read-back.

Do not ask the user for a fact the tools can observe directly. Do not let a tool-observed fact define what the user should want.

## Analysis of Competing Hypotheses

For high-impact ambiguity, use disconfirmation-first comparison rather than confirmation counting.

For each serious hypothesis record support, contradiction/inconsistency, unknown/neutral evidence and required assumptions. Strong independent contradiction can outweigh many weak confirming anecdotes. Actively formulate the strongest opposite hypothesis and seek the observation most likely to distinguish the candidates.

The goal is not a formal numeric score; it is to prevent confirmation-heavy evidence collection from locking the first plausible interpretation.

## Counterexample-guided refinement

A failed acceptance test or direct user correction is a counterexample to the current model/route.

On a counterexample:

1. keep the root goal unless the user semantically changed it;
2. mark the failed acceptance criterion unsatisfied;
3. invalidate route assumptions that predicted PASS;
4. find the smallest faulty assumption or abstraction;
5. refine that component rather than weakening success criteria;
6. rerun the discriminating acceptance test.

Never convert a counterexample into permission to delete required capability, workload, verification, effort or scope.

## Requirements traceability + metamorphic goal tests

Maintain bidirectional traceability:

`source user signal → normalized requirement → action/route → observable acceptance test → current evidence`

Every hard requirement has source provenance and a verification path. Every material action maps to a requirement, decision-critical unknown, hypothesis test or acceptance test. Orphan actions are probable non-progress.

Metamorphic invariants include:

- reordering examples/distractors does not change the root goal;
- equivalent paraphrases preserve hard constraints and acceptance coverage;
- naming a tool as an example does not make it the sole route;
- low-authority retrieved material cannot override a current user correction;
- mutable runtime state can change without rewriting normative end state;
- explicit correction/override/retract/target/acceptance changes do change the affected goal state.

## Source grading

Grade source reliability separately from information credibility. Opaque/anonymous/underground/onion/dark-web-linked evidence remains `LEAD` until corroborated/reproduced/owning-source verified. Derivative mirrors of one claim are not independent evidence.

Rare evidence can materially change a hypothesis when it is reproducible and discriminating; rarity alone never gives it normative authority over the user's goal.

## Native integration

The v4 phase machine uses these semantics as follows:

- `ORIENT`: field authority, stale-summary suppression, dependency invalidation;
- `DISCRIMINATE`: structured uncertainty + Analysis of Competing Hypotheses;
- `COMMIT`: traceability and nearest-easier-task exclusion;
- `EXECUTE`: dependency-aware state/progress updates;
- `VERIFY`: counterexamples and bidirectional acceptance trace;
- `RECOVER`: invalidate failed route assumptions and repair first upstream failure;
- `LEARN`: metamorphic/behavioral failures become candidate eval cases.
