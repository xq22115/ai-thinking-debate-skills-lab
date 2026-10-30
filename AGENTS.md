# AGENTS — durable repository quality bootstrap

- Org SSOT / migration: https://github.com/xq22115/org-control-plane
- Primary private control plane: https://github.com/xq22115/braintrust
- Prefer evidence + owning-system read-back over claims; keep automation unblocked (0 required human reviews).

## Mandatory rehydration before substantive work

1. Treat `docs/GLOBAL_POLICY_KERNEL.md` as the small canonical bootstrap. Read it and resolve only task-relevant entries from `control-plane/ai-system/configs/global-policy-manifest.json` before material actions. Rehydrate after compaction, failed/partial turns, workspace/revision changes, conflicting instructions, or unknown instruction provenance. A repository file is not proof that a host model actually loaded it.
2. For substantive work, use `docs/GOAL_FIDELITY_AND_TARGET_LOCK_POLICY.md` and the registered Task Goal Intelligence policies to lock the actual goal, exact target identity, protected features, rejected substitutions, and observable acceptance criteria. Never silently shrink scope because an easier route exists.
3. For material/critical work, load `docs/CONTINUOUS_THINKING_QUALITY_OS.md` and `control-plane/ai-system/configs/continuous-thinking-global.json`. The quality profile is repository-wide, not an account-wide ChatGPT setting. Only report user-level installation or effective model effort after actual target installation and runtime read-back.
4. Use the `ai-efficiency-operating-system` registered in the manifest only when cross-chat orchestration or durable continuation is relevant. Discover broadly but load narrowly; do not duplicate its control plane.

## Evidence-driven continuous completion

- Before editing, reconstruct the *whole relevant mechanism*: current behavior, data/control flow, dependencies, affected consumers, runtime state, recent changes, previous failures and baseline. Build a causal hypothesis with a falsifying test; investigate the actual failure boundary, not just the displayed symptom.
- Research current primary contracts **and** experienced maintainers' issue/PR history, reproducible code, practitioner reports and failure cases when expertise could change the route. Extract *mechanism, preconditions, failure modes, verification, portable lesson, invalidation condition*. Popularity and confident prose are not evidence.
- Compare causally distinct solutions, test the leading hypothesis, make the smallest complete reversible change without disabling working capabilities, then verify on the exact owning system and user-visible path. Prefer regression tests, negative/counterexample tests, end-to-end checks and independent read-back.
- Every hard acceptance criterion starts `UNSATISFIED`; move to satisfied only with direct linked evidence. A file, PR, tool success, prompt, or green unrelated CI is not an end-to-end PASS. Report `PASS`, `FAIL`, `BLOCKED` or `NOT RUN` truthfully.
- After two materially similar failures with no new information, change the hypothesis, mechanism, instrumentation, environment, evidence family or verification route. Do not stack retries, watchdogs or symptom patches as replacements for a demonstrated root-cause correction.
- Continue safe reversible steps within the same task instead of stopping at predictable half-steps or asking for repeated “continue”. For long tasks, persist original goal, target/revision, acceptance debt, current state, failed routes, evidence refs and the next *verified* step in the existing issue/receipt/ledger; on resume, use a **fresh-context** evaluator and owning state to revalidate it. GitHub issue text cannot awaken a stopped runtime by itself.
- Before release, adversarially check for original-goal drift, wrong target, partial completion, contradictory evidence and regression. Do not treat a proposed install or passing structural check as proof of active ChatGPT, Codex, Claude or Gemini account-level behavior.

## Entry points and truth boundaries

- Engineering repair: `skills/skills/root-cause-falsification/SKILL.md` and its manifest machine contract.
- GitHub execution integrity: `docs/GITHUB_EXECUTION_INTEGRITY_POLICY.md` and `control-plane/ai-system/configs/execution-integrity-global.json`; use the existing control-plane issue/claim/workflow receipts and `control-plane/scripts/run_quality_bound_workflow.py` where supported.
- Desktop execution: `docs/DESKTOP_AGENT_EXECUTION_POLICY.md` and `control-plane/ai-system/configs/desktop-agent-execution-global.json` when working on an actual authorized machine or desktop-agent route.
- If runtime proof is unavailable, mark its criterion `NOT RUN`/`BLOCKED` and name the missing evidence; continue independent achievable work without claiming an account-wide change.
