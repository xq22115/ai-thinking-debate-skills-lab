# Reference Architecture — Evidence-Gated Deliberation & Skills OS

Version: `1.2`

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
VOI ROUTER
  ├─ next test/search/action value
  ├─ decision sensitivity
  ├─ expected information gain
  └─ stop / continue
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

If the answer to (1) is no, stop reasoning and execute/answer.
If (2) is yes, prefer the observation/test over more debate.
Activate the next layer only when (3) is yes.

`DEPTH = RELEVANT DISCRIMINATION, NOT MAXIMUM PROCEDURE COUNT`

## Epistemic state machine

`INTAKE → CLAIM_NORMALIZE → EVIDENCE_SUFFICIENCY → INTERPRET → CAUSALIZE(if needed) → HYPOTHESIZE → TEST/DELIBERATE(if useful) → UPDATE → EXECUTE → OBSERVE → VERIFY → COMMIT`

Valid non-success terminal/intermediate states include:

- `UNRESOLVED_WITH_EVIDENCE_GAP`
- `BLOCKED_WITH_TARGET_BOUND_EVIDENCE`
- `DEFERRED_LOW_VOI`
- `REPLAN`
- `ROLLBACK`

Do not force every path into a definitive yes/no conclusion.

## Evidence / belief invariants

- `SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`
- `CONFIDENCE_CHANGE REQUIRES EVIDENCE_DELTA`
- `CONFLICTING_EVIDENCE != LICENSE_TO_PICK_ONE_SIDE`
- `RELEVANCE != RELIABILITY != DIAGNOSTICITY`
- `MORE_REASONING != BETTER_CALIBRATION`
- `CONSENSUS != CORRECTNESS`
- `RHETORICAL_WIN != EPISTEMIC_WIN`
- `ASSOCIATION != INTERVENTION`
- `LOCAL_CAUSAL_PLAUSIBILITY != GLOBAL_GRAPH_COHERENCE`

## Status vocabulary

Never collapse these states:

`DRAFTED`, `PACKAGED`, `STATIC_VALIDATED`, `TESTED`, `REVIEWED`, `VERIFIED`, `HOST_LIVE_UNVERIFIED`, `HOST_LIVE_VERIFIED`, `DEPLOYED`, `HEALTHY`.

An epistemically unresolved claim can coexist with a successfully completed research task if the acceptance criterion was to determine what is currently knowable and why.

## Deliberation routing

Use more roles when uncertainty, conflicting evidence, impact, irreversibility, cross-platform compatibility, or security risk is high **and** another role provides a distinct method/evidence channel.

Use fewer roles when direct evidence or a discriminating test dominates discussion in expected information value.

Never invoke more agents merely because the task is described as difficult.

## Anti-fake-completion gate

A task may declare `VERIFIED` only when all critical acceptance conditions have target-bound evidence, no blocking red-team finding remains, no critical unknown was closed without evidence, regression scope was checked, and the status label exactly matches what was tested.

`UNRESOLVED` is preferable to a fabricated definitive answer when evidence remains conflicting or insufficient.

## Compatibility adapter layer

Do not assume one skill format is natively portable everywhere. Keep a portable procedural core and host adapters for OpenAI/ChatGPT/Agents SDK, Claude/Claude Code/Agent Skills, MCP, OpenClaw, IDE agents, Windows, and macOS.

Host adapters may change invocation mechanics but must not weaken the epistemic/completion invariants of the portable core.
