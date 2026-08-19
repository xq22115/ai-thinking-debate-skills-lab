# Agent Core V4 Live Positive Control

This documentation-only change exists to prove the default-branch `Merge Readiness` workflow runs after V4 bootstrap and accepts a low-risk PR only after its manifest-applicable current-head workflows succeed.

Expected manifest requirements for this repository:

- `PR Risk Router` — always.
- `Core CI` — always.

The proof is valid only when the `Merge Readiness` run reports this PR's exact head SHA and a PASS result after both workflows succeed.
