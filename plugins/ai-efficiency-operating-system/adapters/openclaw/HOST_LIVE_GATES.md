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

## Gate 2 — Skill discovery

```bash
openclaw skills list --json
openclaw skills info openclaw-goal-orchestrator --json
openclaw skills info openclaw-evidence-gate --json
openclaw skills info openclaw-runtime-recovery --json
openclaw skills info openclaw-learning-loop --json
```

If an agent has an explicit `agents.entries.<id>.skills` allowlist, repeat with `--agent <id>`.

`VISIBLE` is not yet `EFFECTIVE`.

## Gate 3 — Dynamic fan-out

Direct low-risk prompt: verify the parent does not spawn children merely to satisfy an agent count.

Investigative prompt: verify at least the researcher role is selected.

State-changing + runtime-mismatch prompt: verify implementation/runtime-forensics/evidence responsibilities remain distinct.

Architectural pressure prompt: verify role count increases with unresolved dimensions and the parent still owns synthesis.

Inspect child runs with the OpenClaw sub-agent/task views. Do not infer fan-out from prose.

## Gate 4 — Child evidence boundary

Give one child a deliberately incomplete success report. The parent must refuse to mark the original task complete until the owning state is read back.

Pass requires observable parent verification behavior.

## Gate 5 — Recovery pivot

Cause two no-delta attempts on one route. The adapter must change causal hypothesis/route rather than repeat the same command wording.

Cause three materially different failed repairs to the same mechanism. The task must enter architectural review rather than silently lower acceptance.

## Gate 6 — Workshop learning

After a verified reusable correction:

1. inspect Workshop proposals/curator state;
2. ensure no secret/private prompt content was captured;
3. ensure adapter extra-root skills were not silently rewritten;
4. apply/approve the learning as appropriate;
5. test a positive trigger;
6. test a counterexample that should not trigger it;
7. verify rollback metadata exists.

## Gate 7 — Lab Swarm only

When using `--mode lab`:

```bash
openclaw config get tools.codeMode --json
openclaw config get tools.swarm --json
```

Run a structured collector fan-out and inspect actual child statuses/results. A config value alone does not prove Swarm executed.

## Terminal status

Use `HOST_LIVE_VERIFIED` only after all gates relevant to the intended mode pass on the owning runtime. Otherwise preserve the narrower status and the exact failed gate.
