# Formal Dialectical Reasoning

Status: `EXPERIMENTAL REFERENCE / DEMAND-LOADED`

Purpose: provide a conservative formal layer for disputes whose verdict depends on attack type, cycles, collective premises, preference-sensitive defeat, incomplete information, or belief revision. It supplements `SKILL.md`; it is not a second semantic owner.

## Core invariants

- `ATTACK != DEFEAT`
- `UNKNOWN != FALSE`
- `SOLVER_CORRECTNESS != PARSER_CORRECTNESS`
- `UNCERTAINTY MUST PROPAGATE`
- `SALIENT_DISAGREEMENT != DECISION_CRUX`
- `GENERATED_REASONING != COMMITTABLE_BELIEF`
- `PERSUASION != FORMAL_ARGUMENT_STRENGTH`
- `MODEL_DIVERSITY != ARGUMENT_DIVERSITY`

## Routing gate

Use this layer only when at least one is material:

- cycles or mutually defeating arguments;
- an attack targets a premise, inference rule, or conclusion differently;
- two or more premises must jointly support/attack a claim;
- preferences/evidence quality determine whether an attack succeeds as a defeat;
- missing premises or uncertain warrants would otherwise be forced into binary truth values;
- the decision requires a stable `IN / OUT / UNDEC` representation;
- the user needs to know what minimal change would flip the verdict.

Do not load it merely because a disagreement exists. For a self-contained premise attack with no cycles, no preference interaction, and no uncertainty propagation, prefer the lighter semantic path.

## Structured argument object

Represent decision-critical arguments as:

- `premises` — explicit, implicit, or temporarily assumed propositions;
- `rule / warrant` — strict or defeasible bridge from premises to conclusion;
- `intermediate conclusions` — reusable derived propositions;
- `final conclusion` — proposition being defended or rejected;
- `provenance` — text span, source/evidence lineage, parser confidence;
- `scope` — QUD, domain, time/population, and concession locality.

Do not treat a whole paragraph as an indivisible argument when attack location matters.

## Typed attacks

Use three minimum attack types:

1. `UNDERMINE` — attacks a premise.
2. `UNDERCUT` — attacks the inference/warrant connecting premise to conclusion.
3. `REBUT` — attacks an incompatible conclusion.

A candidate attack becomes a `DEFEAT` only after preference/evidence/value rules permit it. Preserve suppressed attacks for audit; never silently delete them from provenance.

## Collective support and attack

Some relations are conjunctive rather than pairwise:

`{P1, P2, ... Pn} -> C`

If all members are required, do not convert the set into several independent supports. The default three-state propagation is:

- all required premises and the warrant `SUPPORTED` -> conclusion support `SUPPORTED`;
- any required premise or warrant `REJECTED` -> that support route `REJECTED`;
- otherwise at least one required component `UNKNOWN` -> route `UNKNOWN`.

This prevents missing information from being treated as a counterexample.

## Conservative acceptability

When a formal extension is needed, use grounded semantics as the conservative default:

- `IN` — defended under the current effective defeat graph;
- `OUT` — defeated by an `IN` argument;
- `UNDEC` — neither defensibly accepted nor rejected under the current graph.

A bare two-cycle with no external defender remains `UNDEC / UNDEC`. Do not invent a winner from recency, fluency, agent identity, or rhetorical confidence.

Use preferred/stable/value-based or gradual semantics only when the decision actually depends on alternative extensions, audience/value priorities, or graded relation strength. Record the reason for leaving grounded semantics.

## Parser confidence is separate from solver validity

Natural-language extraction creates candidate graph objects. Each decision-critical node/edge should carry:

- `parser_state`: `CANDIDATE / CROSS_CHECKED / ACCEPTED / REJECTED`;
- supporting text span or source pointer;
- semantic interpretation confidence;
- alternative plausible relation when ambiguity is material.

Do not let a mathematically correct solver create false confidence in a misparsed graph. For high-impact edges, perturb the parser hypothesis (`rebut` vs `undercut`, pairwise vs collective, asserted vs hypothetical) and check whether the verdict changes.

## Edge-level warrant uncertainty

Treat the warrant as a first-class relation object. If premises are supported but the warrant is unresolved, the derived support remains unresolved. Do not hide warrant uncertainty inside a final scalar confidence.

Prefer ordinal or interval-like states when evidence does not justify precise probabilities. Numeric weights require an explicit empirical or decision-theoretic basis.

## Verdict sensitivity and flip sets

Separate the point receiving the most conversational attention from the point that can actually change the decision.

For each candidate hinge, ask:

`remove / weaken / strengthen X -> does target verdict change?`

A `MINIMAL_VERDICT_FLIP_SET` is the smallest tested set of premises, warrants, attacks, or preference assumptions whose change flips the target label or materially changes recommendation strength.

Use this to rank follow-up evidence obligations. A loud disagreement with zero verdict sensitivity is not the primary decision crux.

## Belief revision and commit gate

New evidence should trigger bounded recomputation:

`evidence delta -> directly affected belief -> downstream dependents -> verdict/crux`

Keep unrelated beliefs unchanged unless a shared dependency is exposed. Flag:

- `UNDER_REVISION` — valid defeating evidence arrives but the affected belief stays fixed;
- `OVER_REVISION` — local evidence causes unrelated beliefs to change;
- `ILLEGAL_PROMOTION` — a hypothesis, temporary assumption, or unresolved claim is written back as established fact.
