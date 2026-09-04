from __future__ import annotations

import unittest

from scripts.task_goal_state_engine import (
    ACTIVE,
    INVALIDATED,
    NON_BINDING,
    OBSOLETE,
    UNSATISFIED,
    EvidenceItem,
    GoalState,
    can_evidence_mutate_normative_goal,
    rank_hypotheses,
)


class TaskGoalStateEngineTests(unittest.TestCase):
    def test_user_correction_invalidates_dependent_downstream_work(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="goal-v1",
            key="ROOT_GOAL",
            value="optimize the existing system without reducing capability",
            field_type="root_goal",
            authority="original_user_request",
            source_id="user-turn-1",
        )
        state.apply_signal(
            node_id="route-v1",
            key="route",
            value="tune cache only",
            field_type="hypothesis",
            authority="model_inference",
            source_id="agent",
            depends_on={"goal-v1"},
        )
        result = state.apply_signal(
            node_id="goal-v2",
            key="ROOT_GOAL",
            value="replace the architecture while preserving capability",
            field_type="root_goal",
            authority="current_user_correction",
            effect="OVERRIDE",
            source_id="user-turn-2",
        )
        self.assertTrue(result.accepted)
        self.assertEqual(state.nodes["goal-v1"].status, OBSOLETE)
        self.assertEqual(state.nodes["route-v1"].status, INVALIDATED)
        self.assertEqual(state.active_by_key["ROOT_GOAL"], "goal-v2")

    def test_example_and_distractor_never_become_binding_requirements(self) -> None:
        state = GoalState()
        for effect, node_id in (("EXAMPLE", "ex"), ("DISTRACTOR", "noise")):
            result = state.apply_signal(
                node_id=node_id,
                key=f"k-{node_id}",
                value="GitHub",
                field_type="hard_constraint",
                authority="current_user_explicit",
                effect=effect,
                source_id="user",
            )
            self.assertTrue(result.accepted)
            self.assertEqual(state.nodes[node_id].status, NON_BINDING)
            self.assertNotIn(f"k-{node_id}", state.active_by_key)

    def test_runtime_fact_cannot_silently_rewrite_normative_goal(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="goal",
            key="DESIRED_END_STATE",
            value="feature remains enabled and becomes reliable",
            field_type="desired_end_state",
            authority="current_user_explicit",
            source_id="user",
        )
        result = state.apply_signal(
            node_id="runtime-attempt",
            key="DESIRED_END_STATE",
            value="disable feature",
            field_type="desired_end_state",
            authority="owning_runtime_readback",
            effect="UPDATE",
            source_id="runtime",
        )
        self.assertFalse(result.accepted)
        self.assertEqual(state.nodes["goal"].status, ACTIVE)
        self.assertEqual(state.nodes[state.active_by_key["DESIRED_END_STATE"]].value, "feature remains enabled and becomes reliable")

    def test_owning_runtime_overrides_stale_summary_for_mutable_facts(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="summary",
            key="runtime.version",
            value="1.0",
            field_type="version",
            authority="summary_cache",
            source_id="old-summary",
        )
        result = state.apply_signal(
            node_id="live",
            key="runtime.version",
            value="2.0",
            field_type="version",
            authority="owning_runtime_readback",
            effect="UPDATE",
            source_id="runtime-readback",
        )
        self.assertTrue(result.accepted)
        self.assertEqual(state.nodes["summary"].status, OBSOLETE)
        self.assertEqual(state.nodes["live"].status, ACTIVE)

    def test_stale_summary_cannot_override_current_user_correction(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="corrected",
            key="HARD_CONSTRAINT",
            value="preserve workload",
            field_type="hard_constraint",
            authority="current_user_correction",
            source_id="user-new",
        )
        result = state.apply_signal(
            node_id="stale",
            key="HARD_CONSTRAINT",
            value="reduce workload",
            field_type="hard_constraint",
            authority="summary_cache",
            effect="UPDATE",
            source_id="summary-old",
        )
        self.assertFalse(result.accepted)
        self.assertEqual(state.active_by_key["HARD_CONSTRAINT"], "corrected")

    def test_low_authority_retract_cannot_remove_current_user_requirement(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="required",
            key="PROTECTED_CAPABILITY",
            value="keep all requested functionality",
            field_type="protected_capability",
            authority="current_user_explicit",
            source_id="user",
        )
        result = state.apply_signal(
            node_id="agent-retract",
            key="PROTECTED_CAPABILITY",
            value=None,
            field_type="protected_capability",
            authority="model_inference",
            effect="RETRACT",
            source_id="agent",
        )
        self.assertFalse(result.accepted)
        self.assertEqual(state.active_by_key["PROTECTED_CAPABILITY"], "required")
        self.assertEqual(state.nodes["required"].status, ACTIVE)
        self.assertIn("cannot retract normative field", result.reason)

    def test_same_value_weaker_signal_cannot_downgrade_active_authority(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="user-rule",
            key="HARD_CONSTRAINT",
            value="preserve workload",
            field_type="hard_constraint",
            authority="current_user_correction",
            source_id="user-new",
        )
        result = state.apply_signal(
            node_id="weak-copy",
            key="HARD_CONSTRAINT",
            value="preserve workload",
            field_type="hard_constraint",
            authority="summary_cache",
            effect="UPDATE",
            source_id="summary-copy",
        )
        self.assertTrue(result.accepted)
        active = state.nodes[state.active_by_key["HARD_CONSTRAINT"]]
        self.assertEqual(active.node_id, "user-rule")
        self.assertEqual(active.authority, "current_user_correction")
        self.assertEqual(active.source_id, "user-new")
        self.assertIn("summary-copy", active.metadata.get("corroborating_sources", []))

    def test_same_value_stronger_factual_readback_promotes_authority_without_breaking_dependents(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="fact",
            key="runtime.version",
            value="2.0",
            field_type="version",
            authority="summary_cache",
            source_id="summary",
        )
        state.apply_signal(
            node_id="dependent",
            key="route-hypothesis",
            value="use v2 path",
            field_type="hypothesis",
            authority="model_inference",
            source_id="agent",
            depends_on={"fact"},
        )
        result = state.apply_signal(
            node_id="live-confirmation",
            key="runtime.version",
            value="2.0",
            field_type="version",
            authority="owning_runtime_readback",
            effect="UPDATE",
            source_id="runtime",
        )
        self.assertTrue(result.accepted)
        active = state.nodes[state.active_by_key["runtime.version"]]
        self.assertEqual(active.node_id, "fact")
        self.assertEqual(active.authority, "owning_runtime_readback")
        self.assertEqual(active.source_id, "runtime")
        self.assertEqual(state.nodes["dependent"].status, ACTIVE)

    def test_uncertainty_classes_route_to_different_resolvers(self) -> None:
        self.assertEqual(GoalState.resolver_for("specification"), "current_user_or_explicit_task_contract")
        self.assertEqual(GoalState.resolver_for("environment_state"), "owning_runtime_readback")
        self.assertEqual(GoalState.resolver_for("capability"), "harmless_capability_probe_or_executable_test")
        self.assertEqual(GoalState.resolver_for("evidence"), "independent_corroboration_and_source_grading")
        self.assertNotEqual(GoalState.resolver_for("specification"), GoalState.resolver_for("model"))

    def test_darkweb_or_unverified_evidence_is_hypothesis_signal_not_goal_authority(self) -> None:
        item = EvidenceItem(
            evidence_id="rare-1",
            reliability="F",
            credibility=6,
            origin="darkweb_or_unverified",
            corroborated=False,
            relations={"h1": "support"},
        )
        self.assertLess(item.weight(), 0.1)
        self.assertFalse(can_evidence_mutate_normative_goal(item))

    def test_corroboration_increases_evidence_weight_without_making_it_goal_authority(self) -> None:
        raw = EvidenceItem("e1", reliability="C", credibility=3, origin="long_tail", corroborated=False)
        corroborated = EvidenceItem("e2", reliability="C", credibility=3, origin="long_tail", corroborated=True)
        self.assertGreater(corroborated.weight(), raw.weight())
        self.assertFalse(can_evidence_mutate_normative_goal(corroborated))

    def test_ach_ranking_penalizes_strong_disconfirmation_more_than_confirmation_volume(self) -> None:
        evidence = [
            EvidenceItem("primary-contradiction", "A", 1, "primary", True, {"h1": "contradict", "h2": "neutral"}),
            EvidenceItem("weak-support-1", "D", 4, "long_tail", False, {"h1": "support", "h2": "neutral"}),
            EvidenceItem("weak-support-2", "D", 4, "long_tail", False, {"h1": "support", "h2": "neutral"}),
            EvidenceItem("solid-support", "B", 2, "independent_reproduction", True, {"h2": "support"}),
        ]
        ranking = rank_hypotheses(["h1", "h2"], evidence)
        self.assertEqual(ranking[0]["hypothesis"], "h2")
        self.assertGreater(ranking[1]["inconsistency"], ranking[0]["inconsistency"])

    def test_failed_acceptance_test_reopens_dependent_route_not_root_goal(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="goal",
            key="ROOT_GOAL",
            value="make the feature work",
            field_type="root_goal",
            authority="current_user_explicit",
            source_id="user",
        )
        state.apply_signal(
            node_id="accept",
            key="ACCEPTANCE:feature",
            value="feature works in owning runtime",
            field_type="acceptance_test",
            authority="current_user_explicit",
            source_id="user",
            depends_on={"goal"},
            metadata={"observable_test": "runtime read-back"},
        )
        state.apply_signal(
            node_id="route",
            key="route",
            value="implementation A",
            field_type="action",
            authority="model_inference",
            source_id="agent",
            depends_on={"accept"},
        )
        result = state.apply_counterexample("accept", "runtime-failure")
        self.assertTrue(result.accepted)
        self.assertEqual(state.nodes["accept"].status, UNSATISFIED)
        self.assertEqual(state.nodes["route"].status, INVALIDATED)
        self.assertEqual(state.nodes["goal"].status, ACTIVE)

    def test_traceability_audit_rejects_orphan_requirement_and_orphan_action(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="orphan-goal",
            key="ROOT_GOAL",
            value="do something",
            field_type="root_goal",
            authority="current_user_explicit",
            source_id=None,
        )
        state.apply_signal(
            node_id="orphan-action",
            key="action-1",
            value="run unrelated tool",
            field_type="action",
            authority="model_inference",
            source_id="agent",
        )
        audit = state.traceability_audit()
        self.assertIn("orphan-goal", audit["orphan_requirements"])
        self.assertIn("orphan-action", audit["orphan_actions"])

    def test_traceability_audit_accepts_requirement_and_action_with_causal_links(self) -> None:
        state = GoalState()
        state.apply_signal(
            node_id="goal",
            key="ROOT_GOAL",
            value="verified result",
            field_type="root_goal",
            authority="current_user_explicit",
            source_id="user",
        )
        state.apply_signal(
            node_id="acceptance",
            key="ACCEPTANCE",
            value="read-back matches",
            field_type="acceptance_test",
            authority="current_user_explicit",
            source_id="user",
            depends_on={"goal"},
            metadata={"observable_test": "owning runtime read-back"},
        )
        state.apply_signal(
            node_id="action",
            key="ACTION",
            value="perform mutation",
            field_type="action",
            authority="model_inference",
            source_id="agent",
            depends_on={"acceptance"},
        )
        self.assertEqual(state.traceability_audit(), {"orphan_requirements": [], "orphan_actions": []})

    def test_metamorphic_noise_and_example_order_do_not_change_active_root_goal(self) -> None:
        def build(order: list[str]) -> tuple[str, str]:
            state = GoalState()
            state.apply_signal(
                node_id="goal",
                key="ROOT_GOAL",
                value="complete the real task",
                field_type="root_goal",
                authority="original_user_request",
                source_id="user",
            )
            for item in order:
                state.apply_signal(
                    node_id=item,
                    key=f"aux-{item}",
                    value="decorative context",
                    field_type="hard_constraint",
                    authority="current_user_explicit",
                    effect="EXAMPLE" if item.startswith("ex") else "DISTRACTOR",
                    source_id="user",
                )
            active = state.nodes[state.active_by_key["ROOT_GOAL"]]
            return active.node_id, active.value

        self.assertEqual(build(["ex1", "noise1", "ex2"]), build(["noise1", "ex2", "ex1"]))


if __name__ == "__main__":
    unittest.main()
