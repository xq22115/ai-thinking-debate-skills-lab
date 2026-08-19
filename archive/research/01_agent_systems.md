# Agent Systems Research

## Primary objective
Build agent systems that do not stop after one superficial answer, do not mark partial work complete, and can recover/replan from errors.

## Repeated architectural themes

### 1. State machine over free-form prompting
Preferred pattern:
`INTAKE → DISCOVER → REPRODUCE → DIAGNOSE → PLAN → PRECHECK → SANDBOX_APPLY → OBSERVE → VERIFY → RED_TEAM → SELECT → COMMIT`

Failure must branch to:
- `ROLLBACK`
- `REPLAN`
- `HALT`

A later Continuous Thinking line used:
`INTAKE → PREPARE → DISCOVER → PLAN → EXECUTE → OBSERVE → VERIFY → RED_TEAM → SELECT → CANARY → COMMIT → POSTCHECK → COMPLETE`

## 2. Evidence before completion
Completion should require:
- requirement IDs,
- evidence per requirement,
- test artifacts,
- contradiction resolution,
- regression checks,
- explicit unresolved risks.

## 3. Root-error unification
Instead of:
`A fails → patch A → B fails → patch B → C fails`

model the common mechanism behind A/B/C and repair the shared root cause. This reduces cascading symptom patches.

## 4. Agent diversity must be real
A “30-agent” or “10-agent” scheme should not be counted as diverse merely because labels differ. Strategy fingerprints must differ in:
- assumptions,
- tools/evidence sought,
- failure model,
- success criteria,
- adversarial stance.

## 5. Idle is not done
A key borrowed concept from OpenHands research: lack of visible activity is not sufficient evidence that a task is complete.

## 6. Ledger-based continuity
Useful patterns:
- facts ledger,
- plan ledger,
- progress ledger,
- issue/defect ledger,
- evidence ledger,
- decision log,
- rollback log.

## 7. Checkpoint / replay / interrupt
LangGraph-style checkpointing was identified as a useful conceptual basis for resumable agent workflows.

## 8. Repair feedback loop
Aider-style lint/test feedback was identified as a strong pattern:
`change → run checks → feed failure → revise → re-run`

## Risks
- fake diversity,
- “1/10 complete” mislabeled as complete,
- stale memory overriding repository evidence,
- cross-product surface confusion,
- hidden dependency drift,
- agent stalls without terminal criteria,
- unbounded retries,
- privilege creep through MCP/tools.
