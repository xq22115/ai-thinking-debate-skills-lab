---
name: ai-efficiency-operating-system
description: Orchestrate complex AI work for maximum useful progress per unit of context, tool use and iteration while preserving quality, capabilities and verifiable completion.
---

# AI Efficiency Operating System

Version: `0.1.0-rc1`
Status: `PACKAGED_GITHUB_STAGED / HOST_LIVE_UNVERIFIED`

## Objective

Increase AI task efficiency without trading away required features, answer quality, evidence quality or completion truth. Efficiency means reducing wasted context, wrong routing, duplicate work, repeated failed approaches, unnecessary serialization and false-completion loops while increasing first-pass correctness and verified task closure.

## Activation

Use this skill when a task is complex, long-running, multi-tool, cross-chat, research-heavy, repair/debugging-oriented, multi-agent, or at risk of goal drift, context bloat, repeated work, latency or false completion.

Do not activate the full workflow for simple deterministic questions where extra orchestration would cost more than it saves.

## Canonical workflow

1. **Compile the task** into `PRIMARY_TASK`, `DESIRED_END_STATE`, `NEGATIONS`, `HARD_CONSTRAINTS`, `ACCEPTANCE_TESTS` and a stable evidence-backed `ROOT_GOAL`.
2. **Lock identity before mutation**: repository, branch/PR, path, version, runtime/profile, owner/supersession relation and permissions.
3. **Build an evidence-gap ledger** before accepting uncertain claims. Separate direct user directives, repository evidence, current external evidence, runtime observations and assistant synthesis.
4. **Maintain competing hypotheses** for material uncertainty; prefer discriminating tests over repeated discussion.
5. **Cluster symptoms by shared mechanism** and repair common causes before patching symptoms individually.
6. **Route context and tools on demand**. Keep capabilities available but load/call only those causally relevant to the current task; avoid indiscriminate tool/context fan-out.
7. **Parallelize independent reads/research**, but serialize writes to the same mutable target and require writer ownership.
8. **Use deliberation adaptively**. A role must add a distinct evidence channel, method, capability, falsification pressure or verification duty. Role count is not a quality metric.
9. **Prefer execution/read-back when it has higher information gain than more debate**. Stop research when new sources or roles no longer change the decision, risk estimate or acceptance result.
10. **Keep durable recoverable state** for multi-step work: task ID, checkpoint, pending actions, evidence refs, completed irreversible actions and rollback target.
11. **Apply the completion gate**. Never infer `TESTED`, `VERIFIED`, `HOST_LIVE_VERIFIED`, `DEPLOYED` or `HEALTHY` from file existence, a commit, configuration presence, CI metadata or an agent statement alone.
12. **Compress the final response after verification**: conclusion first, then only evidence, mechanism, action and material limitations that change the decision.

## Ten-role review topology

For high-complexity work, map responsibilities to the repository's existing A01–A10 control-plane roles rather than inventing aliases:

- A01 Orchestrator — task ledger, root goal, dependencies and acceptance ownership.
- A02 Architect/Claimant — candidate solution and architecture.
- A03 Source Research — original-source and provenance recovery.
- A04 Root Cause — shared mechanisms, dependency graph and discriminating tests.
- A05 Adversarial — omission, over-inclusion, regression and false-completion attacks.
- A06 Cross Exam — distinguish user directives, evidence and model synthesis; challenge naming and claims.
- A07 Implementer — scoped mutation with path/branch/version verification.
- A08 Verifier — structural validation, read-back, tests and acceptance evidence.
- A09 Risk — rollback, data-loss, overwrite, permission and compatibility risks.
- A10 Adjudicator — retain the best-supported solution and unresolved minority evidence.

These are responsibilities. Do not claim authentic runtime independence unless separate executions/processes/sessions are observed and receipted.

## Core efficiency skills

This orchestrator composes, rather than duplicates, the repository's existing portable skills:

- `evidence-gap-research`
- `competing-hypotheses`
- `root-cause-clustering`
- `compatibility-audit`
- `capability-challenge`
- `multi-agent-deliberation`
- `durable-agent-control-plane`
- `recoverable-state`
- `completion-gate`

Machine-readable extensions and examples are in `skillpack.json`.

## Non-goals

Do not improve apparent speed by disabling required functions, opening fewer required workspaces, deleting evidence, lowering answer quality, reducing requested concurrency, suppressing verification or replacing the task with an easier neighboring problem.

Do not use fixed waiting time, token drip, verbosity, role count or source count as proxies for depth.

Do not keep retrying the same failing method after evidence shows the mechanism is wrong; update the hypothesis, mechanism, route or source.

## Evidence and provenance contract

Every material skill entry should identify one of:

- `USER_DIRECTIVE` — explicitly required by the user;
- `REPOSITORY_CANONICAL` — already present in the canonical repository skill/control-plane artifacts;
- `CROSS_CHAT_GITHUB_RECOVERY` — recovered from pinned cross-chat GitHub artifacts;
- `ASSISTANT_SYNTHESIS` — a new integration/inference that must not be misrepresented as a direct user instruction;
- `REQUIRES_CONFIRMATION` — insufficient evidence for promotion.

When a branch or runtime changes, mutable evidence must be refreshed rather than inherited automatically.

## Output contract

Return or persist:

- task ledger and identity lock;
- activated skills/roles with reasons;
- evidence/provenance map;
- competing hypotheses and decisive tests when applicable;
- mutation/write plan;
- verification/read-back receipt;
- unresolved risks/TBD items;
- highest defensible completion state.

## Completion gate for this skill

`PACKAGED` requires this `SKILL.md` and a parseable machine-readable `skillpack.json` with unique names.
`GITHUB_COMMITTED` requires GitHub write receipts.
`VERIFIED` requires direct read-back of the committed files and structural/uniqueness checks.
`HOST_LIVE_VERIFIED` requires a target-host execution showing the skill is actually loaded/activated; repository presence alone is insufficient.
