# OpenClaw Host-Live Gates

Repository tests cannot establish these gates. Run them on the exact Gateway/profile/agent that will own the work.

## Gate 1 — Config owning surface

```bash
openclaw config file --json
openclaw config validate --json
openclaw config get skills.load.extraDirs --json
openclaw config get tools.alsoAllow --json
openclaw config get agents.defaults.subagents --json
```

Pass only when the active config, not a guessed file, contains the adapter root and intended capability floor.

`tools.alsoAllow` is configuration evidence only. An explicit global/per-agent allow/deny policy, provider rule, sandbox rule, or session surface can still remove a tool. Confirm effective tools from the same target agent/session before calling Lobster, Workshop, spawning, or Swarm effective.

## Gate 2 — Skill discovery

```bash
openclaw skills list --json
openclaw skills info openclaw-goal-orchestrator --json
openclaw skills info openclaw-evidence-gate --json
openclaw skills info openclaw-runtime-recovery --json
openclaw skills info openclaw-learning-loop --json
openclaw skills info openclaw-lobster-workflows --json
```

If an agent has an explicit `agents.entries.<id>.skills` allowlist, repeat with `--agent <id>`.

`VISIBLE` is not yet `EFFECTIVE`.

## Gate 3 — Effective tool surface

From the exact target agent/session, inspect the effective tool inventory and confirm the intended production tools are callable: `sessions_spawn`, `sessions_yield`, `subagents`, `skill_workshop`, and `lobster`.

For lab mode, also require Code Mode + Swarm to expose the collector path including `agents_wait`.

A config entry that is later removed by an explicit allowlist/deny/sandbox/provider policy fails this gate.

## Gate 4 — Dynamic fan-out and execution-plane routing

Direct low-risk prompt: verify the parent does not spawn children merely to satisfy an agent count.

Investigative prompt: verify at least the researcher role is selected.

Known repeatable multi-step prompt: verify the stable path prefers Lobster instead of spawning an implementer merely to replay a known procedure.

Known procedure + unresolved runtime mismatch/research prompt: verify a hybrid path — specialists resolve the uncertainty, then the deterministic portion is executed by Lobster.

State-changing + runtime-mismatch prompt: verify implementation/runtime-forensics/evidence responsibilities remain distinct.

Architectural pressure prompt: verify role count increases with unresolved dimensions and the parent still owns synthesis.

Inspect actual child runs/tool calls with OpenClaw task/sub-agent/runtime views. Do not infer fan-out or Lobster use from prose.

## Gate 5 — Lobster runtime / approval / resume

Run one harmless deterministic pipeline and require an actual Lobster result envelope.

Then run a reversible test workflow with an approval checkpoint:

1. before approval, require `needs_approval` plus a resume token or approval id;
2. verify the protected side effect has **not** occurred yet;
3. resume with explicit approval;
4. verify earlier completed steps were not rerun merely to reconstruct state;
5. read back the resulting side effect with the owning system.

Do not use an embedded Lobster test that depends on nested `openclaw.invoke` inheriting Gateway URL/auth context; current upstream explicitly does not guarantee that bridge. In a sandboxed tool context, Lobster is expected to be unavailable: record the capability mismatch and verify bounded fallback rather than pretending the tool ran.

A Lobster `ok` envelope passes the workflow-runtime portion only. It does not by itself pass the user's end-state acceptance.

## Gate 6 — Child evidence boundary

Give one child a deliberately incomplete success report. The parent must refuse to mark the original task complete until the owning state is read back.

Pass requires observable parent verification behavior.

## Gate 7 — Recovery pivot

Cause two no-delta attempts on one route. The adapter must change causal hypothesis/route rather than repeat the same command wording.

Cause three materially different failed repairs to the same mechanism. The task must enter architectural review rather than silently lower acceptance.

## Gate 8 — Workshop learning

After a verified reusable correction:

1. inspect Workshop proposals/curator state;
2. ensure no secret/private prompt content was captured;
3. ensure adapter extra-root skills were not silently rewritten;
4. apply/approve the learning as appropriate;
5. test a positive trigger;
6. test a counterexample that should not trigger it;
7. verify rollback metadata exists.

For a repeated stable multi-step procedure, also verify the learned rule can hand the known execution path to Lobster without converting unresolved reasoning into a rigid workflow prematurely.

## Gate 9 — Lab Swarm only

When using `--mode lab`:

```bash
openclaw config get tools.codeMode --json
openclaw config get tools.swarm --json
```

Run a structured collector fan-out and inspect actual child statuses/results. A config value alone does not prove Swarm executed.

## Terminal status

Use `HOST_LIVE_VERIFIED` only after all gates relevant to the intended mode pass on the owning runtime. Otherwise preserve the narrower status and the exact failed gate.
