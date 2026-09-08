---
name: semantic-argument-microscope
description: Decompose important claims into literal meaning, hidden warrants, presuppositions, definitions, cruxes, evidence obligations, counterexamples, and rhetorical effects before accepting, rejecting, or debating them. Use for debates, ambiguous wording, contested claims, policy/ethics arguments, research synthesis, requirements, and any sentence where surface wording may hide multiple meanings.
---

# Semantic Argument Microscope

Version: `0.1.0-rc1`

Status: `EXPERIMENTAL / PORTABLE PROCEDURAL CORE`

## Objective

Increase reasoning quality by preventing surface-level agreement or rebuttal. Treat an important sentence as a compressed argument whose hidden structure must be reconstructed before it is judged.

This skill is not a political-position module and does not copy a speaker's conclusions. It extracts transferable reasoning techniques from adversarial dialogue while separating epistemic quality from rhetorical effectiveness.

## Trigger

Activate when one or more of these are true:

- a short sentence appears to carry multiple interpretations or unstated assumptions;
- two sides disagree but may be using different definitions, standards, scopes, or burdens of proof;
- an argument depends on a moral principle, analogy, authority, causal claim, or broad label;
- a factual assertion is decisive but vague, bundled, or weakly sourced;
- a debate is becoming rhetorical, circular, or frame-shifting;
- a user asks for deeper meaning, logic, argument quality, hidden assumptions, or debate analysis.

Do not activate for simple deterministic facts or wording where the extra decomposition has negligible decision value.

## Core Representation

For each decision-critical claim, reconstruct only the fields that materially matter:

1. **CLAIM** — What is literally being asserted?
2. **GROUNDS** — What evidence, observation, example, or premise is offered?
3. **WARRANT** — What unstated rule makes the grounds support the claim?
4. **PRESUPPOSITION** — What must already be assumed for the sentence to make sense?
5. **DEFINITION / SCOPE** — What key terms, quantifiers, time range, population, or comparison class are implied?
6. **CRUX** — Which proposition would most change the conclusion if false?
7. **EVIDENCE OBLIGATION** — What external evidence or discriminating test would resolve the crux?
8. **COUNTEREXAMPLE / EDGE CASE** — Does the stated principle survive a hard but relevant case?
9. **QUALIFIER** — How strong is the claim: always, usually, sometimes, likely, possible?
10. **REBUTTAL** — What is the strongest evidence-based objection?
11. **FRAME MOVE** — Did the speaker change definition, burden, scope, authority, or question?
12. **RHETORICAL EFFECT** — What audience effect is produced independently of truth value?

## Six-Layer Sentence Read

When deeper interpretation is useful, read the sentence through six layers:

- **L1 Literal:** what the words directly say.
- **L2 Logical:** premises, conclusion, dependency, quantifiers, causal direction.
- **L3 Hidden:** presuppositions, warrant, omitted alternatives, implied standard.
- **L4 Strategic:** what question the sentence forces the opponent to answer; what burden or frame it creates.
- **L5 Rhetorical:** compression, contrast, analogy, humor, moral loading, status move, audience targeting.
- **L6 Falsification:** what observation would make the sentence or its warrant materially weaker.

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

### 5. Crux lock

Prevent debate drift by maintaining a one-sentence live crux:

`The dispute currently turns on whether ______.`

A new point may replace the crux only if it has higher decision value. Record why the crux changed.

### 6. Burden and frame ledger

Track material shifts such as:

- claim becomes weaker/stronger;
- universal becomes existential or vice versa;
- factual claim becomes value claim;
- source standard changes;
- definition changes;
- burden of proof is transferred;
- answer substitutes a nearby question.

Do not call every clarification a fallacy. A frame shift is problematic only when it evades a material obligation or changes the proposition without acknowledgment.

### 7. Epistemic vs rhetorical score

Never equate a sharp comeback, applause line, confidence, speed, humor, or verbal dominance with correctness.

Score separately:

- **Epistemic:** evidence, validity, calibration, consistency, falsifiability, response to counterevidence.
- **Rhetorical:** clarity, compression, memorability, framing, emotional/audience effect.

A move can be rhetorically strong and epistemically weak, or the reverse.

## AI Reasoning Integration

### Before hypothesis generation

Use this skill to normalize the claim and expose hidden warrants. Then pass materially different interpretations to `competing-hypotheses` rather than allowing multiple agents to debate different questions unknowingly.

### Before multi-agent debate

Give agents the same current crux, definition ledger, and evidence obligations. Diversity should come from hypotheses/evidence/perspectives, not from accidental disagreement over wording.

### During critique

A critique counts as progress only if it adds at least one of:

- new evidence;
- new counterexample;
- new discriminating test;
- exposed hidden warrant;
- corrected definition/scope;
- material contradiction;
- calibrated confidence change.

Pure `reflect harder` loops with no new information do not count as independent verification.

### Before final synthesis

Reconstruct the strongest version of each surviving side, identify the decisive cruxes, and report unresolved uncertainty. Do not hide a weak evidence base behind rhetorical certainty.

## Argument Graph

For complex disputes, represent the argument as a small graph rather than a paragraph:

`grounds -> warrant -> claim`

Add edges for:

- `supports`
- `contradicts`
- `depends_on`
- `defines`
- `qualifies`
- `counterexample_to`
- `requires_evidence`

Merge nodes only when they are semantically equivalent. Preserve disagreements that rely on different warrants even when their surface conclusions match.

## Failure Modes

- **Mind-reading:** inferring hidden motives without evidence.
- **Fallacy hunting:** naming fallacies instead of testing whether the inference actually fails.
- **Analogy abuse:** treating emotional similarity as structural equivalence.
- **Gish-gallop imitation:** increasing point count faster than evidence can be checked.
- **Definition laundering:** silently changing what a key term means.
- **Burden escape:** replying to a weaker neighboring question.
- **Rhetoric-as-proof:** treating audience reaction or confidence as evidence.
- **Self-critique theater:** producing longer reflection without a new test, fact, or model delta.
- **False precision:** assigning numerical confidence without an evidence basis.

## Output Contract

For a high-value claim, return a compact analysis containing:

- normalized claim;
- strongest interpretation(s) if ambiguity is material;
- hidden warrant/presupposition;
- current crux;
- strongest supporting and contradicting evidence;
- decisive test or missing evidence;
- counterexample/edge-case result;
- frame shifts if any;
- epistemic assessment;
- rhetorical assessment only when useful;
- calibrated conclusion and remaining uncertainty.

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

### S5 — Moving crux
The speaker answers a neighboring issue and introduces three new claims.

Pass: preserve the original crux until it is answered or explicitly superseded.

### S6 — Pure self-reflection loop
A model critiques its answer repeatedly without new evidence or discriminating tests.

Pass: stop the loop and request/seek information that can change the decision.

## Research Basis

Portable concepts incorporated here include:

- Toulmin-style claim / grounds / warrant / qualifier / rebuttal decomposition;
- argument mapping and claim-evidence graphs;
- self-consistency and multi-path reasoning;
- Tree/Graph-of-Thought style branching when alternatives are materially different;
- multi-agent debate with evidence-based adjudication;
- evidence-grounded correction rather than unsupported intrinsic self-correction;
- diversity-aware oversight to reduce correlated errors.

These are mechanisms, not guarantees. Apply them only when they increase information gain relative to a simpler baseline.

## Portable Lesson

The deepest transferable debate skill is not `answer faster` or `attack harder`.

It is:

`surface wording -> hidden structure -> decisive crux -> discriminating evidence -> adversarial test -> calibrated conclusion`

A sentence becomes easier to reason about once the implicit bridge between its words and its conclusion is made explicit.

## Invalidation Conditions

Re-evaluate this skill if evidence shows that:

- the decomposition adds cost without improving error detection or decision quality;
- a simpler baseline performs equally well on the target task class;
- the host provides a stronger native argument/evidence representation;
- newer reasoning/debate studies materially reverse the current evidence on self-correction, diversity, or adjudication.
