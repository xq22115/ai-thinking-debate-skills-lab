---
name: openclaw-runtime-recovery
description: Use when OpenClaw tools, agents, skills, delivery, config, browser, files, or runtime effects fail, stall, disagree, or report success without effect.
---

# OpenClaw Runtime Recovery

Recover the user's original end state without lowering capability, acceptance, or verification.

## First upstream failure

Trace the causal path:

`intent → routing → skill/tool visibility → authorization → invocation → runtime → side effect → delivery/read-back`

Find the earliest broken edge that explains the downstream symptoms. Do not repeatedly patch later symptoms while the upstream edge remains false.

## Route-pivot rules

- The same strategy may receive at most one retry without new evidence.
- **Two consecutive** material steps with no acceptance/evidence/state/uncertainty delta require a different causal route.
- **Three materially distinct** failed repairs to one mechanism require architectural review.
- Localize a blocked slice and continue all separable work.
- Preserve unaffected evidence after a correction or failure.
- Never turn one unavailable tool into a claim that the whole goal is impossible.

A different causal route means changing the mechanism or hypothesis, not merely rephrasing the same command.

## Runtime mismatch

When a tool reports success but the intended effect is absent:

1. record the exact claimed action and target;
2. inspect the owning runtime/process/file/network/artifact;
3. distinguish registration from invocation and invocation from effect;
4. check session/profile/agent/workspace/version identity;
5. reproduce with the smallest discriminating probe;
6. repair the first false edge;
7. rerun the original acceptance test.

## Child failures

A failed child is not a reason to abandon the task. Re-brief, choose a materially different role/tool, or continue in the parent when that is the stronger route.

Do not create infinite polling or retry loops. Use OpenClaw's completion/collector semantics and bounded waits.

## Recovery receipt

Expose only useful state:

- failed acceptance;
- first upstream failure or strongest hypothesis;
- evidence that discriminated it;
- route changed;
- remaining blocker;
- current postcondition status.
