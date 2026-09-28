---
name: root-cause-falsification
description: Use when debugging, repair, optimization, flaky behavior, performance issues, capability claims, repeated workaround stacks, or completion claims can be falsely passed by symptom masking, success cherry-picking, or weak evidence.
---

# Root Cause Falsification — Plugin Projection

Canonical owner: `skills/skills/root-cause-falsification/SKILL.md`.
Machine contract: `control-plane/ai-system/configs/root-cause-falsification-v1.json`.

Load the canonical owner and machine contract before material diagnosis, mutation, or “fixed/verified” claims when this skill matches.

Critical gates:
- examples are non-binding unless explicitly made requirements;
- trigger conditions do not become root causes by convenience;
- caps, throttles, disabled features, reduced concurrency/quality, avoidance, watchdogs, and warning-only controls are mitigation/guardrail/degradation unless they remove the causal mechanism;
- one reproducible in-scope failure falsifies a universal zero-failure completion claim;
- verification scope is declared before observing results and all in-scope trials count;
- practical quality uses owning-runtime plus independent practitioner/issue/PR/postmortem/benchmark evidence; official docs remain authoritative for contracts, supported syntax, versions, limits, and lifecycle;
- search evidence must feed a discriminating target test before it authorizes a material repair;
- previously failing cases are retained and replayed as regression tests.

Advanced field-practice anchors: `../../references/root-cause-falsification-field-practice.md`.

Do not duplicate or soften the canonical skill.
