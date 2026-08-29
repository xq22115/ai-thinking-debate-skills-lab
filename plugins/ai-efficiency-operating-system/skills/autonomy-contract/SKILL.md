---
name: autonomy-contract
description: Use when the user explicitly asks for autonomous or effect-bearing work, broad delegation, unattended execution, or actions whose approval and irreversible boundaries must be fixed before execution.
---

# Autonomy Contract

This skill is explicit-only. It documents authority; it does not create authority.

Before an effect-bearing action record:

- exact objective/goal version;
- target and semantic scope;
- permitted capabilities;
- approval mode and responder;
- irreversible or externally visible effects;
- timeout/cancel behavior;
- rollback/reconciliation path;
- required postcondition.

A plugin, model, tool or delegated agent cannot expand its own authority. "No prompt" does not mean auto-approve. If approval is required but no authorized responder/channel is reachable, surface/block according to the actual host contract rather than waiting forever or silently granting permission.

For retries, use semantic action identity and reconcile ambiguous prior effects before replay. Authority from an older goal version or ownership epoch is stale.

Do not claim background/unattended execution if the host provides no scheduler, durable worker or webhook/condition runtime.
