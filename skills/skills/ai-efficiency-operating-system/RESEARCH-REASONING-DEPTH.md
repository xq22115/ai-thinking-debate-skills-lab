# Research & Reasoning Depth Engine

Status: `RC / CANONICAL SUBSYSTEM`
Owner: `ai-efficiency-operating-system`

This subsystem upgrades search/reasoning depth without creating a competing top-level skill alias. It is intentionally subordinate to the canonical task contract, evidence ladder and completion gate.

## 1. Objective

Maximize **decision-relevant information gain** rather than token count, elapsed time, source count or role count.

Depth is real only when work produces at least one of:

- a new causal mechanism;
- a falsified or weakened hypothesis;
- stronger or more direct evidence;
- a discriminating experiment;
- a newly exposed blind spot;
- a tighter failure boundary;
- a materially better action choice.

Waiting, polling, duplicate searching, paraphrase accumulation and verbosity do not count as depth.

## 2. Research contract

Before deep research, compile:

- `RESEARCH_QUESTION`
- `DECISION_TO_SUPPORT`
- `CLAIMS_TO_PROVE`
- `CLAIMS_TO_FALSIFY`
- `FRESHNESS_REQUIREMENT`
- `SOURCE_CLASSES_REQUIRED`
- `KNOWN_UNKNOWNS`
- `STOP_CONDITIONS`
- `INCOMPLETE_EVIDENCE_POLICY`

The research contract is subordinate to `PRIMARY_TASK / ROOT_GOAL / HARD_CONSTRAINTS / ACCEPTANCE_TESTS` and may not silently redefine them.

## 3. Query decomposition

Do not rely on one large search query. Build a query graph with distinct lanes:

1. **Direct answer lane** — exact user question, exact product/feature/version.
2. **Mechanism lane** — architecture, implementation, protocol, root cause.
3. **Primary-source lane** — official docs, specs, changelogs, source code, issues, commits, release notes.
4. **Freshness lane** — latest version, dated changes, deprecations, renamed features, compatibility changes.
5. **Failure lane** — bugs, regressions, limitations, unsupported cases, outage reports.
6. **Counterevidence lane** — evidence that would make the current leading answer wrong.
7. **Alternative-path lane** — materially different methods that still satisfy the same goal.
8. **Runtime-proof lane** — live behavior, read-back, exact revision, actual host/runtime evidence when relevant.

Queries should branch only when they test different hypotheses or source classes. Semantic duplicates are collapsed.

## 4. Four-pass default research loop

For substantive research, use this default loop unless the task clearly needs less or more:

### Pass A — Broad map
Identify the vocabulary, current names, versions, major source families and plausible answer space.

### Pass B — Blind-spot expansion
Search for missing dimensions, renamed concepts, hidden constraints, adjacent failure modes and alternative terminology.

### Pass C — Falsification / adversarial pass
Actively search for counterexamples, regressions, unsupported environments, conflicting primary evidence and reasons the leading conclusion may fail.

### Pass D — Cross-verification
Resolve the highest-impact conflicts with stronger/directer evidence. Prefer exact-source and exact-version proof over consensus summaries.

A fifth pass is justified only if a material claim remains unresolved and another search/test has positive expected information gain.

## 5. Freshness and naming gate

Every material external fact that can drift must carry:

- source date or version;
- verification date;
- exact product/repository/host identity;
- old/new name mapping when terminology changed;
- deprecation/replacement status;
- compatibility scope.

Rules:

- newer is not automatically more authoritative;
- undated pages cannot prove current behavior when currentness matters;
- a current marketing page cannot override a contradictory current spec/runtime observation;
- renamed or superseded features must be normalized to the current canonical name while preserving aliases for searchability;
- stale paths, dead project names and obsolete route instructions are retired from the active path, not merely annotated.

Lifecycle labels:

`CURRENT / CURRENT_WITH_COMPAT / STALE_REFERENCE_ONLY / SUPERSEDED / INVALID`

Only `CURRENT` and `CURRENT_WITH_COMPAT` may drive new implementation by default.

## 6. Evidence independence

Source count is not evidence independence.

Cluster sources by likely common origin:

`original_source × reporting_lineage × vendor_family × evidence_route`

Multiple articles that repeat one announcement are one corroboration family.

For material claims, prefer:

- at least two independent evidence families;
- three when a claim is high-impact, disputed or controls an irreversible action;
- at least one primary/direct source when such a source exists.

If evidence is insufficient, emit `INCOMPLETE_EVIDENCE` for that claim rather than filling the gap with confidence language.

## 7. Source-class priority

Default preference order, adjusted by question type:

1. owning-runtime read-back / deterministic reproduction;
2. current official specification or first-party implementation;
3. exact repository source, issue, PR, commit, release/changelog;
4. authoritative vendor/product documentation;
5. high-quality independent technical analysis;
6. community experience for discovery and failure-pattern detection;
7. secondary summaries only for orientation.

Do not use lower-ranked sources to overrule stronger direct evidence without a specific reason.

## 8. Claim ledger

Track important claims as records:

- `claim_id`
- claim text
- importance
- support evidence
- refute evidence
- freshness status
- provenance cluster
- evidence level `E0–E6`
- unresolved conflict
- next discriminating action

The final answer should be generated from the claim ledger, not from whichever source was read last.

## 9. Hypothesis discipline

Maintain materially different hypotheses, not cosmetic variants.

Each hypothesis should include:

- mechanism;
- predictions;
- evidence for;
- evidence against;
- discriminating observation/test;
- current status.

Status:

`ACTIVE / WEAKENED / FALSIFIED / DOMINANT / UNKNOWN`

Never convert lack of counterevidence into proof.

## 10. Research stop rule

Stop collecting sources when one of these is true:

- acceptance-critical claims have sufficient evidence;
- the next best action is a runtime test/read-back with higher information gain;
- remaining uncertainty cannot change the recommended action;
- new sources are overwhelmingly duplicates;
- the task's evidence budget is exhausted and remaining gaps are explicitly labeled.

Do **not** stop merely because a preselected number of sources or minutes has elapsed.

## 11. Depth budget

Allocate effort by expected impact:

- `P0`: acceptance-critical / irreversible / security-or-loss relevant claims;
- `P1`: architecture and root-cause claims affecting the chosen route;
- `P2`: supporting detail;
- `P3`: nice-to-know context.

Deep research concentrates on P0/P1. P2/P3 are compressed or omitted when they do not change the decision.

## 12. Search-to-action bridge

Research is incomplete until it changes one of:

- chosen implementation path;
- rejected path list;
- target identity;
- required compatibility guard;
- test plan;
- rollback plan;
- completion evidence.

If research cannot affect any downstream decision, it is likely ornamental and should be stopped.

## 13. Anti-patterns to retire

Retire these patterns from active use:

- "search longer" without a new hypothesis or source class;
- fixed-time waiting as proof of deeper reasoning;
- fixed-source-count completion as a universal rule;
- counting mirrored/reposted sources as independent;
- using a newer blog post to override exact runtime evidence;
- preserving obsolete product names or dead repository paths as current instructions;
- spawning many reviewers who share the same evidence route and calling it consensus;
- treating GitHub search hit, tool success, CI pass, file presence or agent self-report as task completion;
- continuing research after a decisive read-back would be more informative.

## 14. Integration with sibling skills

Use existing specialist skills rather than duplicating them:

- `evidence-gap-research` owns claim/evidence closure;
- `competing-hypotheses` owns causal alternatives and discriminating tests;
- `root-cause-clustering` owns shared-mechanism grouping;
- `compatibility-audit` owns host/OS/version/permission compatibility;
- `multi-agent-deliberation` is activated only when independent lanes add marginal information;
- `completion-gate` owns terminal truth claims;
- `recoverable-state` owns checkpoints for long-horizon work.

This file defines orchestration and research-depth policy; it does not duplicate those skills' full procedures.

## 15. Minimum output state for deep research

Persist or report, as appropriate:

- research question and decision target;
- current canonical names/versions;
- query lanes actually used;
- dominant and falsified hypotheses;
- strongest support and refute evidence;
- freshness/compatibility status;
- unresolved `INCOMPLETE_EVIDENCE` claims;
- next action or justified stop condition.

## 16. Promotion gate

This subsystem should not be treated as stable solely because it reads well. Promote only after regression tests demonstrate that it:

- improves factual/current accuracy;
- reduces duplicate-source inflation;
- catches stale names/paths;
- improves root-cause discrimination;
- does not increase false completion;
- does not force unnecessary browsing on simple tasks;
- does not reduce answer quality through over-research;
- preserves user corrections and task scope.
