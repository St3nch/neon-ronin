"""Phase 6 business-neutrality proof tests for the first persistence slice.

These tests prove existing validation rejects customer-facing, SearchClarity,
and external-action shortcuts without adding tables, schemas, runtime surfaces,
agents, integrations, scheduled jobs, watch mode, Observatory ingestion,
customer-facing onboarding, SearchClarity onboarding, or automation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
import unittest

from neon_ronin_core.persistence.sqlite_store import ValidationError
from proof_helpers import make_store
from proof_payloads import VALID_HUMAN_DECISION, VALID_REVIEW_ITEM
from workspace_config_fixture import (
    INTERNAL_RESEARCH_WORKSPACE_CONFIG,
    INTERNAL_RESEARCH_WORKSPACE_ID,
)

FIXED_TIME = datetime(2026, 5, 26, 12, 0, 0, tzinfo=UTC)
REVIEW_TIME = datetime(2026, 5, 26, 14, 0, 0, tzinfo=UTC)
DECISION_TIME = datetime(2026, 5, 26, 15, 0, 0, tzinfo=UTC)


class Phase6BusinessNeutralityProofTests(unittest.TestCase):
    def make_store(self):
        audit_ids = iter(
            [
                "audit_workspace_config_create_001",
                "audit_review_item_create_001",
                "audit_human_decision_001",
            ]
        )
        clock_values = iter([FIXED_TIME, REVIEW_TIME, DECISION_TIME])
        return make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
            review_item_id_factory=lambda: "review_item_001",
            human_decision_id_factory=lambda: "human_decision_001",
        )

    def create_workspace(self, store):
        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )

    def create_workspace_and_review_item(self, store):
        self.create_workspace(store)
        store.create_review_queue_item(review_item=deepcopy(VALID_REVIEW_ITEM))

    def test_review_item_rejects_customer_facing_review_shape(self):
        store = self.make_store()
        self.create_workspace(store)
        payload = deepcopy(VALID_REVIEW_ITEM)
        payload.update(
            {
                "review_type": "customer_delivery_review",
                "risk_categories": ["customer_delivery"],
                "required_gates": ["customer_delivery_gate"],
                "linked_records": [
                    {
                        "record_type": "customer_order",
                        "record_id": "order_001",
                        "relationship": "customer_delivery_target",
                    }
                ],
            }
        )

        with self.assertRaises(ValidationError):
            store.create_review_queue_item(review_item=payload)

        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_human_decision_rejects_external_action_or_customer_target_shape(self):
        store = self.make_store()
        self.create_workspace_and_review_item(store)
        payload = deepcopy(VALID_HUMAN_DECISION)
        payload.update(
            {
                "decision_scope": "external_action",
                "target_records": [
                    {
                        "record_type": "customer_order",
                        "record_id": "order_001",
                        "relationship": "approve_customer_delivery",
                    }
                ],
            }
        )

        with self.assertRaises(ValidationError):
            store.record_human_decision(human_decision=payload)

        review_item = store.get_review_queue_item("review_item_001")
        self.assertIsNotNone(review_item)
        assert review_item is not None
        self.assertEqual(review_item["status"], "open")
        self.assertIsNone(review_item["decision"])
        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 2)

    def test_human_decision_rejects_searchclarity_context_as_hidden_schema(self):
        store = self.make_store()
        self.create_workspace_and_review_item(store)
        payload = deepcopy(VALID_HUMAN_DECISION)
        payload["custom_data"] = {
            "business": "SearchClarity",
            "fiverr_order_id": "order_001",
            "customer_delivery_ready": True,
        }

        with self.assertRaisesRegex(ValidationError, "forbidden fields"):
            store.record_human_decision(human_decision=payload)

        review_item = store.get_review_queue_item("review_item_001")
        self.assertIsNotNone(review_item)
        assert review_item is not None
        self.assertEqual(review_item["status"], "open")
        self.assertIsNone(review_item["decision"])
        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 2)


if __name__ == "__main__":
    unittest.main()
