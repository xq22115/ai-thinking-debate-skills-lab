# STATUS — 2026-08-18

## Current candidate

`Evidence-Gated Deliberation & Skills OS v1.3 RC1`

Highest defensible status:

`RC1_PACKAGED_AND_GITHUB_STAGED / CI_BLOCKED / HOST_LIVE_UNVERIFIED`

PR: `#45` — `research: Evidence-Gated Deliberation & Skills OS v1.3 RC1`

PR must remain **Draft** while blocking release gates remain unresolved.

## Completed / staged

- Substantial cross-chat recovery for AI thinking, debate, skills, evidence governance, recovery, OpenClaw and related systems.
- 30-role deliberation coverage topology defined; runtime fan-out remains adaptive.
- Dynamic 1–30 role deliberation router and machine-readable activation policy staged.
- Claim/obligation graph and hard release invariants staged.
- 9 portable RC1 skills staged.
- Five high-impact skills hardened to `0.1.1-rc1`:
  - capability-challenge
  - completion-gate
  - compatibility-audit
  - durable-agent-control-plane
  - multi-agent-deliberation
- Adversarial RC1 fixture set expanded to 15 cases (`0.1.1-rc1`).
- Portability/compatibility matrix staged.
- Durable-agent control-plane abstraction staged.
- Host-adapter boundary staged.
- Cross-chat convergence with PR #46 archive/vault and PR #29 execution/control-plane staged.
- Governance/autonomy principles distilled from PR #28, PR #25 and PR #19 without copying host-specific automation wholesale.
- Exact internal cross-chat PR/branch/head source lock staged.
- 10-gate RC1 release/status policy staged.
- External 2026 upstream snapshot expanded to exact commit SHA locks.
- Evidence ledger expanded to 22 sources with explicit source-class separation.
- OpenAI Codex product guidance / repository content / repository metadata contradiction handling documented.
- Google ADK 2.0 breaking version/session boundary independently verified from current upstream README.
- 2026-08-18 upstream delta analysis staged.
- README synchronized to current RC1 skills/evals/source count.

## Canonical architecture

`ARCHIVE TRUTH → EVIDENCE GAP → COMPETING HYPOTHESES → DYNAMIC DELIBERATION → ROOT CAUSE → COMPATIBILITY → DURABLE CONTROL PLANE → EXECUTION → RECEIPTS/EVALS → COMPLETION GATE → CHECKPOINT/RECOVERY`

Design rules:

**TRUTH HARD / METHOD SOFT**

`VISIBLE → AUTHORIZED → VERIFIED`

`PRODUCT_GUIDANCE / REPOSITORY_CONTENT / REPOSITORY_METADATA / RUNTIME_OBSERVATION`

Scale by unresolved information, consequence and verifiable execution value — not by a fixed agent count or prompt length.

## GitHub connector

Authenticated profile: `xq22115-pixel`.

Writable organization repositories observed:
- `xq22115/braintrust`
- `xq22115/cursor`
- `xq22115/demo-repository`

The current connected action set does not expose top-level repository creation.

## Staging location

- Repository: `xq22115/demo-repository`
- Branch: `research/ai-thinking-debate-skills-20260818`
- PR: `#45`
- Directory: `research/ai-thinking-debate-skills-2026-08-18/`

## Cross-chat source roles

- PR #46 = archive/vault layer.
- PR #45 = portable reasoning/skills/evidence layer.
- PR #29 = execution/control-plane layer.
- PR #28/#25/#19 = governance/autonomy inputs, distilled rather than copied wholesale.

Exact source heads are pinned/snapshotted in `13-cross-chat-source-lock.json`; do not migrate from a moving branch without recording a newer verified checkpoint.

## External source reproducibility

`12-upstream-source-lock.json` pins current upstream repositories by exact SHA where applicable. `05-source-ledger.json` now contains 22 sources and separately records current product guidance, repository content and repository metadata when these can diverge.

Important current lines include:
- OpenAI Agents Python
- OpenAI Codex plugin/skill product guidance
- `openai/skills` README deprecation evidence
- `openai/plugins` example format snapshot + archived metadata observation
- Anthropic Skills
- Microsoft Agent Framework
- Google ADK 2.0
- LangGraph
- Superpowers
- OpenClaw
- Model Context Protocol
- AutoGen maintenance marker

Human-readable implications are in `13-aug18-upstream-delta.md` and `16-governance-autonomy-convergence.md`.

## Commit receipts from current continuation

Research/evidence:
- Upstream exact-SHA source lock: `4da42deb62233a9d5a78aead2930bd82accca3ef`
- 2026-08-18 upstream delta synthesis: `e15ce0a1b509828b21156a4d9f420c8856e2a357`
- Initial 18-source ledger: `34bc922d6105aedc9c17319890b7ff9fffdf96be`
- Governance/autonomy convergence: `82012944f0b8f9a8eb97c0b20079927163543279`
- 22-source ledger expansion: `5d356d2f0180e719a06f280e08264031428ffede`

Skill hardening:
- capability-challenge 0.1.1: `c9c217667136e443c4b963e9b5d8215840879927`
- completion-gate 0.1.1: `d59b56ae51add42993b13dbd97b5c1976f22be8c`
- compatibility-audit 0.1.1: `078c4f03bdb987feabe8d6e12c41b2133757c879`
- durable-agent-control-plane 0.1.1: `911e3399557449c1097663bb1ead99f504effd1c`
- multi-agent-deliberation 0.1.1: `85a3d77745b96fcb18df68990f0b3d2e3beb8e14`
- nine-skill README synchronization: `43df376d7375e0db60515b6d92ea33ca46578aae`
- skills catalog synchronization: `8e41016d9a2b120dd8a89e411885221d658fb822`
- 15-fixture eval specification: `4ba18701f3a366af662f733bf30fc1eae6d7a478`
- top-level README synchronization: `696ef554dc62eda719e856596e0dc9f800280374`

Earlier v1.1 receipts remain part of branch history:
- Evaluation suite: `f8b4506a5a9628d7d1ed6b444f5b48715622cc2c`
- Deliberation router: `6f3a5d6b36f9c27ef04df49c96fbea7f2472e05d`
- Portability matrix: `02412106cf334e2cd7f4092610c5a8cad18a7d2f`
- Research backlog: `48b739db0a86b8b8c34728d6752c31ef52cd81b3`

## Status boundary

- `PACKAGED`: YES
- `GITHUB_COMMITTED`: YES
- `CROSS_CHAT_SOURCE_LOCKED`: YES (snapshot-based; moving heads require re-snapshot)
- `UPSTREAM_SOURCE_LOCKED`: YES where repository pinning is applicable
- `EVAL_SPECIFIED`: YES
- `EVAL_EXECUTED_HOSTED`: NO
- `CI_HEALTHY`: NO
- `AUTHENTIC_MULTI_AGENT_RUNTIME_VERIFIED`: NO
- `HOST_ADAPTER_VERIFIED`: NO
- `DEDICATED_REPOSITORY_CREATED`: NO
- `HOST_LIVE_VERIFIED`: NO
- `STABLE`: NO
- `MERGE_READY`: NO

## Blocking issues

### Issue #47 — Hosted GitHub Actions

Title: `blocker: GitHub Actions jobs fail before steps execute`

Leading diagnosis:

`BLOCKED_BY_BILLING_OR_SPENDING_LIMIT`

Latest inspected exact-head family before this status commit reproduced completed/failure jobs with `steps=null` across Core CI, Proof HTML, Auto Assign and PR Risk Router. This must not be misreported as a code/test failure or success. A new branch commit invalidates automatic inheritance of that exact-head CI snapshot; the new head must be checked again.

Acceptance requires a fresh run on the final head that actually starts workflow steps and passes or produces actionable step-level failures.

### Issue #48 — Dedicated repository migration

Target: `ai-thinking-debate-skills-lab`

Status:

`BLOCKED_BY_CONNECTOR_CAPABILITY`

The dedicated repository must not be reported as existing until it actually exists. When creation becomes available, migrate from pinned PR/head sources with provenance/hashes and keep archive, portable skills and control-plane layers separated.

## Release authority

`14-rc1-release-gates.md` is authoritative for promotion beyond RC1 staging.

Do not infer:
- committed → CI passed;
- eval specified → eval executed;
- role list → independent external agents ran;
- visible tool → authorized host mutation;
- repository artifact → runtime behavior verified;
- local/deterministic test → live provider verified;
- staged branch → dedicated repository exists;
- package → stable/deployed/healthy.
