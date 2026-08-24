# Continuous Thinking Quality System — Legacy Compatibility Guide

Status: superseded by `docs/CONTINUOUS_THINKING_QUALITY_OS.md` v3.0.0.

This file remains in place so older links and tooling do not break. The canonical policy is the v3 Quality OS and the machine-readable profile is `control-plane/ai-system/configs/continuous-thinking-global.json`.

## Compatibility rules

- Deep thinking is measured by correctness, evidence, information gain, falsification, and task closure — not by elapsed minutes.
- Do not require arbitrary source quotas such as `100+ sources`. Research should continue only while new evidence can materially change the decision or expose an important failure mode.
- Do not require arbitrary waiting periods such as `10+ minutes`. Increase reasoning effort when uncertainty, impact, novelty, repeated failure, or verification difficulty justify it.
- Do not treat a fixed agent count as a quality metric. Existing fixed-lane orchestration is compatibility topology, not proof of depth.
- Before modifying a system, reconstruct current state, dependencies, protected behavior, acceptance criteria, and the smallest useful causal/system model.
- Every hard acceptance criterion starts `UNSATISFIED` and requires resolvable PASS evidence before it can become `SATISFIED`; partial completion cannot produce overall `PASS`.
- Track decision-critical unknowns. A high-impact unknown must be resolved, bounded by evidence, or reported as a blocker before `PASS`.
- Prefer the next action with the highest decision value: falsify the leading hypothesis, distinguish competing mechanisms, resolve a blocker, or verify the real user path.
- Repeated failure must create new information. After two materially similar failures, pivot the hypothesis, mechanism, diagnostic instrument, environment, evidence source, or verification method.
- Configuration presence is not runtime success. Verify `configured → registered → loaded → executed → observable effect` at the highest practical layer.
- Preserve durable expert experience as mechanism + preconditions + failure modes + verification + portable lesson + invalidation condition, rather than copying commands or prompts.
- Prefer a fresh-context evaluator for material/critical work so the builder's confidence does not become its own evidence.
- Do not announce completion from a write, a green unrelated check, an agent self-report, source-count volume, elapsed time, or agent-count volume.

## Canonical flow

Observe → Reconstruct → Default-fail Contract → Model → Resolve unknowns → Research if needed → Compare → Execute → Verify → Fresh-context/Falsify → Learn → Release

For material control-plane work, machine-checkable quality contracts and the deep reasoning receipt gate are authoritative.
