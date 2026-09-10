---
name: executive-research
description: Use when current, uncertain, conflicting or technical evidence matters; when deeper reasoning, root-cause diagnosis, temporal/version analysis, counterevidence, or broad source triangulation can change the decision.
---

# Executive Research

Depth means decision-relevant information gain, not more tokens, sources, roles or elapsed time.

## Select a research mode

- `NO_SEARCH` — stable logic/facts are sufficient and retrieval cannot change the decision.
- `TARGETED` — one or two decisive unknowns.
- `BROAD` — several hypotheses/source families.
- `FORENSIC` — contradictions, version drift, sparse indexing or high-impact root cause.

## Depth governor

Maintain a compact ledger of competing hypotheses, decisive unknowns, cheapest discriminators, missing gate evidence, counterexamples and version/time/surface uncertainty.

Open another branch/round only if it is expected to create a **MATERIAL DELTA**: advance a gate; discriminate a hypothesis; expose a shared upstream cause; add independent decision-changing evidence; resolve a version/time contradiction; reveal a regression/counterexample; or change the feasible action set while preserving constraints.

After two materially equivalent no-delta attempts, change the discriminator, source family, time slice, tool, hypothesis or reviewer. Do not rephrase the same search.

## Evidence graph

Track support/refute/context-only, authority, date/version/surface, lineage/origin, independence, freshness/supersession and the obligation affected. Mirrored reports of one origin are one corroboration family.

Choose source authority **by the claim being tested**, not by a universal prestige order:

- target behavior / “does it actually work here?” → owning-runtime observation and reproducible postcondition/read-back;
- implementation mechanism → exact source code, commit/blob, package/manifest and maintainer implementation evidence;
- operational failure modes → high-signal independent practitioner/tooling evidence, issue/PR reproductions and maintainer discussions;
- documented support and normative semantics → current official product/developer documentation;
- popularity or copied recipes → discovery signals only, never proof.

Official documentation alone must not be promoted into execution proof. Likewise, community or third-party reports alone must not be promoted into target-runtime proof. If official guidance says a path is unsupported but exact current runtime evidence demonstrates it, report the distinction as `unsupported/undocumented but observed working` rather than rewriting either side. If an actually enforced authorization/platform boundary blocks the path, record the concrete boundary and continue evaluating other allowed mechanisms instead of generalizing one blocked route into universal impossibility.

For GitHub and other indexed code systems, a zero-result search is not proof of absence. If exact owner/repository/path/ref or another independent locator exists, pivot to exact lookup, direct fetch, tree/contents, manifest, release/tag, or other causally distinct resolution before closing the hypothesis. Keep search-hit revision, repository HEAD, file/blob revision, package/marketplace version and installed revision separate.

For evolving systems, distinguish event, publication, effective, observed and version time. Search origin → transition → current rather than only newest-first.

## Root-cause requirement

When the same symptom recurs across commands, repositories, tools, versions, or retries, stop patching the visible error one occurrence at a time. Build the smallest causal model that can explain the shared failures, such as target-identity drift, stale discovery/indexing, version-state collapse, configured-vs-loaded layer collapse, persistence false positives, permission/entitlement drift, dependency failure, or a broken verification mechanism. A proposed root cause must predict at least one discriminating test; otherwise it remains a hypothesis.

Read `references/deep-task-integrity.md` for the full search map and research audit. For AI models, agent harnesses, plugins, MCP/tooling, desktop AI clients, skills or eval systems, read `references/ai-ecosystem-recon.md`. Read `references/strict-deeplock-profile.md` only when the user explicitly selects the strict profile.
