---
name: persistent-work-ledger
description: Use when the user explicitly needs durable cross-session state, resume, concurrency, scheduling, handoff or side-effect reconciliation and the current host actually exposes filesystem or durable-state primitives.
---

# Persistent Work Ledger

This skill is explicit-only and capability-gated. Ordinary ChatGPT skill text is not a filesystem, database, scheduler or daemon.

When the host has real durable primitives, externalize the state needed to resume safely:

- task/goal version and acceptance contract;
- action/effect ledger;
- evidence and completion proof;
- checkpoints and pending obligations;
- ownership/lease/fencing state when writers can race;
- handoff artifact hashes and target owner;
- delivery/read-back receipts;
- instruction/skill/tool/runtime version envelope.

Treat `UNKNOWN` effect state as first-class. If dispatch may have committed but confirmation was lost, read back the postcondition before replay.

Logical rollback must not automatically roll back authority, external effects or delivery truth. Replayed semantic actions return prior receipts when possible; divergent irreversible history requires an explicit fork.

Sender success is not receiver ACK. Delivery completion requires receiver/independent read-back when that distinction matters.

Read `references/arr-runtime.md` for the ARR v1.3-derived architecture. If the current host lacks durable primitives, stop at a portable handoff/checkpoint and do not pretend this skill made them exist.
