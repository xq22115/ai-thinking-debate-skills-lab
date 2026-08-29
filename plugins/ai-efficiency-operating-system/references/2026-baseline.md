# 2026 baseline and borrowed mechanisms

Verification date: 2026-08-29.

This package borrows mechanisms, not prose, and keeps internal/user-specific acceptance rules separate from external framework claims.

## OpenAI

- **Plugins in ChatGPT and Codex**: as of 2026-07-09, Plugin Directory is the cross-product discovery model; plugins can be skills-only and are available in ChatGPT web/desktop and Codex subject to plan/workspace/surface controls.
- **GitHub marketplace import**: current OpenAI guidance supports workspace import/sync from `.agents/plugins/marketplace.json`; repository sync does not prove installation or grant underlying app permissions.
- **openai/plugins**: current official packaging uses `.codex-plugin/plugin.json`, `skills/`, optional per-skill `agents/openai.yaml`, and plugin-eval tooling.
- **plugin-eval**: static/package analysis, benchmark and comparison are useful but remain distinct from live host activation.

## Mature skill frameworks

- **obra/superpowers**: skill creation is treated like TDD; observe baseline failure, write the smallest effective skill, rerun pressure cases, refactor. Frequently loaded skills are kept thin; heavy material moves to references/scripts.
- **addyosmani/agent-skills**: skills are specific, verifiable and minimal; lifecycle ownership and trigger regression matter; current repo supports Codex/Antigravity and other Agent Skills runtimes.
- **garrytan/gstack**: many narrow opinionated skills rather than one universal prompt; host-specific/domain knowledge is persisted as scoped skill data rather than a self-modifying global runtime.
- **OthmanAdi/planning-with-files**: persistent working state survives compaction/restart; install route matters because a skill can be present while lifecycle hooks are absent. Its later security analysis also demonstrates that repeatedly reinjecting writable planning state can amplify untrusted instruction-like content, so durable findings and authoritative control state must stay separated.
- **Tencent/SkillHone**: optimize the whole skill folder, not only `SKILL.md`; keep eval and skill data separated; record changes as reviewable Git artifacts; gate promotion on held-out validation.
- **Microsoft SkillOpt**: treat skill text as trainable external state; use bounded add/delete/replace edits, a held-out strict-improvement gate, rejected-edit feedback and slow/meta updates instead of unbounded self-rewriting.
- **SkillsBench**: large paired evaluation shows curated skills can help on average while still harming a non-trivial subset of tasks; focused 2–3-module skills outperform comprehensive documentation and self-generated skills do not provide reliable average gains. This supports narrow composition plus negative routing, not universal activation.
- **Anthropic official plugin/skill-development guidance**: focused triggers, progressive disclosure, references/scripts for heavy detail, explicit activation testing and low trigger overlap.

## 2026 research constraints

- Multi-agent debate can converge on shared error; diversity and isolated first-pass evidence are more important than raw seat count.
- Tool availability is not monotonic utility; irrelevant/distracting tools can reduce performance, so tools are demand-loaded.
- Skill usefulness is task/model/harness dependent; a positive aggregate benchmark cannot justify enabling every skill on every task.
- Self-evolving skill pools can accumulate contamination; promotion needs pre-commit evaluation, bounded edits, independent/held-out validation, rejected-change history and rollback.
- Persistent working memory improves recovery only when the actual host supplies the persistence/reinjection mechanism; reinjected writable state must not become an authority-escalation channel.

## Internal validated lineage

The package also incorporates prior validated user artifacts:

- Executive Harness v1.0.0 — 54/54 local tests, 8/8 lint, deterministic routing corpus, distribution parity; live ChatGPT trigger remained unproven.
- Deep Task Integrity — adaptive depth, temporal breadth, search/evidence graph and two-no-delta pivot.
- DeepLock V2.1 — authority separation, real worker identity, evidence-family accounting, strict external completion gate.
- ARR v1.3 — logical/control/effect-delivery/temporal-witness separation and durable effect semantics.

None of those historical local results are upgraded into current ChatGPT Desktop `HOST_LIVE` evidence without a fresh live probe.
