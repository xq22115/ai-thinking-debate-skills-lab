---
name: semantic-argument-microscope
description: Decompose important claims into literal meaning, hidden warrants, presuppositions, definitions, cruxes, evidence obligations, counterexamples, pragmatic implications, and rhetorical effects before accepting, rejecting, or debating them. Use for debates, ambiguous wording, contested claims, policy/ethics arguments, research synthesis, requirements, and any sentence where surface wording may hide multiple meanings.
---

# Semantic Argument Microscope

Version: `0.2.0-rc1`

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Objective

Increase reasoning quality by preventing both surface-level interpretation and unsupported over-interpretation. Treat an important sentence as a compressed argument whose hidden structure may need reconstruction before it is judged, while preserving a strict boundary between what is explicit, pragmatically supported, merely plausible, and unsupported.

This skill is not a political-position module and does not copy a speaker's conclusions. It extracts transferable reasoning techniques from adversarial dialogue while separating epistemic quality from rhetorical effectiveness.

## Trigger

Activate when one or more of these are true:

- a short sentence appears to carry multiple interpretations or unstated assumptions;
- two sides disagree but may be using different definitions, standards, scopes, questions, or burdens of proof;
- an argument depends on a moral principle, analogy, authority, causal claim, implicature, presupposition, or broad label;
- a factual assertion is decisive but vague, bundled, or weakly sourced;
- a debate is becoming rhetorical, circular, frame-shifting, or stance-locked;
- a user asks for deeper meaning, logic, argument quality, hidden assumptions, or debate analysis.

Do not activate for simple deterministic facts or wording where the extra decomposition has negligible decision value.

## Core Representation

For each decision-critical claim, reconstruct only the fields that materially matter:

1. **CLAIM** — What is literally being asserted?
2. **GROUNDS** — What evidence, observation, example, or premise is offered?
3. **WARRANT** — What unstated rule makes the grounds support the claim?
4. **PRESUPPOSITION** — What must already be assumed for the sentence to make sense?
5. **IMPLICATURE** — What additional meaning may be pragmatically conveyed without being literally asserted?
6. **DEFINITION / SCOPE** — What key terms, quantifiers, time range, population, or comparison class are implied?
7. **QUD** — What Question Under Discussion is the sentence actually answering?
8. **CRUX** — Which proposition would most change the conclusion if false?
9. **EVIDENCE OBLIGATION** — What external evidence or discriminating test would resolve the crux?
10. **COUNTEREXAMPLE / EDGE CASE** — Does the stated principle survive a hard but relevant case?
11. **QUALIFIER** — How strong is the claim: always, usually, sometimes, likely, possible?
12. **REBUTTAL** — What is the strongest evidence-based objection?
13. **FRAME MOVE** — Did the speaker change definition, burden, scope, authority, question, or evidentiary standard?
14. **RHETORICAL EFFECT** — What audience effect is produced independently of truth value?

## Interpretation Confidence Ladder

Every non-literal interpretation must be assigned one of four states:

- **EXPLICIT** — directly asserted by the words in context.
- **STRONGLY_LICENSED** — not literal, but strongly supported by conventional pragmatics and the immediate context.
- **PLAUSIBLE** — one reasonable interpretation among multiple live alternatives.
- **UNSUPPORTED** — requires motive-reading, missing context, or assumptions not licensed by the evidence.

Rules:

1. Never silently promote `PLAUSIBLE` to `EXPLICIT`.
2. A presupposition or implicature is not automatically a factual commitment by the speaker.
3. For `STRONGLY_LICENSED` or `PLAUSIBLE`, identify the contextual cue and at least one viable alternative interpretation when material.
4. If the same surface sentence changes meaning under a small context change, treat context as causal evidence rather than treating the words alone as sufficient.
5. Prefer `uncertain` over inventing a hidden meaning when contextual support is weak.

## Seven-Layer Sentence Read

When deeper interpretation is useful, read the sentence through seven layers:

- **L1 Literal:** what the words directly say.
- **L2 Logical:** premises, conclusion, dependency, quantifiers, causal direction.
- **L3 Pragmatic:** implicature, presupposition, reference, deixis, Question Under Discussion.
- **L4 Hidden:** warrant, omitted alternatives, implied standard, defeasible assumptions.
- **L5 Strategic:** what question the sentence forces the opponent to answer; what burden or frame it creates.
- **L6 Rhetorical:** compression, contrast, analogy, humor, moral loading, status move, audience targeting.
- **L7 Falsification:** what observation would make the sentence, warrant, or pragmatic interpretation materially weaker.

Do not invent hidden motives. Strategic/rhetorical interpretations must be labeled as hypotheses unless directly supported by context.

## Debate-Derived Reasoning Patterns

### 1. Principle extraction

When an opponent gives a conclusion, ask what general rule produces it. Move from `position` to `criterion`.

Then test whether the same criterion is applied consistently elsewhere.

### 2. Counterexample stress test

Construct the strongest relevant edge case for the stated rule. A useful counterexample tests the governing principle, not a cosmetic similarity.

After using an analogy, explicitly check both:

- relevant similarities that make the analogy informative;
- relevant dissimilarities that may break it.

### 3. Broad-label decomposition

If a speaker says an actor, policy, system, or idea is simply `good`, `bad`, `corrupt`, `safe`, `harmful`, `successful`, or similar, require decomposition into concrete propositions.

Ask for the highest-impact reason first, then turn it into a falsifiable claim.

### 4. Interpretation-rule exposure

When disagreement is about a text, rule, metric, precedent, or authority, identify the governing interpretation method before arguing isolated examples.

Separate:

- source text;
- translation/measurement uncertainty;
- interpretive rule;
- authority hierarchy;
- application to the present claim.

### 5. Question-under-discussion lock

Track the live Question Under Discussion (`QUD`) separately from the speaker's latest sentence.

Classify each response as:

- `DIRECTLY_ANSWERS_QUD`
- `PARTIALLY_ANSWERS_QUD`
- `REFRAMES_QUD_WITH_ACKNOWLEDGMENT`
- `CHANGES_QUD_WITHOUT_RESOLVING`
- `IRRELEVANT_TO_QUD`

A rhetorically effective answer to a neighboring question does not resolve the original QUD.

### 6. Crux lock

Prevent debate drift by maintaining a one-sentence live crux:

`The dispute currently turns on whether ______.`

A new point may replace the crux only if it has higher decision value. Record why the crux changed.

### 7. Burden and frame ledger

Track material shifts such as:

- claim becomes weaker/stronger;
- universal becomes existential or vice versa;
- factual claim becomes value claim;
- source standard changes;
- definition changes;
- burden of proof is transferred;
- answer substitutes a nearby question.

The stronger or more consequential the claim, the stronger the evidence obligation generally becomes. Do not weaponize `burden of proof` as a way to ignore available contrary evidence; track obligations on all decision-critical claims.

Do not call every clarification a fallacy. A frame shift is problematic only when it evades a material obligation or changes the proposition without acknowledgment.

### 8. Defeasible reasoning and belief revision

Treat many real-world conclusions as defeasible rather than monotonic: a conclusion can be reasonable under current evidence and later lose support when an exception, defeating condition, or stronger source appears.

Maintain:

- current conclusion;
- supporting warrant;
- known exceptions/defeaters;
- evidence that would raise or lower confidence;
- last material update and why it changed the state.

When new evidence arrives, update the claim/warrant/confidence. Do not preserve an earlier conclusion merely for consistency with a previous turn.

### 9. Stance freedom

Debate roles are hypothesis generators and falsifiers, not identities to defend.

Rules:

- any agent may abandon its initial hypothesis after decisive counterevidence;
- a forced pro/con stance may be used as a temporary stress test, but not as evidence of the agent's belief;
- adjudication should reward accurate revision, not rhetorical persistence;
- repeated defense of a defeated premise is a failure mode, not `strong debate`.

### 10. Epistemic vs rhetorical score

Never equate a sharp comeback, applause line, confidence, speed, humor, or verbal dominance with correctness.

Score separately:

- **Epistemic:** evidence, validity, calibration, consistency, falsifiability, response to counterevidence.
- **Rhetorical:** clarity, compression, memorability, framing, emotional/audience effect.

A move can be rhetorically strong and epistemically weak, or the reverse.

## AI Reasoning Integration

### Before hypothesis generation

Use this skill to normalize the claim, identify the active QUD, expose hidden warrants, and classify pragmatic interpretations by confidence. Then pass materially different interpretations to `competing-hypotheses` rather than allowing multiple agents to debate different questions unknowingly.

### Before multi-agent debate

Give agents the same current QUD, crux, definition ledger, interpretation-confidence state, and evidence obligations. Diversity should come from hypotheses/evidence/perspectives, not from accidental disagreement over wording.

Do not permanently assign agents to defend a stance. If stance assignment is used for stress testing, explicitly restore revision freedom before adjudication.

### During critique

A critique counts as progress only if it adds at least one of:

- new evidence;
- new counterexample or defeater;
- new discriminating test;
- exposed hidden warrant;
- corrected pragmatic interpretation;
- corrected definition/scope/QUD;
- material contradiction;
- calibrated confidence change.

Pure `reflect harder` loops with no new information do not count as independent verification.

### During evidence update

After decision-relevant evidence, recompute rather than merely append commentary:

`claim state -> warrant state -> defeaters -> confidence -> crux -> next discriminating test`

A confidence change without an identified evidence delta is not a valid belief update.

### Before final synthesis

Reconstruct the strongest version of each surviving side, identify the decisive cruxes, distinguish literal from pragmatic claims, and report unresolved uncertainty. Do not hide a weak evidence base behind rhetorical certainty.

## Argument Graph

For complex disputes, represent the argument as a small graph rather than a paragraph:

`grounds -> warrant -> claim`

Add edges for:

- `supports`
- `contradicts`
- `depends_on`
- `presupposes`
- `implicates`
- `defines`
- `qualifies`
- `defeats`
- `counterexample_to`
- `answers_qud`
- `requires_evidence`

Merge nodes only when they are semantically equivalent. Preserve disagreements that rely on different warrants even when their surface conclusions match.

## Failure Modes

- **Mind-reading:** inferring hidden motives without evidence.
- **Pragmatic hallucination:** converting a plausible implied meaning into a factual assertion without sufficient contextual support.
- **Literalism:** ignoring strongly licensed context-dependent meaning.
- **QUD substitution:** answering a nearby question while leaving the original unresolved.
- **Fallacy hunting:** naming fallacies instead of testing whether the inference actually fails.
- **Analogy abuse:** treating emotional similarity as structural equivalence.
- **Gish-gallop imitation:** increasing point count faster than evidence can be checked.
- **Definition laundering:** silently changing what a key term means.
- **Burden escape:** replying to a weaker neighboring question.
- **Stance lock:** defending an assigned position after its warrant has been defeated.
- **Rhetoric-as-proof:** treating audience reaction or confidence as evidence.
- **Self-critique theater:** producing longer reflection without a new test, fact, or model delta.
- **False precision:** assigning numerical confidence without an evidence basis.
- **Monotonicity error:** refusing to revise a conclusion when a legitimate defeater appears.

## Output Contract

For a high-value claim, return a compact analysis containing:

- normalized literal claim;
- pragmatic interpretation(s) with confidence state;
- active Question Under Discussion;
- strongest interpretation(s) if ambiguity is material;
- hidden warrant/presupposition;
- current crux;
- strongest supporting and contradicting evidence;
- known defeaters/exceptions;
- decisive test or missing evidence;
- counterexample/edge-case result;
- frame/burden shifts if any;
- epistemic assessment;
- rhetorical assessment only when useful;
- calibrated conclusion, update reason, and remaining uncertainty.

Do not expose private chain-of-thought. Provide concise, auditable reasoning summaries and evidence instead.

## Evaluation Fixtures

### S1 — Same words, different definitions
Two parties use the same key term with incompatible definitions.

Pass: detect the mismatch before choosing a side.

### S2 — Hidden warrant failure
The stated evidence is true but supports the conclusion only through a contestable unstated rule.

Pass: surface and test the warrant.

### S3 — Rhetorical knockout, weak evidence
One response is memorable and forceful but does not answer the factual crux.

Pass: high rhetorical score does not raise epistemic score.

### S4 — Valid counterexample vs cheap analogy
Present one edge case that genuinely violates the claimed universal rule and one that only looks similar.

Pass: distinguish them by relevant structural properties.

### S5 — Moving crux / QUD substitution
The speaker answers a neighboring issue and introduces three new claims.

Pass: preserve the original QUD/crux until it is answered or explicitly superseded.

### S6 — Pure self-reflection loop
A model critiques its answer repeatedly without new evidence or discriminating tests.

Pass: stop the loop and request/seek information that can change the decision.

### S7 — Pragmatic hallucination
The same sentence appears in two contexts, only one of which licenses the implied meaning.

Pass: infer the implication only in the supporting context; otherwise mark it plausible/unsupported rather than factual.

### S8 — Presupposition is not assertion
A sentence presupposes a proposition without directly arguing for it.

Pass: record the presupposition but do not count it as independently established evidence.

### S9 — Defeater update
A conclusion is initially reasonable, then a valid exception arrives.

Pass: revise the conclusion/warrant/confidence and name the defeating evidence.

### S10 — Assigned-stance rigidity
Two agents are assigned opposing positions; one receives decisive counterevidence against its assigned side.

Pass: the agent is allowed and expected to update rather than continue defending the assignment.

### S11 — Stronger claim, stronger obligation
A speaker escalates from `some` to `all` or from `possible` to `certain` without new evidence.

Pass: detect the increased evidence burden and downgrade calibration if unsupported.

### S12 — Generation/inference asymmetry
A model can invent several contexts where an implication would make sense, but the observed context does not select one of them.

Pass: do not treat generative plausibility as evidence that the implication is present in the actual case.

## Research Basis

Portable concepts incorporated here include:

- Toulmin-style claim / grounds / warrant / qualifier / rebuttal decomposition;
- argument-reasoning and implicit-warrant reconstruction;
- pragmatics: implicature, presupposition, reference/deixis, alternatives, and Question Under Discussion;
- context-sensitive interpretation with explicit anti-overinterpretation controls;
- argument mapping and claim-evidence graphs;
- defeasible / non-monotonic reasoning and evidence-driven belief revision;
- self-consistency and multi-path reasoning;
- Tree/Graph-of-Thought style branching when alternatives are materially different;
- multi-agent debate with evidence-based adjudication and revision freedom;
- evidence-grounded correction rather than unsupported intrinsic self-correction;
- diversity-aware oversight to reduce correlated errors and conformity.

These are mechanisms, not guarantees. Apply them only when they increase information gain relative to a simpler baseline.

## Portable Lesson

The deepest transferable debate skill is not `answer faster`, `attack harder`, or `always find a deeper hidden meaning`.

It is:

`surface wording -> literal/pragmatic boundary -> hidden structure -> active QUD -> decisive crux -> discriminating evidence -> defeater test -> calibrated revision`

A sentence becomes easier to reason about once the implicit bridge between its words and its conclusion is made explicit — and once unsupported bridges are rejected rather than imagined.

## Invalidation Conditions

Re-evaluate this skill if evidence shows that:

- the decomposition adds cost without improving error detection or decision quality;
- a simpler baseline performs equally well on the target task class;
- the interpretation-confidence ladder systematically suppresses valid pragmatic inference;
- the host provides a stronger native argument/evidence representation;
- newer reasoning/debate/pragmatics studies materially reverse the current evidence on self-correction, pragmatic inference, diversity, stance assignment, or adjudication.
