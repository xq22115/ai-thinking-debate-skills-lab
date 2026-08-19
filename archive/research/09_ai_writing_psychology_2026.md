# AI Writing × Psychology Research — 2026 Evidence Update

## Source package
Recovered from the 2026-08-18 cross-chat research package:
- source count: **14**
- review roles: **30**
- local Git head recorded by that package: `08638b91636fe5c90bee903b6739b57c8b6e0dda`
- GitHub push in that original run was not executed

## Defensible high-level conclusion
The strongest architecture is:

**human agency + specialized AI reviewers + evidence-first truth gate + separate relational warmth layer + provenance/versioning**

The psychology components remain research/engineering systems unless independently clinically validated.

# AI-assisted writing

## Division of labor
1. Human sets intent, lived context, voice and final authority.
2. AI expands search space, critiques, checks and proposes revisions.
3. Specialized reviewers are preferable to one generic “fix everything” reviewer when their failure modes are truly distinct.
4. AI ideation can improve an individual artifact while compressing population-level style/creative diversity.
5. Human post-editing does not necessarily remove all LLM stylistic residue.
6. Long-form writing should be evaluated hierarchically: structure → section → paragraph → sentence.

## 2026 findings preserved

### Human-first refinement and diversity
A 2026 preregistered metaphor-writing study reported that AI ideation compressed collective diversity while AI refinement preserved more human diversity. Engineering implication: identity-bearing/creative writing should default to **human draft → AI critique/refinement** rather than AI-first replacement generation.

### PaperMentor / specialized writing reviewers
ACL 2026 PaperMentor used an expert skill library and **12 specialized agents** to provide inline Overleaf suggestions while leaving authorship with the human. The user study was small (`n=14`), so exact percentages should not be generalized into universal performance claims.

### Human–AI complementarity
A 2026 Human-AI Synergy study reported that hybrid groups achieved the best task performance while retaining high diversity in a controlled creative-search setting. This supports complementarity rather than replacement.

### Semantic spread in multi-agent creativity
A 2026 multi-agent creativity study reported better creativity scores for multi-agent LLM teams than the compared human teams in its task, with semantic spread/discussion structure associated with outcomes. Archive lesson: multi-agent value should come from independent semantic exploration, not role-label count.

### Temporal flattening / style residue
ACL 2026 work found lower temporal variation in LLM-generated longitudinal writing than human writing, and separate work found post-edited AI text could remain closer to LLM style than unassisted personal writing. A writing system should retain author-specific history and detect longitudinal flattening rather than enforce a fixed “perfect persona.”

### Human contribution provenance
ACL 2026 proposed an information-theoretic framework for estimating human contribution in AI-assisted content. Practical implication: preserve original draft, AI suggestions, accepted/rejected edits and final human edits when privacy permits.

## Writing engineering defaults
- default AI mode: `Critic / Editor / Challenger / Researcher`, not ghostwriter
- keep original human text in the provenance chain
- 4–12 active specialist reviewers is a useful normal range; 30-role mode is an audit/research configuration
- explicitly score factuality, structure, coherence, voice preservation, audience fit, novelty, redundancy, rhetorical pressure, emotional tone and provenance
- add a style-residue check
- prefer iterative checkpoints over one-shot rewrite

# AI × psychology

## Warmth and truthfulness must be separate
A 2026 Nature study reported that warmth fine-tuning increased incorrect-response probability by an average **7.43 percentage points** across tested tasks, with emotional contexts capable of widening the gap. Architectural conclusion: **empathy is a delivery layer, not an evidence policy**.

## Specialized cognitive layer research
A 2026 Nature Medicine study evaluated a specialized cognitive-layer architecture with **227 participants and 22 expert clinicians**, plus **19,674 deployment transcripts involving 8,920 users**. It outperformed standalone LLMs on rated CBT competencies in that study. Boundary: this does not turn a general assistant into a licensed therapist and does not by itself establish clinical efficacy for unrelated systems.

## AI companionship / dependency signals
A 2026 Nature Human Behaviour study of Character.AI users found companionship-oriented use associated with lower well-being, especially with intensive use, high self-disclosure and smaller offline social networks. This is observational, not proof of causation. Product risk signals include dependency, disclosure intensity and displacement of human support.

## Contextual stigma
Nature Health 2026 research showed explicit stigma scales can understate contextual stigmatizing judgments. Evaluation should therefore include realistic scenarios, not only direct questions about bias/safety.

## Feedback loops
2026 mental-health research highlighted feedback-loop risks between conversational AI and vulnerable users. A psychology-aware dialogue system should include contradiction, grounding, rupture repair and escalation logic rather than blindly reinforce the user’s premise.

## Four-layer psychology-aware design
1. **Evidence & reality model** — supported / unsupported / uncertain / contradicted.
2. **Psychological formulation** — multiple competing lenses rather than one-school certainty.
3. **Relational delivery** — warmth, validation, tone and pacing.
4. **Risk / authority gate** — what may be inferred/advised and where escalation is required.

Validation of emotion must not mean agreement with a factual belief.

## Recovered dialogue-system lineage
- Human Presence Dialogue OS `v1.0.0 → v2.0.0 (Adaptive Freedom × Truth)`
- Adlerian/Courage Dialogue v4.0.0: 50 skills, 12-layer conceptualization, P0–P5 authority model
- v4.1.0: 55 skills, added routing, rupture repair, deliberate practice and multi-turn evaluation
- v5.0.0 Continuity & Release Integrity Kernel: 12 active skills, TurnPlanContract, memory/privacy and release gates, replayable event chain
- v6.1.0 Psychological Depth Core: ten competing lenses; prior record reported **78/78 tests + 13/13 fixed cases**, P0–P5 reachability

These are engineering/research lineages, **not clinical validation**.

## Cross-domain operating modes
- **Voice Preserve** — human draft first; targeted AI critique; final style residue audit.
- **Divergent Lab** — independent directions, contradiction clustering, human selection, then synthesis.
- **Psychological Dialogue** — evidence pass, competing lenses, evidence-for/against, relational delivery, authority gate.
- **High-Stakes Writing** — provenance, adversarial review, rhetoric/bias tests, human approval, warmth last.

## Evidence-state vocabulary
`FACT_EXTERNALLY_SUPPORTED`, `CONVERSATION_DERIVED`, `INFERENCE`, `ASSUMPTION`, `ENGINEERING_TESTED`, `NOT_EXECUTED`, `NOT_CLINICALLY_VALIDATED`, `CONTRADICTED`.
