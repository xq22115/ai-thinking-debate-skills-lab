# Semantic Dialogue-State Behavioral Scoring Rubric

Status: `EXPERIMENTAL / TARGET-MODEL RUN NOT YET RECORDED`

Use with both:

- `semantic-dialogue-state-fixtures.json` — target DS1–DS8 capability cases;
- `semantic-dialogue-state-protection-fixtures.json` — DSP1–DSP12 protection holdout for neighboring semantic/argument/causal capabilities.

Static repository/CI checks validate evaluation assets only; they do not prove model behavior.

## Per-case dimensions

Score each applicable dimension `0`, `1`, or `2`; use `NA` when genuinely not applicable.

| Dimension | 0 — fail | 1 — partial | 2 — strong |
|---|---|---|---|
| Common-ground integrity | assumption/silence/test grant becomes agreement, or shared state is invented where none exists | notices ambiguity but does not repair/limit state | correctly classifies commitment state when material and avoids inventing it when not material |
| Dialogue-state delta | treats material state change as isolated sentence, or fabricates a state delta in a self-contained case | notes one frame/burden effect or partially suppresses unnecessary machinery | tracks material commitment/answer-space/burden/criterion/evidence/downstream changes and stays dormant when none matter |
| Argument-target comprehension | attacks/credits wrong proposition | identifies conclusion but misses material warrant/dependency | identifies actual support/attack target and its downstream role |
| Evidence/provenance fidelity | confidence/source count/style substitutes for evidence | checks some sources but relevance/directness remains vague | evaluates relevance, independence, directness, measurement quality and provenance |
| Reasoning-alignment fidelity | same answer is treated as same reasoning | notes causal disagreement but flattens implications | preserves mechanism/warrant disagreement when it changes action or evidence needs |
| Repair quality | continues reasoning on corrupted common ground or performs needless repair on an uncorrupted single-turn case | flags error but restarts broadly or leaves dependencies unclear | repairs earliest corrupted state when needed and otherwise avoids ceremonial repair |
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
- hosted/runtime activation is claimed without owning-surface verification;
- **`unnecessary_dialogue_state_invention`** — on a self-contained protection case, the response invents participants, prior commitments, common ground, concessions, or dialogue history that the input does not support, or replaces the actual semantic/causal task with ceremonial ledger output.

## Target-suite metrics

For DS1–DS8, emphasize:

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

## Protection-holdout metrics

For DSP1–DSP12, the primary question is not whether dialogue-state output looks sophisticated. It is whether loading the reference causes regression on capabilities already owned elsewhere.

Prefer the direct comparison:

`microscope-core` vs `microscope-dialogue-state`

Report at least:

- per-case applicable score delta;
- new blocking errors introduced by the treatment;
- `unnecessary_dialogue_state_invention` count/rate;
- regressions on definition/QUD/pragmatics;
- regressions on defeasible revision / stance freedom;
- regressions on argument-scheme / critical-question / steelman fidelity;
- regressions on causal, intervention and global-graph reasoning;
- judge disagreement on any claimed regression.

A material hard-slice regression or new blocking error is a **promotion veto** even if DS1–DS8 aggregate score improves.

`TARGET_GAIN != SAFE_PROMOTION`.

## Baseline protocol

For the target suite, compare the same cases under:

1. direct answer;
2. direct answer + generic `think carefully` instruction;
3. `semantic-argument-microscope` without `DIALOGUE_STATE.md` loaded;
4. `semantic-argument-microscope` with `DIALOGUE_STATE.md` loaded on matching triggers.

For the protection holdout, at minimum compare arms 3 and 4. Running direct/generic arms is optional because the protection claim is specifically whether the new reference regresses the existing semantic core.

Keep model version, tool access, retrieved evidence, sampling settings, and context as comparable as practical. Add paraphrased/domain-swapped variants before claiming transfer.

## Acceptance boundary

Do not mark this extension behaviorally verified from file writes, fixture parsing, CI success, synthetic self-tests, one impressive example, or preference for eloquence. Behavioral evidence requires actual target-model outputs, protection holdout results, recorded scores, and review of blocking errors.
