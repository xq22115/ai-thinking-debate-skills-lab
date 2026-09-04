from __future__ import annotations

import unittest

from scripts.task_goal_state_engine import ACTIVE, GoalState


class TaskGoalStateAuthorityCreationTests(unittest.TestCase):
    def test_model_inference_cannot_create_root_goal_from_empty_state(self) -> None:
        state = GoalState()
        result = state.apply_signal(
            node_id="guess",
            key="ROOT_GOAL",
            value="a plausible hidden goal",
            field_type="root_goal",
            authority="model_inference",
            source_id="agent",
        )
        self.assertFalse(result.accepted)
        self.assertNotIn("ROOT_GOAL", state.active_by_key)
        self.assertIn("cannot create or mutate normative field", result.reason)

    def test_durable_preference_cannot_be_promoted_into_hard_constraint(self) -> None:
        state = GoalState()
        result = state.apply_signal(
            node_id="pref-as-constraint",
            key="HARD_CONSTRAINT",
            value="always use GitHub",
            field_type="hard_constraint",
            authority="durable_user_preference",
            source_id="preference-memory",
        )
        self.assertFalse(result.accepted)
        self.assertNotIn("HARD_CONSTRAINT", state.active_by_key)

    def test_durable_preference_remains_valid_as_preference(self) -> None:
        state = GoalState()
        result = state.apply_signal(
            node_id="pref",
            key="route.preference",
            value="prefer GitHub when task-equivalent",
            field_type="preference",
            authority="durable_user_preference",
            source_id="preference-memory",
        )
        self.assertTrue(result.accepted)
        active = state.nodes[state.active_by_key["route.preference"]]
        self.assertEqual(active.status, ACTIVE)
        self.assertEqual(active.authority, "durable_user_preference")


if __name__ == "__main__":
    unittest.main()
