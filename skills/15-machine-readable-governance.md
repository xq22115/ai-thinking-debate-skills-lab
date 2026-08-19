# 15 — Machine-Readable Governance Layer

Date: 2026-08-18

This layer converts the human-readable deliberation and release rules into data structures that a future runtime can inspect directly.

## Files

### `data/role_activation_policy.yaml`

Purpose:
- encode the adaptive 1–30-role policy from `07-deliberation-router-spec.md`;
- distinguish deterministic, independent-alternative, adversarial, extended-council and full-pool tiers;
- provide escalation/de-escalation triggers;
- prohibit 30-clone/majority-vote/approval-theater anti-patterns;
- preserve explicit release states.

Key rule:

> 30 roles are a coverage pool, not a required fan-out count.

The router should activate a role only when it adds independent evidence, a distinct hypothesis, a required capability, or a verification duty.

### `data/claim_obligation_graph.json`

Purpose:
- represent major research conclusions as claims;
- represent non-negotiable completion/compatibility duties as obligations;
- link claims to repository evidence;
- expose release invariants in a format that can be checked mechanically.

Important invariants include:

- `UNKNOWN != IMPOSSIBLE`
- `FAILED_PATH != FAILED_GOAL`
- `DOCUMENTATION != RUNTIME_PROOF`
- `CONFIGURED != VERIFIED_DIRECT`
- `CONFIDENCE != EVIDENCE`
- `CONSENSUS != CORRECTNESS`
- `LOCAL_TEST_PASS != HOSTED_CI_PASS`
- `REPOSITORY_ARTIFACT != PROVIDER_LIVE_EXECUTION`
- `TOOL_SUCCESS != TASK_COMPLETE`

## 2026 platform delta now incorporated

`08-portability-matrix.md` was refreshed in the same pass with current official GitHub evidence:

1. **OpenAI Codex** — current example packaging is plugin-first: required `.codex-plugin/plugin.json` plus optional skills/apps/MCP/agents/commands/hooks/assets. The former `openai/skills` repository is deprecated for current deployment guidance.
2. **Anthropic Skills** — self-contained `SKILL.md` remains a portable semantic pattern, but the official repository explicitly warns that critical use requires target-environment testing.
3. **Google ADK** — official Python README observed 2026-08-13 identifies **ADK 2.0** and a breaking-change boundary in agent API, event model and session schema. 2.0 sessions are readable by 1.28+ with extra fields ignored, but older 1.x versions are not session-compatible.

## Why this matters

The research archive previously had strong prose governance. This addition makes the same constraints easier to consume by:

- a task router;
- an evaluator;
- a release checker;
- a GitHub-backed control plane;
- a cross-platform adapter generator.

It does **not** prove those runtimes have been implemented or provider-live tested.

Current truth remains:

`RC1_PACKAGED_AND_GITHUB_STAGED / CI_BLOCKED / HOST_LIVE_UNVERIFIED`
