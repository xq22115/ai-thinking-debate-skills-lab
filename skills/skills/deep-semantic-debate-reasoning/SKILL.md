---
name: deep-semantic-debate-reasoning
description: Analyze dense or adversarial language as layered meaning plus an argument graph; identify hinge premises, framing moves, burden shifts, pragmatic implications, dialogue-state changes, common-ground drift, and persuasion/comprehension gaps before rebutting, while separating rhetorical force from evidential strength.
---

# Deep Semantic Debate Reasoning

Version: `0.3.0-rc1`
Status: `EXPERIMENTAL / NOT HOST-LIVE VERIFIED`

## Objective

Increase reasoning quality when a short utterance may carry multiple relevant meanings or when debate structure matters. The skill must deepen interpretation without inventing hidden motives, improve rebuttal without rewarding sophistry, distinguish persuasion from comprehension, and maintain explicit shared dialogue state so later reasoning does not silently inherit false agreements.

This is a narrow specialist. It does not replace `task-goal-intelligence`, `evidence-gap-research`, `competing-hypotheses`, or `multi-agent-deliberation`.

## Trigger

Activate when at least one is material:

- a sentence has plausible literal + implied + strategic readings;
- definitions, categories, scope, or quantifiers control the dispute;
- a question may be reframing the original claim;
- burden of proof is contested or silently shifted;
- a debate contains multiple support/attack relations that linear summarization would flatten;
- the user asks for deep interpretation, cross-examination, rebuttal, steelmanning, or hidden assumptions;
- a persuasive argument looks stronger than its evidence warrants;
- participants converge on an answer while their underlying reasoning or causal models remain misaligned;
- later reasoning depends on whether a proposition was actually agreed, merely assumed, or left unresolved.

Do not activate for ordinary factual retrieval, mechanical tasks, or clear low-stakes prose where the extra structure cannot change the answer.

## 1. Utterance Stack

For each material sentence, extract only layers supported by text/context:

1. **EXPLICIT_PROPOSITION** — what is directly asserted or asked.
2. **PRESUPPOSITION** — what the utterance treats as already granted.
3. **IMPLICATURE** — what is reasonably suggested but not literally stated.
4. **FRAME** — which categories, definitions, comparison class, or decision boundary the wording selects.
5. **SCOPE** — quantifiers, exceptions, time window, population, and modality (`can`, `must`, `usually`, `always`).
6. **BURDEN_MOVE** — who is now expected to establish which proposition.
7. **SPEECH_ACT** — assertion, challenge, concession, clarification, dilemma, counterexample, bridge, or request for commitment.
8. **STRATEGIC_SETUP** — what later inference this move enables if accepted.
9. **UPDATE_CONDITION** — what evidence or counterexample would materially weaken the move.

Label uncertain layers as `HYPOTHESIS`, not fact. Do not infer private intent when discourse function is sufficient.

## 2. Claim Precision Gate

Before answering or rebutting, normalize the claim:

- separate descriptive, causal, definitional, predictive, and normative claims;
- resolve pronouns and comparison classes;
- distinguish `some`, `many`, `most`, and `all`;
- preserve the speaker's actual scope;
- distinguish a claim from an example offered for it;
- distinguish `X is compatible with Y` from `X proves Y`;
- identify whether the disputed word has multiple live definitions.

If two interpretations would produce materially different answers, keep both until context discriminates them.

## 3. Argument Graph

Represent the dispute as nodes and edges rather than a flat transcript.

Node types:
- claim;
- premise;
- evidence;
- definition;
- value/criterion;
- counterexample;
- concession;
- uncertainty.

Edge types:
- `SUPPORTS`;
- `ATTACKS`;
- `QUALIFIES`;
- `DEPENDS_ON`;
- `CONTRADICTS`;
- `REDEFINES`.

Find the **HINGE_PREMISE**: the smallest premise or definition whose change would cause the largest downstream verdict change. Test that before spending effort on peripheral points.

## 4. Dialogue-State Delta

A strong debate move is not just a sentence; it changes the conversational state. For each material move, track the delta across:

- **COMMITMENT_SET** — what each side is now committed to if the move is accepted;
- **ANSWER_SPACE** — which replies remain logically or rhetorically available;
- **BURDEN_VECTOR** — which side must establish which proposition next;
- **CRITERION_LOCK** — what metric, definition, or decision rule is now controlling the dispute;
- **CONCESSION_FRONTIER** — what can be granted without conceding the main conclusion;
- **EVIDENCE_GATE** — what kind of evidence is now required to advance the argument;
- **DOWNSTREAM_REACH** — how many later claims depend on this move.

Prefer moves with high discriminative value and low ambiguity. If a question merely narrows the opponent's rhetorical options without increasing truth-relevant information, treat that as a debate tactic rather than an epistemic gain.

## 5. Common-Ground Ledger

Do not let dialogue history become a vague narrative. Maintain a compact ledger when state matters:

- **AGREED** — explicitly accepted propositions;
- **DISPUTED** — propositions under active challenge;
- **UNRESOLVED** — raised but not settled;
- **ASSUMED_FOR_TEST** — temporarily granted for a consequence/counterfactual test;
- **WITHDRAWN** — explicitly retracted or superseded;
- **EVIDENCE_PENDING** — claims whose status depends on external verification.

Also preserve:

- commitments by participant;
- current burden holder for each material claim;
- open clarification questions;
- live competing hypotheses;
- current definitions/criteria and who accepted them;
- repair notes when an earlier interpretation was wrong.

Never promote `ASSUMED_FOR_TEST` or an unanswered presupposition into `AGREED`. If a later inference depends on a proposition whose status is unclear, repair the common ground before continuing.

## 6. Implicit-Premise Recovery

When an argument appears to jump from stated premise to conclusion, recover the missing bridge cautiously:

1. generate the smallest set of plausible implicit premises that would make the inference coherent;
2. rank them by textual/contextual fit, not by convenience for either side;
3. test each against known commitments, counterexamples, and source context;
4. preserve multiple candidates when evidence does not discriminate them;
5. if ambiguity is material, use an independent challenger to attack candidate premises rather than repeating the same generation.

Do **not** force an agent to defend an assigned stance after evidence moves against it. Stance commitment is not evidence; rhetorical rigidity can preserve a bad premise merely because the role prompt demands defense.

## 7. Critical-Question Selection

Generate questions broadly, but ask narrowly. A useful critical question should expose a reasoning gap or discriminate between live hypotheses.

For each candidate question, score qualitatively on:

- **HINGE_RELEVANCE** — does it test a premise with large downstream reach?
- **DISCRIMINATIVE_VALUE** — would materially different answers favor different hypotheses?
- **ANSWERABILITY** — can evidence or clarification realistically resolve it?
- **EVIDENCE_TARGETING** — does it point toward observable/source-checkable information?
- **FRAME_NEUTRALITY** — does it avoid smuggling the desired conclusion into the question?
- **COST** — is it cheaper/more decisive than another debate round?

Prefer the top 1–3 questions. Do not reward question volume. A question that cannot change the argument graph is usually decorative.

## 8. Cross-Examination Sequence

Prefer one decisive question over many decorative questions.

1. **Lock the proposition** — “Is the claim X, or the narrower Y?”
2. **Expose the hinge** — “Does the conclusion still follow if premise P is false?”
3. **Demand symmetry** — apply the same standard of evidence/definition/exceptions to both sides.
4. **Test boundary cases** — search for a case that separates rival definitions or causal stories.
5. **Ask the update question** — “What observation would change this conclusion?”
6. **Repair common ground** — “Did we actually agree to P, or were we only assuming P for this test?”

A question is useful only if possible answers change the argument graph or materially reduce uncertainty.

## 9. Debate Moves Worth Learning

Use these when truth-seeking value is positive:

- **Definition lock**: clarify a contested term before deriving consequences.
- **Scope correction**: narrow an exaggerated claim back to what was actually asserted.
- **Consequence test**: grant a premise temporarily and test whether its implications remain acceptable/consistent.
- **Category distinction**: separate two rules or domains that appear similar but have different governing criteria.
- **Counterexample probe**: use a discriminating example to test universality.
- **Internal-consistency test**: compare the current claim with another commitment under the same standard.
- **Burden symmetry**: prevent one side from demanding certainty while using weak evidence itself.
- **Steelman-before-attack**: rebut the strongest defensible version, not the easiest caricature.
- **Concession with boundary**: explicitly grant the valid portion while isolating what remains disputed.
- **Source challenge**: when a claim depends on text/history/data, inspect translation, provenance, sampling, or measurement rather than debating rhetoric alone.
- **Common-ground repair**: explicitly correct a mistaken shared assumption before it contaminates downstream reasoning.

## 10. Persuasion–Truth Firewall

Never treat the following as evidence of correctness:

- confidence;
- fluency;
- speed;
- applause or social dominance;
- repeated assertion;
- majority agreement without independent evidence;
- a rhetorically clean binary;
- a citation whose source quality/relevance has not been checked.

Score arguments by evidence, logical dependence, falsifiability, and robustness under counterexample — not by how forceful they sound.

### Comprehension–Persuasion Diagnostic

A model or speaker may be persuasive without understanding the structure it is discussing. Before crediting “good debate,” test whether it can:

- identify which premise actually supports which conclusion;
- name the target of a rebuttal rather than merely produce a counter-slogan;
- distinguish argument validity from factual truth of premises;
- state the strongest counterargument fairly;
- identify what evidence would update its position;
- preserve unresolved mechanism disagreement even when final answers match;
- distinguish genuinely shared commitments from merely assumed or rhetorically pressured commitments.

If persuasion rises while these structural diagnostics fail, classify the improvement as `RHETORICAL_GAIN`, not `REASONING_GAIN`.

### Confidence as Structured Metadata

Confidence must attach to a claim, evidence link, or inference step — not to the speaker's persona. Prefer calibrated confidence tied to provenance and uncertainty. A high-confidence weakly evidenced claim does not outrank a lower-confidence claim backed by direct reproducible evidence.

## 11. Anti-Sophistry Checks

Detect and correct rather than imitate:

- **QUESTION_SUBSTITUTION** — answering a different question because it is easier to win;
- **DEFINITIONAL_CAPTURE** — selecting a definition that smuggles in the desired conclusion;
- **FALSE_DICHOTOMY** — presenting two options when a material third state exists;
- **MOVING_GOALPOSTS** — changing the required proof after the original standard is met;
- **ASYMMETRIC_BURDEN** — one side must prove everything while the other side's assumptions are exempt;
- **EXAMPLE_TO_UNIVERSAL** — treating one vivid example as a universal rule;
- **MOTIVE_MINDREADING** — substituting speculative intent for what the text supports;
- **CONFIDENCE_SUBSTITUTION** — using certainty/tone as a proxy for evidence;
- **GISH_DENSITY** — accumulating more claims than can be independently checked and treating unanswered items as wins;
- **PROVENANCE_LAUNDERING** — using many citations, RAG snippets, or technical detail to manufacture credibility without checking relevance/quality;
- **FALLACY_FALLACY** — correctly identifying a bad argument and then incorrectly concluding that the proposition itself must be false;
- **FORCED_STANCE_RIGIDITY** — continuing to defend a role-assigned conclusion after its supporting premises collapse;
- **COMMON_GROUND_LAUNDERING** — treating an unchallenged assumption, temporary grant, or unanswered presupposition as if both sides explicitly agreed.

When a move is both rhetorically effective and epistemically weak, explicitly separate those two judgments. Detecting a fallacy weakens that route of support; it does not automatically refute the conclusion if another independent argument could support it.

## 12. Stepwise Critique

For complex reasoning, inspect material steps rather than only the final conclusion:

For each step ask:
- What does this step depend on?
- Is that premise evidenced, stipulated, implicit, or merely plausible?
- Is the inference deductive, inductive, abductive, or analogical?
- What is the strongest counterexample?
- Does the next step require a stronger claim than the previous step established?
- Is confidence calibrated to the quality of this particular step?
- Was the prerequisite proposition actually agreed, or merely assumed for testing?

Revise the earliest weak hinge first. Do not repeatedly “rethink” the entire answer when a local repair suffices.

## 13. Generalization Guard

Argument understanding must survive topic and wording changes. Before treating a benchmark gain as structural reasoning improvement:

- paraphrase content while preserving argument structure;
- swap domain vocabulary while keeping support/attack relations constant;
- test unseen topics and different discourse styles;
- check whether predictions collapse when lexical cues are removed;
- separate scheme/structure recognition from memorized dataset patterns.

A model that succeeds only on familiar lexical templates has learned a benchmark shortcut, not robust argument reasoning.

## 14. Debate-on-Demand Routing

Do not invoke a large council merely because the content is argumentative.

- one clear interpretation + strong evidence → single reasoner;
- two materially different readings → independent interpretation check;
- unresolved implicit premise → challenger compares candidate bridges;
- unresolved support/attack graph or high-impact dispute → adversarial review;
- persuasive-pressure risk → add evidence auditor / falsifier;
- same answer but incompatible rationales → preserve diversity until mechanism matters are resolved;
- common-ground drift → repair state before adding debate rounds;
- stop when another debate round adds less information than targeted evidence or a discriminating critical question.

Compose with `multi-agent-deliberation` only when distinct roles can contribute unique evidence/methods. Do not force consensus when a minority hypothesis remains better supported, and do not force agents to preserve assigned stances against evidence.

## 15. Output Contract

When this skill materially affects the answer, preserve internally or expose when useful:

- normalized claim(s);
- strongest alternative interpretation(s);
- hinge premise/definition;
- support/attack relationships;
- candidate implicit premise(s) when required;
- dialogue-state delta when it changes the dispute;
- common-ground status for material commitments;
- rhetorical move vs evidential value;
- calibrated confidence and provenance;
- highest-value critical question or decisive discriminator;
- conclusion with explicit uncertainty;
- what would change the conclusion.

Do not dump an exhaustive layer table when a concise answer is sufficient.

## Evaluation Invariants

- `IMPLICATURE != EXPLICIT_CLAIM`
- `PLAUSIBLE_INTENT != PROVEN_INTENT`
- `PERSUASION != TRUTH`
- `PERSUASION != COMPREHENSION`
- `DEFINITION != EVIDENCE`
- `CONSENSUS != REASONING_ALIGNMENT`
- `CONFIDENCE != EVIDENCE`
- `FALLACY_DETECTED != CONCLUSION_REFUTED`
- `RAG_OR_CITATIONS != PROVENANCE_QUALITY`
- `TEMPORARY_GRANT != AGREEMENT`
- `UNANSWERED_PRESUPPOSITION != COMMON_GROUND`
- `ASSIGNED_STANCE != EPISTEMIC_COMMITMENT`
- `MORE_QUESTIONS != BETTER_CROSS_EXAMINATION`
- `LEXICAL_MATCH != ARGUMENT_UNDERSTANDING`
- `REBUTTAL != QUESTION_SUBSTITUTION`
- `MORE_DEBATE != BETTER_REASONING`
- `DEPTH != VERBOSITY`

## Provenance / Research Basis

This skill was motivated by close analysis of adversarial public debate patterns (including Cambridge Union Q&A/debate footage, 19 May 2025) and cross-checked against recent work on graph-aware argumentation, pragmatic inference, implicit-premise recovery, critical-question generation/selection, common-ground tracking, stepwise natural-language self-critique, selective/evidence-weighted debate, calibrated confidence/diversity, fallacy robustness, progressive argument mining, generalization limits, and persuasion-driven failure modes.

Primary research links are maintained in `skills/03-2026-current-evidence.md`; this file contains portable reasoning rules rather than claims that a hosted model has been retrained.