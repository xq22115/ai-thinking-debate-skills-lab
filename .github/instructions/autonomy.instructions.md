---
applyTo: "control-plane/autonomy/**,.github/agents/**,docs/AUTONOMOUS_LEARNING_DEBUG_ARCHITECTURE_v1.md"
---

Changes to the autonomous learning/debug subsystem must remain deterministic, testable, rollback-friendly, and evidence-bound.

Do not weaken lesson-promotion thresholds merely to make tests pass. Do not convert model confidence or prose claims into verified evidence. Keep contradictory evidence visible.

Every behavioral change requires a focused regression test. Every new persisted field must have a clear reuse or invalidation purpose. Avoid hidden background daemons; prefer explicit event-driven execution through existing agent runtimes and GitHub Actions.

The two-strike pivot rule is a semantic invariant: renaming the same mechanism does not count as a pivot.
