import copy
import re
import sqlite3
import unittest
from datetime import UTC, datetime

from neon_ronin_core.persistence.sqlite_store import (
    AuditWriteError,
    NotFoundError,
    SCHEMA_VERSION,
    SQLitePersistenceProofStore,
    ValidationError,
)
from workspace_config_fixture import (
    INTERNAL_RESEARCH_WORKSPACE_CONFIG,
    INTERNAL_RESEARCH_WORKSPACE_ID,
)
from proof_helpers import assert_authorized_tables_only


FIXED_TIME = datetime(2026, 5, 26, 12, 0, 0, tzinfo=UTC)
REVIEW_TIME = datetime(2026, 5, 26, 14, 0, 0, tzinfo=UTC)
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


VALID_REVIEW_ITEM = {
    "workspace_id": INTERNAL_RESEARCH_WORKSPACE_ID,
    "review_type": "strategy_review",
    "risk_categories": ["strategy"],
    "source_actor_type": "human",
    "source_actor_id": "human:operator",
    "title": "Review internal research direction",
    "summary": "Human review of a bounded internal research planning item.",
    "required_gates": ["strategy_review_gate"],
    "linked_records": [
        {
            "record_type": "workspace_config",
            "record_id": INTERNAL_RESEARCH_WORKSPACE_ID,
            "relationship": "review_context",
        }
    ],
    "description": "Keep the first executable review queue proof bounded.",
    "priority": "normal",
    "sensitivity_rating": "low",
    "confidence": "medium",
}


class ReviewQueueItemCreateProofTests(unittest.TestCase):
    def make_store(self, *, fail_audit_write=False, clock=None, audit_id_factory=None):
        connection = sqlite3.connect(":memory:")
        store = SQLitePersistenceProofStore(
            connection,
            clock=clock or (lambda: FIXED_TIME),
            audit_id_factory=audit_id_factory or (lambda: "audit_workspace_config_create_001"),
            review_item_id_factory=lambda: "review_item_001",
            fail_audit_write=fail_audit_write,
        )
        store.initialize_schema()
        return store

    def create_base_workspace(self, store):
        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )

    def test_positive_review_item_create_writes_review_item_and_audit_record(self):
        audit_ids = iter(["audit_workspace_config_create_001", "audit_review_item_create_001"])
        clock_values = iter([FIXED_TIME, REVIEW_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)

        result = store.create_review_queue_item(review_item=copy.deepcopy(VALID_REVIEW_ITEM))

        self.assertEqual(result.review_item_id, "review_item_001")
        self.assertEqual(result.audit_record_id, "audit_review_item_create_001")
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_review_queue_items(), 1)
        self.assertEqual(store.count_audit_records(), 2)

        review_item = store.get_review_queue_item("review_item_001")
        audit = store.get_audit_record("audit_review_item_create_001")

        self.assertIsNotNone(review_item)
        self.assertIsNotNone(audit)
        assert review_item is not None
        assert audit is not None

        self.assertEqual(review_item["review_item_id"], "review_item_001")
        self.assertEqual(review_item["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(review_item["status"], "open")
        self.assertIsNone(review_item["decision"])
        self.assertEqual(review_item["audit_record_id"], "audit_review_item_create_001")
        self.assertEqual(review_item["review_type"], "strategy_review")
        self.assertEqual(review_item["schema_version"], SCHEMA_VERSION)
        self.assertEqual(review_item["record_revision"], 1)
        self.assertEqual(review_item["created_at"], "2026-05-26T14:00:00Z")
        self.assertEqual(review_item["updated_at"], "2026-05-26T14:00:00Z")
        self.assertRegex(review_item["created_at"], TIMESTAMP_PATTERN)

        self.assertEqual(audit["event_type"], "review_item_created")
        self.assertEqual(audit["action_type"], "review_queue_item_create")
        self.assertEqual(audit["target_type"], "review_item")
        self.assertEqual(audit["target_id"], "review_item_001")
        self.assertEqual(audit["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(audit["result_status"], "succeeded")
        self.assertEqual(audit["schema_version"], SCHEMA_VERSION)
        self.assertEqual(audit["record_revision"], 1)

    def test_review_item_create_requires_existing_workspace(self):
        store = self.make_store(audit_id_factory=lambda: "audit_review_item_create_001")

        with self.assertRaises(NotFoundError):
            store.create_review_queue_item(review_item=copy.deepcopy(VALID_REVIEW_ITEM))

        self.assertEqual(store.count_workspace_configs(), 0)
        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_forced_audit_failure_rolls_back_review_item_create(self):
        audit_ids = iter(["audit_workspace_config_create_001", "audit_review_item_create_001"])
        clock_values = iter([FIXED_TIME, REVIEW_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)
        store.fail_audit_write = True

        with self.assertRaises(AuditWriteError):
            store.create_review_queue_item(review_item=copy.deepcopy(VALID_REVIEW_ITEM))

        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 1)
        self.assertIsNone(store.get_review_queue_item("review_item_001"))
        self.assertIsNone(store.get_audit_record("audit_review_item_create_001"))

    def test_schema_initialization_includes_only_authorized_tables(self):
        store = self.make_store()
        assert_authorized_tables_only(self, store)

    def test_review_item_rejects_system_owned_fields(self):
        for system_owned_field in (
            "review_item_id",
            "status",
            "decision",
            "audit_record_id",
            "created_at",
            "updated_at",
            "schema_version",
            "record_revision",
        ):
            with self.subTest(system_owned_field=system_owned_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_REVIEW_ITEM)
                payload[system_owned_field] = "forged"

                with self.assertRaisesRegex(ValidationError, "system-owned"):
                    store.create_review_queue_item(review_item=payload)

                self.assertEqual(store.count_review_queue_items(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_review_item_rejects_unknown_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_REVIEW_ITEM)
        payload["surprise_field"] = True

        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            store.create_review_queue_item(review_item=payload)

        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_review_item_rejects_forbidden_metadata_and_custom_data(self):
        for forbidden_field in ("metadata", "custom_data"):
            with self.subTest(forbidden_field=forbidden_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_REVIEW_ITEM)
                payload[forbidden_field] = {}

                with self.assertRaisesRegex(ValidationError, "forbidden fields"):
                    store.create_review_queue_item(review_item=payload)

                self.assertEqual(store.count_review_queue_items(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_review_item_rejects_missing_required_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_REVIEW_ITEM)
        payload.pop("summary")

        with self.assertRaisesRegex(ValidationError, "required fields missing"):
            store.create_review_queue_item(review_item=payload)

        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_review_item_rejects_unsupported_review_type(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_REVIEW_ITEM)
        payload["review_type"] = "customer_delivery_review"

        with self.assertRaisesRegex(ValidationError, "unsupported review_type"):
            store.create_review_queue_item(review_item=payload)

        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_review_item_rejects_unsupported_risk_category(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_REVIEW_ITEM)
        payload["risk_categories"] = ["paid_action"]

        with self.assertRaisesRegex(ValidationError, "unsupported risk_categories"):
            store.create_review_queue_item(review_item=payload)

        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_review_item_rejects_unsupported_required_gate(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_REVIEW_ITEM)
        payload["required_gates"] = ["customer_delivery_gate"]

        with self.assertRaisesRegex(ValidationError, "unsupported required_gates"):
            store.create_review_queue_item(review_item=payload)

        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_review_item_rejects_invalid_linked_record_type(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_REVIEW_ITEM)
        payload["linked_records"] = [
            {
                "record_type": "customer_order",
                "record_id": "order_001",
                "relationship": "review_context",
            }
        ]

        with self.assertRaisesRegex(ValidationError, "unsupported linked record type"):
            store.create_review_queue_item(review_item=payload)

        self.assertEqual(store.count_review_queue_items(), 0)
        self.assertEqual(store.count_audit_records(), 1)


if __name__ == "__main__":
    unittest.main()
