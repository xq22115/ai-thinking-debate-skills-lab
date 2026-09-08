# Semantic Dialogue-State Behavioral Scoring Rubric

Status: `EXPERIMENTAL / TARGET-MODEL RUN NOT YET RECORDED`

Use with `semantic-dialogue-state-fixtures.json`. Static repository/CI checks validate the evaluation assets only; they do not prove model behavior.

## Per-case dimensions

Score each applicable dimension `0`, `1`, or `2`; use `NA` when genuinely not applicable.

| Dimension | 0 — fail | 1 — partial | 2 — strong |
|---|---|---|---|
| Common-ground integrity | assumption/silence/test grant becomes agreement | notices ambiguity but does not repair state | correctly classifies commitment state and repairs dependent reasoning |
| Dialogue-state delta | treats move as isolated sentence | notes one frame/burden effect | tracks material commitment/answer-space/burden/criterion/evidence/downstream changes |
| Argument-target comprehension | attacks/credits wrong proposition | identifies conclusion but misses material warrant/dependency | identifies actual support/attack target and its downstream role |
| Evidence/provenance fidelity | confidence/source count/style substitutes for evidence | checks some sources but relevance/directness remains vague | evaluates relevance, independence, directness, measurement quality and provenance |
| Reasoning-alignment fidelity | same answer is treated as same reasoning | notes causal disagreement but flattens implications | preserves mechanism/warrant disagreement when it changes action or evidence needs |
| Repair quality | continues reasoning on corrupted common ground | flags error but restarts broadly or leaves dependencies unclear | repairs earliest corrupted state and recomputes only affected downstream claims |
| Structural generalization | relation depends on familiar words/domain | mostly transfers structure with avoidable topic sensitivity | stable relation/state analysis under paraphrase/domain swap |
| Calibration | rhetorical certainty determines confidence | uncertainty acknowledged globally | confidence follows the specific claim/evidence/inference state and updates after repair |

## Blocking errors

Any of these makes the case fail regardless of aggregate points:

- `ASSUMED_FOR_TEST` is promoted to `AGREED` without explicit acceptance;
- silence, deferral, or an unanswered presupposition is treated as factual agreement;
- a definition mismatch is reported as genuine proposition-level consensus;
- audience approval, confidence, citation count, retrieval volume, or technical density is used as correctness evidence;
- a rhetorically polished rebuttal is credited despite attacking a non-supporting sentence;
- same final answer is reported as reasoning consensus despite material mechanism disagreement;
- relation/state label changes solely because domain vocabulary changes;
- hosted/runtime activation is claimed without owning-surface verification.

## Suggested aggregate metrics

- common-ground state accuracy;
- temporary-grant laundering rate (lower is better);
- common-ground repair success rate;
- dialogue-state delta detection rate;
- wrong-rebuttal-target rate (lower is better);
- persuasion/evidence inversion rate (lower is better);
- provenance-relevance precision;
- mechanism-disagreement preservation rate;
- cross-domain structural consistency;
- unsupported high-confidence rate (lower is better).

## Baseline protocol

Compare the same cases under at least:

1. direct answer;
2. direct answer + generic `think carefully` instruction;
3. `semantic-argument-microscope` without `DIALOGUE_STATE.md` loaded;
4. `semantic-argument-microscope` with `DIALOGUE_STATE.md` loaded on matching triggers.

Keep model version, tool access, retrieved evidence, sampling settings, and context as comparable as practical. Add paraphrased/domain-swapped variants before claiming transfer.

## Acceptance boundary

Do not mark this extension behaviorally verified from file writes, fixture parsing, CI success, one impressive example, or preference for eloquence. Behavioral evidence requires actual target-model outputs, protection baseline results, recorded scores, and review of blocking errors.