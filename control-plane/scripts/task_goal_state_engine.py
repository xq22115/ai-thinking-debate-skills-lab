#!/usr/bin/env python3
"""Deterministic support layer for Task Goal Intelligence v2.3.

This module does not try to infer natural-language intent by itself. It enforces the
state transitions that should happen *after* an agent has classified a signal:

- authority is field-sensitive (goal requirements are not mutable runtime facts),
- corrections retract dependent conclusions through a truth-maintenance graph,
- uncertainty classes route to different resolvers,
- competing hypotheses are ranked disconfirmation-first (ACH style),
- source reliability and information credibility are tracked separately,
- rare / dark-web / otherwise unverified evidence may propose hypotheses but cannot
  silently rewrite normative goal fields,
- failed acceptance tests generate counterexamples and reopen dependent assumptions,
- traceability audits reject orphan requirements and orphan actions.

The purpose is to make goal-understanding regressions executable and testable rather
than depending only on prompt wording.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


ACTIVE = "ACTIVE"
OBSOLETE = "OBSOLETE"
INVALIDATED = "INVALIDATED"
NON_BINDING = "NON_BINDING"
CONTRADICTED = "CONTRADICTED"
UNSATISFIED = "UNSATISFIED"

NORMATIVE_TYPES = {
    "root_goal",
    "desired_end_state",
    "hard_constraint",
    "negation",
    "protected_capability",
    "acceptance_test",
}
FACTUAL_TYPES = {
    "target_identity",
    "environment_state",
    "version",
    "runtime_fact",
    "capability_fact",
}
PREFERENCE_TYPES = {"preference"}

USER_AUTHORITIES = {
    "current_user_correction",
    "current_user_explicit",
    "original_user_request",
    "prior_user_explicit",
    "durable_user_preference",
}

NORMATIVE_AUTHORITY = {
    "current_user_correction": 100,
    "current_user_explicit": 95,
    "original_user_request": 90,
    "prior_user_explicit": 85,
    "durable_user_preference": 70,
    "model_inference": 15,
    "summary_cache": 5,
    "owning_runtime_readback": 0,
    "immutable_repo_evidence": 0,
    "external_research": 0,
    "rare_unverified_source": 0,
}

FACTUAL_AUTHORITY = {
    "owning_runtime_readback": 100,
    "immutable_repo_evidence": 92,
    "current_user_explicit": 82,
    "current_user_correction": 82,
    "canonical_spec": 78,
    "independent_primary_evidence": 74,
    "external_research": 60,
    "durable_user_preference": 25,
    "original_user_request": 25,
    "summary_cache": 10,
    "model_inference": 5,
    "rare_unverified_source": 3,
}

PREFERENCE_AUTHORITY = {
    "current_user_correction": 100,
    "current_user_explicit": 95,
    "durable_user_preference": 85,
    "original_user_request": 80,
    "prior_user_explicit": 75,
    "summary_cache": 20,
    "model_inference": 10,
    "external_research": 0,
    "owning_runtime_readback": 0,
    "rare_unverified_source": 0,
}

GENERAL_AUTHORITY = {
    "current_user_correction": 100,
    "current_user_explicit": 95,
    "owning_runtime_readback": 90,
    "original_user_request": 88,
    "immutable_repo_evidence": 85,
    "prior_user_explicit": 82,
    "independent_primary_evidence": 78,
    "durable_user_preference": 72,
    "canonical_spec": 70,
    "external_research": 55,
    "summary_cache": 15,
    "model_inference": 10,
    "rare_unverified_source": 5,
}

UNCERTAINTY_RESOLVERS = {
    "specification": "current_user_or_explicit_task_contract",
    "target_identity": "owning_runtime_or_repository_identity_readback",
    "environment_state": "owning_runtime_readback",
    "capability": "harmless_capability_probe_or_executable_test",
    "evidence": "independent_corroboration_and_source_grading",
    "model": "competing_hypotheses_holdout_or_fresh_context_evaluator",
    "temporal": "fresh_timestamped_source_or_runtime_readback",
}

RELIABILITY_WEIGHT = {"A": 1.00, "B": 0.86, "C": 0.68, "D": 0.45, "E": 0.18, "F": 0.30}
CREDIBILITY_WEIGHT = {1: 1.00, 2: 0.82, 3: 0.62, 4: 0.38, 5: 0.14, 6: 0.28}
ORIGIN_WEIGHT = {
    "owning_runtime": 1.00,
    "primary": 0.96,
    "independent_reproduction": 0.94,
    "maintainer": 0.90,
    "practitioner": 0.82,
    "long_tail": 0.62,
    "darkweb_or_unverified": 0.34,
    "summary": 0.22,
    "model_inference": 0.16,
}


@dataclass
class GoalNode:
    node_id: str
    key: str
    value: Any
    field_type: str
    authority: str
    source_id: str | None = None
    depends_on: set[str] = field(default_factory=set)
    status: str = ACTIVE
    metadata: dict[str, Any] = field(default_factory=dict)
    invalidated_by: str | None = None


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    reliability: str = "F"
    credibility: int = 6
    origin: str = "long_tail"
    corroborated: bool = False
    relations: dict[str, str] = field(default_factory=dict)

    def weight(self) -> float:
        r = RELIABILITY_WEIGHT.get(self.reliability.upper(), RELIABILITY_WEIGHT["F"])
        c = CREDIBILITY_WEIGHT.get(int(self.credibility), CREDIBILITY_WEIGHT[6])
        o = ORIGIN_WEIGHT.get(self.origin, 0.5)
        corroboration = 1.12 if self.corroborated else 1.0
        return round(min(1.0, r * c * o * corroboration), 6)


@dataclass
class TransitionResult:
    accepted: bool
    node_id: str | None = None
    invalidated: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    reason: str = ""


class GoalState:
    """Small assumption-based truth-maintenance graph for goal state."""

    def __init__(self) -> None:
        self.nodes: dict[str, GoalNode] = {}
        self.active_by_key: dict[str, str] = {}
        self.dependents: dict[str, set[str]] = {}
        self.contradictions: list[str] = []
        self.events: list[dict[str, Any]] = []

    @staticmethod
    def authority_score(field_type: str, authority: str) -> int:
        if field_type in NORMATIVE_TYPES:
            return NORMATIVE_AUTHORITY.get(authority, 0)
        if field_type in FACTUAL_TYPES:
            return FACTUAL_AUTHORITY.get(authority, 0)
        if field_type in PREFERENCE_TYPES:
            return PREFERENCE_AUTHORITY.get(authority, 0)
        return GENERAL_AUTHORITY.get(authority, 0)

    @staticmethod
    def resolver_for(uncertainty_kind: str) -> str:
        try:
            return UNCERTAINTY_RESOLVERS[uncertainty_kind]
        except KeyError as exc:
            raise ValueError(f"unknown uncertainty kind: {uncertainty_kind}") from exc

    def _register(self, node: GoalNode) -> None:
        self.nodes[node.node_id] = node
        for parent in node.depends_on:
            self.dependents.setdefault(parent, set()).add(node.node_id)

    def _reject(self, message: str) -> TransitionResult:
        self.contradictions.append(message)
        return TransitionResult(False, contradictions=[message], reason=message)

    def _invalidate_cascade(self, node_id: str, by: str, root_status: str = OBSOLETE) -> list[str]:
        invalidated: list[str] = []
        stack: list[tuple[str, bool]] = [(node_id, True)]
        seen: set[str] = set()
        while stack:
            current, is_root = stack.pop()
            if current in seen or current not in self.nodes:
                continue
            seen.add(current)
            node = self.nodes[current]
            node.status = root_status if is_root else INVALIDATED
            node.invalidated_by = by
            if self.active_by_key.get(node.key) == current:
                self.active_by_key.pop(node.key, None)
            invalidated.append(current)
            for child in sorted(self.dependents.get(current, set())):
                stack.append((child, False))
        return invalidated

    def apply_signal(
        self,
        *,
        node_id: str,
        key: str,
        value: Any,
        field_type: str,
        authority: str,
        effect: str = "ADD",
        source_id: str | None = None,
        depends_on: Iterable[str] = (),
        metadata: dict[str, Any] | None = None,
    ) -> TransitionResult:
        effect = effect.upper()
        metadata = dict(metadata or {})
        depends = set(depends_on)

        if effect in {"EXAMPLE", "DISTRACTOR"}:
            node = GoalNode(
                node_id=node_id,
                key=key,
                value=value,
                field_type=field_type,
                authority=authority,
                source_id=source_id,
                depends_on=depends,
                status=NON_BINDING,
                metadata=metadata,
            )
            self._register(node)
            return TransitionResult(True, node_id=node_id, reason=f"{effect} is non-binding")

        current_id = self.active_by_key.get(key)
        current = self.nodes[current_id] if current_id else None

        if current and current.field_type != field_type:
            return self._reject(
                f"field type mismatch for {key}: active={current.field_type}, incoming={field_type}"
            )

        authority_field_type = current.field_type if current else field_type
        new_score = self.authority_score(authority_field_type, authority)

        if effect == "RETRACT":
            if not current:
                return TransitionResult(False, reason="nothing active to retract")
            old_score = self.authority_score(current.field_type, current.authority)
            if current.field_type in NORMATIVE_TYPES and authority not in USER_AUTHORITIES:
                return self._reject(
                    f"non-user authority {authority} cannot retract normative field {key}"
                )
            if new_score < old_score:
                return self._reject(
                    f"lower-authority retract rejected for {key}: {authority}({new_score}) "
                    f"< {current.authority}({old_score})"
                )
            invalidated = self._invalidate_cascade(current.node_id, by=node_id, root_status=OBSOLETE)
            tombstone = GoalNode(
                node_id=node_id,
                key=key,
                value=None,
                field_type=current.field_type,
                authority=authority,
                source_id=source_id,
                depends_on=set(),
                status=ACTIVE,
                metadata={**metadata, "effect": "RETRACT"},
            )
            self._register(tombstone)
            self.active_by_key[key] = node_id
            self.events.append({"effect": effect, "key": key, "invalidated": invalidated})
            return TransitionResult(True, node_id=node_id, invalidated=invalidated, reason="retracted")

        invalidated: list[str] = []

        if current:
            old_score = self.authority_score(current.field_type, current.authority)
            values_conflict = current.value != value

            if current.field_type in NORMATIVE_TYPES and authority not in USER_AUTHORITIES and values_conflict:
                return self._reject(
                    f"non-user authority {authority} cannot override normative field {key}"
                )

            if new_score < old_score:
                if values_conflict:
                    return self._reject(
                        f"lower-authority signal rejected for {key}: {authority}({new_score}) "
                        f"< {current.authority}({old_score})"
                    )
                # Same value from a weaker source is corroboration, never an authority downgrade.
                if source_id:
                    current.metadata.setdefault("corroborating_sources", []).append(source_id)
                return TransitionResult(True, node_id=current.node_id, reason="same value; weaker source cannot downgrade authority")

            if not values_conflict:
                # Promote provenance in-place when a stronger source confirms the same fact so
                # downstream dependency edges stay valid and future conflicts see the stronger authority.
                if new_score > old_score:
                    current.metadata.setdefault("prior_authorities", []).append(
                        {"authority": current.authority, "source_id": current.source_id}
                    )
                    current.authority = authority
                    if source_id:
                        current.source_id = source_id
                    current.metadata.setdefault("corroborating_sources", []).append(source_id or node_id)
                    self.events.append({"effect": "AUTHORITY_PROMOTION", "key": key, "node_id": current.node_id})
                    return TransitionResult(True, node_id=current.node_id, reason="same value; authority promoted")
                return TransitionResult(True, node_id=current.node_id, reason="idempotent duplicate")

            invalidated = self._invalidate_cascade(current.node_id, by=node_id, root_status=OBSOLETE)

        node = GoalNode(
            node_id=node_id,
            key=key,
            value=value,
            field_type=field_type,
            authority=authority,
            source_id=source_id,
            depends_on=depends,
            status=ACTIVE,
            metadata=metadata,
        )
        self._register(node)
        self.active_by_key[key] = node_id
        self.events.append({"effect": effect, "key": key, "node_id": node_id, "invalidated": invalidated})
        return TransitionResult(True, node_id=node_id, invalidated=invalidated)

    def apply_counterexample(self, criterion_node_id: str, evidence_id: str) -> TransitionResult:
        if criterion_node_id not in self.nodes:
            return TransitionResult(False, reason="criterion not found")
        criterion = self.nodes[criterion_node_id]
        if criterion.field_type != "acceptance_test":
            return TransitionResult(False, reason="counterexample target is not an acceptance test")
        criterion.status = UNSATISFIED
        invalidated: list[str] = []
        for child in sorted(self.dependents.get(criterion_node_id, set())):
            invalidated.extend(self._invalidate_cascade(child, by=evidence_id, root_status=INVALIDATED))
        criterion.metadata.setdefault("counterexamples", []).append(evidence_id)
        self.events.append(
            {"effect": "COUNTEREXAMPLE", "criterion": criterion_node_id, "evidence": evidence_id, "invalidated": invalidated}
        )
        return TransitionResult(True, node_id=criterion_node_id, invalidated=invalidated, reason="acceptance reopened")

    def traceability_audit(self) -> dict[str, list[str]]:
        orphan_requirements: list[str] = []
        orphan_actions: list[str] = []
        for node in self.nodes.values():
            if node.status != ACTIVE:
                continue
            if node.field_type in NORMATIVE_TYPES:
                if not node.source_id:
                    orphan_requirements.append(node.node_id)
                if node.field_type == "acceptance_test" and not node.metadata.get("observable_test"):
                    orphan_requirements.append(node.node_id)
            if node.field_type == "action":
                if not node.depends_on:
                    orphan_actions.append(node.node_id)
                elif not any(
                    self.nodes.get(parent)
                    and self.nodes[parent].field_type in (NORMATIVE_TYPES | {"hypothesis", "unknown"})
                    for parent in node.depends_on
                ):
                    orphan_actions.append(node.node_id)
        return {
            "orphan_requirements": sorted(set(orphan_requirements)),
            "orphan_actions": sorted(set(orphan_actions)),
        }


def rank_hypotheses(hypotheses: Iterable[str], evidence: Iterable[EvidenceItem]) -> list[dict[str, Any]]:
    """Rank hypotheses by weighted inconsistency, in the spirit of ACH.

    Support is deliberately not allowed to erase contradictions. The preferred
    hypothesis is the one with the least strong disconfirming evidence, then the most
    independent support. This resists confirmation-heavy research.
    """

    rows: list[dict[str, Any]] = []
    evidence_list = list(evidence)
    for hypothesis in hypotheses:
        contradiction = 0.0
        support = 0.0
        unknown = 0
        for item in evidence_list:
            relation = item.relations.get(hypothesis, "neutral")
            weight = item.weight()
            if relation == "contradict":
                contradiction += weight
            elif relation == "support":
                support += weight
            else:
                unknown += 1
        rows.append(
            {
                "hypothesis": hypothesis,
                "inconsistency": round(contradiction, 6),
                "support": round(support, 6),
                "unknown_evidence": unknown,
            }
        )
    return sorted(rows, key=lambda row: (row["inconsistency"], -row["support"], row["hypothesis"]))


def can_evidence_mutate_normative_goal(evidence: EvidenceItem) -> bool:
    """External evidence never directly rewrites a normative user goal."""

    return False
