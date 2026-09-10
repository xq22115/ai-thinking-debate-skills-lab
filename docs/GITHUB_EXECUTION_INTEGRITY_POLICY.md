# GitHub Execution Integrity Policy

This policy prevents false completion, symptom-only patching, version confusion, weak verification, and one-shot GitHub tool failures from being reported as finished work.

It applies to GitHub repository discovery, code/file retrieval, plugin or skill installation, dependency pulls, branch/file writes, pull requests, workflow verification, and any task whose result depends on persisted GitHub state.

## 1. Primary rule: outcome over tool-call ceremony

A successful API/tool response is only evidence that one operation returned successfully. It is not evidence that the user's requested outcome exists at the target runtime.

For material GitHub work, completion requires an end-to-end chain:

`target identity -> source resolution -> exact revision -> execution/write -> read-back -> behavior test -> adversarial/regression check -> release`

Any missing stage remains `NOT_RUN` or `BLOCKED`; it must never be silently relabeled `PASS`.

## 2. System invariants

Before changing anything, declare the applicable invariants. After the change, test them again on the exact reported revision.

### GI-01 Existing capability preservation
Existing working behavior must not disappear unless the user explicitly requested its removal.

### GI-02 No silent permission downgrade
Repository, branch, app, workflow, token, or tool permissions must not be silently reduced as a side effect of a repair. If effective permissions cannot be read back, permission preservation remains unknown rather than assumed.

### GI-03 Input/output contract stability
Inputs, outputs, file paths, names, schemas, tool parameters, exit/status semantics, and externally consumed formats must remain compatible unless a deliberate migration is part of the accepted goal.

### GI-04 Failure detectability
Failures must be observable through a non-zero result, explicit error state, failed criterion, log, or other inspectable evidence. A swallowed failure, partial success presented as success, or ambiguous result cannot pass.

### GI-05 Success requires read-back
A create/update/install action is not proof of persistence. The resulting state must be independently read back from the target branch/revision/runtime and compared with the intended state.

### GI-06 Local changes must preserve adjacent paths
A repair must not break other supported routes, callers, agents, installation targets, or workflows. At minimum, run focused regression checks for the paths causally adjacent to the change.

### GI-07 Rollback must remain available
Material writes should occur on a rollback-friendly branch or otherwise retain the exact pre-change revision. The rollback target must be recorded before the first material mutation.

### GI-08 Exact-revision evidence
Tests and read-backs must identify the exact branch/commit/file/blob or target installation state they verified. Evidence from a stale search result, different branch, cached file, or unrelated green workflow cannot satisfy the criterion.

### GI-09 Search miss is not absence
A zero-result repository/code search cannot by itself prove that a repository, file, skill, plugin, branch, or feature does not exist. Use a causally distinct fallback such as exact repository lookup, direct path fetch, tree/contents lookup, or known URL/ref resolution before concluding absence.

### GI-10 Configuration is not runtime activation
Keep these states distinct: `configured -> registered -> loaded -> executed -> observable effect`. Evidence at a lower layer cannot be promoted to a higher layer without a test at that layer.

### GI-11 Write success is not task success
A commit SHA, file-write response, PR creation, or installer exit code proves only that the operation occurred. It does not prove the target skill/plugin/tool is usable.

### GI-12 Technical feasibility is evidence-bound
Official documentation and product statements are useful evidence, but they do not replace runtime verification. For technical feasibility, distinguish `documented/supported`, `observed working`, `unsupported but observed`, and `blocked by an actually enforced boundary`. Never translate `not documented` or one failed route into `impossible` without corroborating evidence. Higher-priority platform, authorization, and safety constraints remain binding.

## 3. Root-cause model for recurring GitHub failures

Treat the following as separate failure classes instead of patching the visible symptom:

1. **Target identity drift** — wrong account, organization, repository, branch, workspace, or local installation target.
2. **Discovery false negative** — search ranking/indexing/query behavior misses an object that direct lookup can resolve.
3. **Version-state collapse** — repository HEAD commit, search-hit commit, file blob SHA, release/tag version, marketplace/package version, and locally installed revision are treated as if they were one value.
4. **Layer collapse** — configured/registered/loaded/executed/observable are treated as equivalent.
5. **Persistence false positive** — a write/install command returns success but the expected bytes/state cannot be read back.
6. **Happy-path bias** — one normal run passes while retries, stale state, ordering, permissions, network loss, dependency failure, or partial failure break the workflow.
7. **Single-authority lock-in** — a single document, search result, issue comment, or model conclusion is allowed to decide feasibility without target evidence.
8. **Stagnant retry** — the same causal mechanism is retried with cosmetic changes after it has already failed twice.

A repair is root-cause-level only when it changes the mechanism that produced the failure and adds a regression barrier that would catch recurrence.

## 4. Source and evidence triangulation

For version-sensitive, repeatedly failing, or material GitHub tasks, use more than one evidence family when practical:

- target runtime or owning installation read-back;
- exact GitHub object identity and revision metadata;
- source repository files, commits, manifests, releases, and workflow state;
- maintainer discussions, issue/PR evidence, or implementation source;
- high-signal third-party practitioner/tooling evidence that exposes real operational behavior;
- official documentation for supported semantics and stated constraints.

No single source family is sufficient for a material `PASS` when another independent source or runtime check is practical. Popularity alone is not proof. Official documentation alone is not execution proof. Third-party instructions alone are not execution proof.

When sources conflict, record the conflict and choose a discriminating runtime/revision test. If the evidence shows a technique works but is undocumented, report it as such rather than calling it officially supported.

## 5. Repository and file retrieval algorithm

When pulling a repository, file, plugin definition, or skill:

1. Resolve the exact target owner/repository; do not rely only on ranked repository search.
2. Read repository metadata and record the default branch and effective permissions.
3. Resolve the target path by exact path, code search, tree/contents, or manifest lookup.
4. Record four different identifiers when applicable:
   - repository/default branch;
   - current HEAD commit SHA;
   - source path and file blob SHA;
   - release/tag/package/marketplace version.
5. Fetch the complete target file from the intended ref.
6. For skills/plugins, verify both the implementation file (for example `SKILL.md`) and the registration/manifest entry when one exists.
7. If a wrapper CLI or marketplace is involved, cross-check its resolved repository/path against the source repository rather than assuming identical naming semantics.
8. If reproducibility matters, pin a tag or commit SHA instead of implicitly following a moving default branch.
9. After installation/pull into an owning runtime, read the installed target back and compare the source identity/content/version.

A search hit pinned to an older commit and a direct fetch of current `main` are different evidence. Never combine them into one undifferentiated “latest version”.

## 6. Write and repair algorithm

For a material GitHub change:

1. Record the base commit and rollback target.
2. Fetch every file that will be modified and record its current blob SHA.
3. Prefer an isolated branch for non-trivial repairs.
4. Make the smallest causal change that satisfies the declared acceptance contract.
5. Read every changed file back from the exact branch.
6. Compare intended content with returned content and verify that the blob/commit changed where expected.
7. Compare the repair branch with the base revision and inspect the complete changed-file set.
8. Run focused tests for the requested behavior on the exact repair revision.
9. Run invariant and adjacent-path regression checks.
10. Trigger/inspect CI or an equivalent target-runtime verifier when available.
11. Only after evidence is attached to every hard criterion may the change be released or merged.

Do not use “commit created”, “PR opened”, or “CI is green” as a substitute for the requested behavior test.

## 7. Skill/plugin installation algorithm

A skill/plugin pull is complete only when all applicable layers pass:

1. **Source resolved** — exact repository and path exist.
2. **Registration resolved** — marketplace/plugin manifest points to the intended skill when registration is required.
3. **Version resolved** — source commit/tag/blob and wrapper/marketplace version are not conflated.
4. **Installed** — bytes or package state are written to the intended target.
5. **Read back** — installed target can be inspected and matches the intended source identity.
6. **Discovered/registered** — the owning agent/runtime lists or loads it through the expected mechanism.
7. **Executed** — a representative request actually invokes the skill/tool.
8. **Observable effect** — the requested behavior proves the correct skill/tool path was used.
9. **Regression** — existing skills/tools and permissions still work.

If the current environment can only prove layers 1-3, report exactly that. Do not claim installation or activation.

## 8. Adversarial scenario matrix

For material changes, choose every scenario that can realistically falsify the mechanism; do not run scenarios as ceremony when they cannot affect the result.

Required scenario families:

- normal valid input;
- invalid input;
- empty or missing input;
- idempotent/repeated execution;
- rapid consecutive operations;
- reordered operations or out-of-order state;
- permission loss or scope reduction;
- network interruption/timeout/retry;
- dependency unavailable or version mismatch;
- stale cache/state/old installation residue;
- partial success followed by failure;
- stale search/index result versus direct lookup;
- exact-revision mismatch between test and reported state;
- rollback and recovery path.

For each chosen scenario record: precondition, action, expected result, actual result, evidence, and whether any invariant was violated.

## 9. Tool-call maturity requirements

GitHub tool usage must obey these rules:

- Prefer exact identifiers over fuzzy search once the target is known.
- When search fails but an exact owner/repo or URL is available, immediately pivot to exact lookup.
- Do not retry the same search wording repeatedly after two materially similar failures; change the retrieval mechanism.
- Distinguish read permissions from write/admin permissions using returned repository metadata.
- Before update/delete, fetch the current blob SHA from the same target branch.
- Never parallelize writes to the same path when later writes depend on the prior content SHA.
- After every material write, perform read-back before claiming persistence.
- When a workflow is used as verification, identify the exact run/commit and inspect its conclusion; unrelated historical green runs do not count.
- If a tool response is truncated, fetch the specific file/path/range needed instead of inferring from the truncated payload.

## 10. Release gate

Allowed statuses are:

- `PASS` — all hard criteria and applicable invariants are satisfied on the exact reported state; required negative/regression tests ran; no contradictory evidence remains.
- `FAIL` — a required behavior or invariant test failed; continue root-cause repair when possible.
- `BLOCKED` — a concrete external dependency prevents further progress; preserve evidence and exact next action.
- `NOT_RUN` — required verification was not executed; never relabel as `PASS`.

A repair that makes one symptom disappear while degrading an invariant is `FAIL`, even if the primary happy-path test passes.
