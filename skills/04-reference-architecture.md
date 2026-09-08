# Reference Architecture — Evidence-Gated Deliberation & Skills OS

Version: `1.3`

## Core architecture

```text
USER INTENT
  ↓
INTAKE / GOAL + ACCEPTANCE CONTRACT
  ↓
CAPABILITY / COMPATIBILITY PRECHECK
  ↓
EPISTEMIC GATE
  ├─ claim ledger
  ├─ evidence sufficiency
  ├─ source provenance / dependence
  ├─ contradiction ledger
  └─ highest-value missing evidence
  ↓
SEMANTIC / ARGUMENT GATE (only when wording/inference is contested)
  ├─ literal vs pragmatic meaning
  ├─ QUD / crux
  ├─ claim / grounds / warrant
  ├─ argument scheme
  └─ decision-critical questions
  ↓
CAUSAL / ABDUCTIVE GATE (only when the crux is why/what-caused/what-if)
  ├─ candidate causal graph
  ├─ confounder / reverse / selection checks
  ├─ association vs intervention vs counterfactual
  └─ competing causal explanations
  ↓
HYPOTHESIS / ROOT-CAUSE LAYER
  ├─ materially different hypotheses
  ├─ discriminating tests
  └─ mechanism-level clustering
  ↓
DELIBERATION ROUTER (only if another independent role can change the decision)
  ├─ independent methods / evidence channels
  ├─ specialist roles
  ├─ red team / falsifier
  ├─ minority preservation
  └─ bias-resistant evidence-weighted judge
  ↓
VERIFIER / METAMORPHIC GATE (when consequence or brittleness warrants it)
  ├─ deterministic invariants first
  ├─ evaluator swap / blind labels
  ├─ semantics-preserving perturbations
  └─ hidden/adversarial variants
  ↓
VOI ROUTER
  ├─ next test/search/action value
  ├─ decision sensitivity
  ├─ expected information gain
  └─ stop / continue
  ↓
DECISION ROBUSTNESS GATE (when action is consequential)
  ├─ belief ≠ action separation
  ├─ asymmetric loss / regret
  ├─ reversibility / rollback
  ├─ distribution-shift transfer check
  ├─ sensitivity / threshold flip
  ├─ open-world / misspecification check
  └─ COMMIT / PROBE / PILOT / DEFER / ABSTAIN / ROBUST_FALLBACK
  ↓
PLAN / PRECHECK
  ├─ permissions
  ├─ security
  ├─ rollback
  └─ target/environment binding
  ↓
EXECUTION HARNESS
  ├─ sandbox/tool boundary
  ├─ skill loader
  ├─ deterministic action layer
  └─ durable task state
  ↓
OBSERVE / EVAL
  ├─ tests / measurements
  ├─ traces / receipts
  ├─ contradiction updates
  ├─ counterexample checks
  ├─ shift / sensitivity updates
  └─ confidence update with evidence delta
  ↓
COMPLETION GATE
  ↓
CHECKPOINT / ARCHIVE / DEPLOY
```

## Progressive-disclosure rule

Do **not** execute every reasoning layer on every task.

At each gate ask:

1. Is there a material unresolved uncertainty?
2. Can a cheaper direct observation/test settle it?
3. Will the next reasoning layer produce information that can change the decision?
4. Is the decision robust enough to act without that next layer?

If the answer to (1) is no, stop reasoning and execute/answer.
If (2) is yes, prefer the observation/test over more debate.
Activate the next layer only when (3) is yes or when (4) is no for a consequential action.

`DEPTH = RELEVANT DISCRIMINATION + DECISION ROBUSTNESS, NOT MAXIMUM PROCEDURE COUNT`

## Epistemic / decision state machine

`INTAKE → CLAIM_NORMALIZE → EVIDENCE_SUFFICIENCY → INTERPRET → CAUSALIZE(if needed) → HYPOTHESIZE → TEST/DELIBERATE(if useful) → VERIFY(if useful) → UPDATE → DECIDE_ACTION → EXECUTE → OBSERVE → VERIFY_TARGET → COMMIT`

Valid non-success terminal/intermediate states include:

- `UNRESOLVED_WITH_EVIDENCE_GAP`
- `BLOCKED_WITH_TARGET_BOUND_EVIDENCE`
- `DEFERRED_LOW_VOI`
- `PROBE_REQUIRED`
- `PILOT_REQUIRED`
- `SHIFT_UNSAFE`
- `THRESHOLD_SENSITIVE`
- `ROBUST_FALLBACK_SELECTED`
- `REPLAN`
- `ROLLBACK`

Do not force every path into a definitive yes/no conclusion or an immediate commitment.

## Evidence / belief / decision invariants

- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`
- `CONFIDENCE_CHANGE REQUIRES EVIDENCE_DELTA`
- `CONFLICTING_EVIDENCE != LICENSE_TO_PICK_ONE_SIDE`
- `RELEVANCE != RELIABILITY != DIAGNOSTICITY`
- `MORE_REASONING != BETTER_CALIBRATION`
- `MOST_LIKELY_STATE != BEST_ACTION`
- `CONFIDENCE != UTILITY`
- `CALIBRATED_IN_DOMAIN != CALIBRATED_UNDER_SHIFT`
- `IRREVERSIBLE_ACTION REQUIRES STRONGER_DECISION_EVIDENCE`
- `UNRESOLVED_STATE != NO_ACTION_POSSIBLE`
- `CONSENSUS != CORRECTNESS`
- `RHETORICAL_WIN != EPISTEMIC_WIN`
- `ASSOCIATION != INTERVENTION`
- `LOCAL_CAUSAL_PLAUSIBILITY != GLOBAL_GRAPH_COHERENCE`
- `VERIFIER_PASS != TASK_TRUTH`

## Status vocabulary

Never collapse these states:

`DRAFTED`, `PACKAGED`, `STATIC_VALIDATED`, `TESTED`, `REVIEWED`, `VERIFIED`, `HOST_LIVE_UNVERIFIED`, `HOST_LIVE_VERIFIED`, `DEPLOYED`, `HEALTHY`.

An epistemically unresolved claim can coexist with a successfully completed research task if the acceptance criterion was to determine what is currently knowable and why. Likewise, an unresolved belief can still permit a justified `PROBE`, `PILOT`, or `ROBUST_FALLBACK` action.

## Deliberation routing

Use more roles when uncertainty, conflicting evidence, impact, irreversibility, cross-platform compatibility, security risk, or suspected distribution shift is high **and** another role provides a distinct method/evidence channel.

Use fewer roles when direct evidence, a discriminating test, or a reversible probe dominates discussion in expected information value.

Never invoke more agents merely because the task is described as difficult.

## Decision routing

Before a consequential commitment, separate:

- what is believed;
- how uncertain that belief is;
- what each action costs under each live state;
- whether calibration is transferable to the current context;
- whether small plausible assumption changes flip the recommendation;
- whether a reversible probe/pilot or robust fallback can dominate immediate commitment.

Do not treat a calibrated probability estimate as a complete decision policy.

## Anti-fake-completion gate

A task may declare `VERIFIED` only when all critical acceptance conditions have target-bound evidence, no blocking red-team finding remains, no critical unknown was closed without evidence, regression scope was checked, and the status label exactly matches what was tested.

`UNRESOLVED` is preferable to a fabricated definitive answer when evidence remains conflicting or insufficient; `PROBE` or `PILOT` is preferable to brittle commitment when uncertainty remains decision-critical but reversible learning is available.

## Compatibility adapter layer

Do not assume one skill format is natively portable everywhere. Keep a portable procedural core and host adapters for OpenAI/ChatGPT/Agents SDK, Claude/Claude Code/Agent Skills, MCP, OpenClaw, IDE agents, Windows, and macOS.

Host adapters may change invocation mechanics but must not weaken the epistemic, decision-robustness, verification, or completion invariants of the portable core.