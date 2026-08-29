---
name: agent-runtime-forensics
description: Use when an agent's behavior, side effects, provenance, or completion is disputed and model/tool transcripts alone cannot prove which decision, tool call, process, file, network event, or artifact caused the observed result.
---

# Agent Runtime Forensics

## Core principle

Reconstruct **causality outside model prose**. Model intent, tool return text, OS/runtime effects, and final postconditions are separate evidence channels.

## Causal chain

Prefer a scoped chain such as:

`BASE_STATE → RUN → MODEL_EVENT → TOOL_EVENT → PROCESS → FILE/NETWORK/RUNTIME EVENT → ARTIFACT → POSTCONDITION`

Missing edges stay missing; do not bridge them with the executor's narrative.

## Workflow

1. Lock run/session/target identity and the observation window.
2. Capture or locate model/tool events plus available runtime telemetry.
3. Normalize process, file, network, artifact and external-effect identifiers.
4. Hash material evidence where possible and preserve timestamps/lineage.
5. Build support/refute edges for claimed causality.
6. Mark tainted, ambiguous, concurrent, or cross-run evidence explicitly.
7. Use diff/blame/replay only when the effect model says replay is safe.
8. Let an external verifier judge acceptance-critical completion; the forensic layer supplies evidence, not self-certification.

**REQUIRED REFERENCE:** read `references/runtime-provenance.md` for material investigations.

## High-value uses

- tool says success but no file/state change exists;
- unexpected file/network/process effect;
- multiple agents touched one target;
- stale worker or wrong session caused a mutation;
- determining which model/tool step produced an artifact;
- comparing before/after runs without trusting summaries;
- generating a forensic manifest for independent evaluation.

## Output

Return run scope, evidence manifest, causal graph, missing/ambiguous edges, effect status, replay safety, and the strongest externally verifiable postcondition.

## Boundary

Do not infer private telemetry that was never observed, and do not treat monitoring capability as permission to inspect data outside the authorized target scope.
