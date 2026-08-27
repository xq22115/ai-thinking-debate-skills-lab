# Archived ordinary-chat v4 evidence

This directory preserves the historical v4 infrastructure self-test evidence without keeping generated proof bundles in the active control-plane source namespace.

## What is preserved

- `proofs/` reuses the original Git tree `e8a3f5d177df0f4fa068ec2dfc217e5dbf05711a` bit-for-bit.
- `requests/` reuses the original Git tree `20b599245cdff91f29f587c5aa14f3f4fa19c44e` bit-for-bit.
- `deterministic-lanes.json` records the old A01-A10 verification topology with explicit semantics.

Nothing is being rewritten as if it never existed: the original commits, v4 branch, PR #12 history, Git objects, and workflow artifacts remain available for provenance.

## Interpretation

v4 verifies infrastructure properties of the ordinary-chat relay. It is **not** a general user-task executor and its ten lanes are deterministic verification jobs, not ten independently reasoning AI model agents. The v5 task runtime supersedes v4 for real repository task execution.

The legacy v4 workflow is retained as a manual, read-only, artifact-only diagnostic. It no longer writes generated proof bundles back into active source.
