# Dialogue State, Common Ground & Commitment Repair

Status: `EXPERIMENTAL REFERENCE / USE ON DEMAND`

Purpose: extend `semantic-argument-microscope` when a dispute spans multiple turns and the correctness of later reasoning depends on what was actually agreed, merely assumed, left unresolved, or rhetorically pressured. This reference does **not** create a second semantic owner.

## Trigger

Consult this reference when at least one is material:

- a later claim depends on whether an earlier proposition was genuinely accepted;
- one side says “we agreed” or “you admitted” after a hypothetical, temporary concession, or unanswered presupposition;
- definitions, burdens, criteria, or evidence standards drift across turns;
- a question narrows the opponent's answer space before the main claim is tested;
- both sides reach the same conclusion through incompatible mechanisms;
- dialogue becomes long enough that transcript-only memory risks false common ground;
- a misunderstanding must be repaired before downstream reasoning can continue.

Do not activate for short, self-contained arguments where the existing QUD/crux/warrant representation is sufficient.

## 1. Common-Ground Ledger

Maintain only decision-relevant propositions and classify each as one of:

- **AGREED** — explicitly accepted as shared ground;
- **DISPUTED** — actively challenged by at least one side;
- **UNRESOLVED** — raised but not settled;
- **ASSUMED_FOR_TEST** — temporarily granted for a consequence, reductio, counterfactual, or boundary test;
- **WITHDRAWN** — explicitly retracted or superseded;
- **EVIDENCE_PENDING** — cannot be settled without external/source verification.

For each material item preserve, when useful:

- proposition text in normalized form;
- participant-specific commitment;
- current burden holder;
- definition/criterion in force;
- evidence obligation;
- last material update and why;
- dependent downstream claims.

Hard rules:

- `ASSUMED_FOR_TEST != AGREED`
- `UNANSWERED_PRESUPPOSITION != COMMON_GROUND`
- `SILENCE != ACCEPTANCE` unless the governing procedure explicitly makes it so
- `SHARED_CONCLUSION != SHARED_REASONING`
- `RHETORICAL_PRESSURE != VOLUNTARY_COMMITMENT`

If status is ambiguous and downstream reasoning depends on it, repair the state before continuing.

## 2. Dialogue-State Delta

Treat a consequential utterance as a state transition, not only a sentence. Track the smallest useful subset of:

- **COMMITMENT_SET** — what the move would commit each participant to;
- **ANSWER_SPACE** — which responses remain logically or rhetorically available;
- **BURDEN_VECTOR** — who must establish which proposition next;
- **CRITERION_LOCK** — which metric, definition, value rule, or decision threshold now controls the dispute;
- **CONCESSION_FRONTIER** — what can be granted without conceding the central conclusion;
- **EVIDENCE_GATE** — what kind of evidence is now required to advance the argument;
- **DOWNSTREAM_REACH** — how many important later claims depend on this state change.

A move may be tactically powerful while adding little epistemic information. Record those judgments separately.

### Example distinction

A question such as “Before discussing whether policy P works, can we agree that any policy costing more than last year is wasteful?” can:

- create a proposed `CRITERION_LOCK`;
- shrink `ANSWER_SPACE` if accepted;
- shift later `BURDEN_VECTOR` toward defending cost increases;
- increase `DOWNSTREAM_REACH` because many later claims inherit the criterion.

None of those effects make the proposed criterion true. The state change itself is not evidence for the premise.

## 3. Commitment Hygiene

Before using an earlier proposition as a premise, check its status.

### Temporary grants

If a speaker says `suppose P`, `grant P for the moment`, `even if P`, or equivalent, mark P as `ASSUMED_FOR_TEST` unless P is independently accepted.

A later move `you agreed P` is **temporary-grant laundering** unless explicit acceptance occurred.

### Presuppositions

Questions and formulations can presuppose propositions without proving them. Preserve the presupposition as a semantic fact about the utterance, not as established world evidence.

### Concessions

A bounded concession should record its scope. `P is true in benchmark B` does not imply `P is globally best`; `some X` does not imply `all X`.

### Definition agreement

Two speakers using the same word do not share a proposition until the governing definition/comparison class is aligned. Apparent consensus under incompatible definitions is `UNRESOLVED`.

## 4. Common-Ground Repair

When drift is detected:

1. identify the earliest proposition/definition whose state became ambiguous or corrupted;
2. mark downstream conclusions that depend on it as provisionally affected;
3. restate the competing interpretations or commitment states;
4. ask the smallest clarification needed to discriminate them, or inspect the transcript/source if available;
5. update the ledger;
6. recompute only affected downstream reasoning.

Do not restart the whole debate if a local repair suffices.

Recommended repair forms:

- “Did we accept P, or were we assuming P only for the consequence test?”
- “When you say efficient here, is the criterion cost, speed, or both?”
- “Are you withdrawing the earlier stronger claim, or narrowing it?”
- “Is this now a factual claim or a value criterion?”

## 5. Comprehension–Persuasion Diagnostic

A speaker/model can sound persuasive without correctly tracking dialogue structure. Before crediting a strong rebuttal, test whether it can:

- identify the actual premise or warrant being attacked;
- distinguish the live QUD from a neighboring question;
- recover current shared vs disputed commitments;
- distinguish temporary assumptions from agreement;
- state what evidence would update the relevant claim;
- preserve unresolved causal/mechanistic disagreement when final answers match.

If rhetorical effectiveness increases while these checks fail, classify the change as `RHETORICAL_GAIN`, not `REASONING_GAIN`.

## 6. Provenance Laundering

A long argument can create the appearance of evidential strength by accumulating citations, RAG snippets, technical vocabulary, or repeated source references.

Treat **provenance quality** separately from **provenance volume**. Check:

- direct relevance to the exact claim;
- primary vs derivative source status;
- independence vs copied/shared origin;
- measurement/design quality;
- context/translation/sampling fidelity;
- whether the cited source establishes the claimed magnitude/direction rather than an adjacent fact.

Hard rules:

- `CITATION_COUNT != EVIDENCE_STRENGTH`
- `RAG_RETRIEVAL != CLAIM_VERIFICATION`
- `SOURCE_PRESTIGE != DOMAIN_RELEVANCE`
- `TECHNICAL_DENSITY != PROVENANCE_QUALITY`

## 7. Structural Generalization Guard

Before treating semantic/argument performance as robust:

- paraphrase wording while preserving the same logical structure;
- swap topic/domain vocabulary while preserving support/attack/warrant relations;
- change rhetorical style while preserving the QUD/crux;
- remove familiar lexical cues;
- test whether common-ground states and relation labels remain stable.

A model that succeeds only on familiar words/templates has learned a benchmark shortcut, not portable argument understanding.

## 8. Interaction with Existing References

Use `ARGUMENT_SCHEMES.md` when the main problem is identifying the inferential scheme and ranking critical questions.

Use `CAUSAL_ABDUCTIVE_REASONING.md` when the crux is causal, explanatory, interventional, counterfactual, or mechanism selection.

Use this file when **dialogue history itself changes what propositions are available as premises**.

These references may compose, but load the smallest set that can change the verdict.

## Output Contract

When dialogue-state analysis materially matters, expose only what helps the decision:

- current QUD/crux;
- material ledger entries and their states;
- the state delta caused by the disputed move;
- any corrupted/ambiguous commitment requiring repair;
- affected downstream conclusion(s);
- decisive clarification/evidence test;
- epistemic conclusion vs rhetorical effect.

Do not dump the entire transcript into the ledger.

## Evaluation Invariants

- `TEMPORARY_GRANT != AGREEMENT`
- `UNANSWERED_PRESUPPOSITION != COMMON_GROUND`
- `SILENCE != ACCEPTANCE`
- `SHARED_CONCLUSION != SHARED_REASONING`
- `STATE_CHANGE != EVIDENCE`
- `PERSUASION != COMPREHENSION`
- `CITATIONS_OR_RAG != PROVENANCE_QUALITY`
- `LEXICAL_MATCH != ARGUMENT_UNDERSTANDING`

## Research Basis

This reference is informed by recent work on common ground / joint action in agentic dialogue, non-linear argument graphs, argument-relation mining, implicit-premise recovery, critical-question selection, persuasion-driven multi-agent failure, and cross-domain generalization limits in argument mining. Evidence links belong in the repository evidence log rather than being duplicated here.

## Invalidation Conditions

Re-evaluate or simplify this reference if:

- explicit ledger tracking adds cost without reducing state/commitment errors;
- transcript-native or host-native dialogue-state primitives make this representation redundant;
- a smaller QUD/crux/definition ledger performs equally well on long-dialogue holdouts;
- newer evidence shows the proposed state labels systematically distort natural dialogue;
- target-model tests fail to transfer under paraphrase/domain shift.