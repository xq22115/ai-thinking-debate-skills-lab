# Continuous Thinking Quality System — Legacy Compatibility Guide

Status: superseded by `docs/CONTINUOUS_THINKING_QUALITY_OS.md` v2.1.0.

This file remains in place so older links and tooling do not break. The canonical policy is the v2.1 Quality OS.

## Compatibility rules

- Deep thinking is measured by correctness, evidence, information gain, falsification, and task closure — not by elapsed minutes.
- Do not require arbitrary source quotas such as `100+ sources`. Research should continue only while new evidence can materially change the decision or expose an important failure mode.
- Do not require arbitrary waiting periods such as `10+ minutes`. Increase reasoning effort when uncertainty, impact, novelty, repeated failure, or verification difficulty justify it.
- Before modifying a system, reconstruct current state, dependencies, protected behavior, acceptance criteria, and the smallest useful causal/system model.
- Track decision-critical unknowns. A high-impact unknown must be resolved, bounded by evidence, or reported as a blocker before `PASS`.
- Prefer the next action with the highest decision value: falsify the leading hypothesis, distinguish competing mechanisms, resolve a blocker, or verify the real user path.
- Repeated failure must create new information. After two materially similar failures, pivot the hypothesis, mechanism, diagnostic instrument, environment, evidence source, or verification method.
- Configuration presence is not runtime success. Verify `configured → registered → loaded → executed → observable effect` at the highest practical layer.
- Preserve durable expert experience as mechanism + preconditions + failure modes + verification + invalidation condition, rather than copying commands or prompts.
- Do not announce completion from a write, a green unrelated check, an agent self-report, source-count volume, or elapsed time.

## Canonical flow

Observe → Reconstruct → Model → Resolve unknowns → Research if needed → Compare → Execute → Verify → Falsify → Learn → Release

For material control-plane work, the machine-checkable deep reasoning receipt gate is authoritative.
