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
from test_review_queue_item_create import VALID_REVIEW_ITEM
from workspace_config_fixture import (
    INTERNAL_RESEARCH_WORKSPACE_CONFIG,
    INTERNAL_RESEARCH_WORKSPACE_ID,
)


FIXED_TIME = datetime(2026, 5, 26, 12, 0, 0, tzinfo=UTC)
REVIEW_TIME = datetime(2026, 5, 26, 14, 0, 0, tzinfo=UTC)
DECISION_TIME = datetime(2026, 5, 26, 15, 0, 0, tzinfo=UTC)
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


VALID_HUMAN_DECISION = {
    "review_item_id": "review_item_001",
    "decision_type": "approve",
    "decision_scope": "review_item",
    "reviewer_actor_id": "human:operator",
    "target_records": [
        {
            "record_type": "review_item",
            "record_id": "review_item_001",
            "relationship": "resolves_review",
        }
    ],
    "decision_summary": "Approved this bounded internal research review item.",
    "decision_notes": "No external action is authorized by this proof.",
    "conditions": [],
    "sensitivity_rating": "low",
}


class HumanDecisionRecordProofTests(unittest.TestCase):
    def make_store(self, *, fail_audit_write=False, clock=None, audit_id_factory=None):
        connection = sqlite3.connect(":memory:")
        default_audit_ids = iter(
            [
                "audit_workspace_config_create_001",
                "audit_review_item_create_001",
                "audit_human_decision_001",
            ]
        )
        store = SQLitePersistenceProofStore(
            connection,
            clock=clock or (lambda: FIXED_TIME),
            audit_id_factory=audit_id_factory or (lambda: next(default_audit_ids)),
            review_item_id_factory=lambda: "review_item_001",
            human_decision_id_factory=lambda: "human_decision_001",
            fail_audit_write=fail_audit_write,
        )
        store.initialize_schema()
        return store

    def create_workspace_and_review_item(self, store):
        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )
        store.create_review_queue_item(review_item=copy.deepcopy(VALID_REVIEW_ITEM))

    def test_positive_human_decision_records_decision_and_resolves_review_item(self):
        audit_ids = iter(
            [
                "audit_workspace_config_create_001",
                "audit_review_item_create_001",
                "audit_human_decision_001",
            ]
        )
        clock_values = iter([FIXED_TIME, REVIEW_TIME, DECISION_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_workspace_and_review_item(store)

        result = store.record_human_decision(
            human_decision=copy.deepcopy(VALID_HUMAN_DECISION)
        )

        self.assertEqual(result.human_decision_id, "human_decision_001")
        self.assertEqual(result.audit_record_id, "audit_human_decision_001")
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_review_queue_items(), 1)
        self.assertEqual(store.count_human_decisions(), 1)
        self.assertEqual(store.count_audit_records(), 3)

        decision = store.get_human_decision("human_decision_001")
        review_item = store.get_review_queue_item("review_item_001")
        audit = store.get_audit_record("audit_human_decision_001")

        self.assertIsNotNone(decision)
        self.assertIsNotNone(review_item)
        self.assertIsNotNone(audit)
        assert decision is not None
        assert review_item is not None
        assert audit is not None

        self.assertEqual(decision["human_decision_id"], "human_decision_001")
        self.assertEqual(decision["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(decision["review_item_id"], "review_item_001")
        self.assertEqual(decision["decision_type"], "approve")
        self.assertEqual(decision["decision_status"], "recorded")
        self.assertEqual(decision["decision_scope"], "review_item")
        self.assertEqual(decision["reviewer_actor_id"], "human:operator")
        self.assertEqual(decision["audit_record_id"], "audit_human_decision_001")
        self.assertEqual(decision["decided_at"], "2026-05-26T15:00:00Z")
        self.assertEqual(decision["schema_version"], SCHEMA_VERSION)
        self.assertEqual(decision["record_revision"], 1)
        self.assertRegex(decision["created_at"], TIMESTAMP_PATTERN)

        self.assertEqual(review_item["status"], "approved")
        self.assertEqual(review_item["record_revision"], 2)
        self.assertEqual(review_item["updated_at"], "2026-05-26T15:00:00Z")
        self.assertEqual(review_item["audit_record_id"], "audit_human_decision_001")
        self.assertEqual(review_item["decision"]["human_decision_id"], "human_decision_001")
        self.assertEqual(review_item["decision"]["decision_type"], "approve")
        self.assertEqual(review_item["decision"]["reviewer_actor_id"], "human:operator")

        self.assertEqual(audit["event_type"], "human_decision_recorded")
        self.assertEqual(audit["action_type"], "human_decision_record")
        self.assertEqual(audit["target_type"], "human_decision")
        self.assertEqual(audit["target_id"], "human_decision_001")
        self.assertEqual(audit["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(audit["result_status"], "succeeded")
        self.assertEqual(audit["schema_version"], SCHEMA_VERSION)
        self.assertEqual(audit["record_revision"], 1)

    def test_human_decision_missing_review_item_does_not_create_audit_record(self):
        store = self.make_store(audit_id_factory=lambda: "audit_human_decision_001")

        with self.assertRaises(NotFoundError):
            store.record_human_decision(human_decision=copy.deepcopy(VALID_HUMAN_DECISION))

        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_forced_audit_failure_rolls_back_human_decision_and_review_resolution(self):
        audit_ids = iter(
            [
                "audit_workspace_config_create_001",
                "audit_review_item_create_001",
                "audit_human_decision_001",
            ]
        )
        clock_values = iter([FIXED_TIME, REVIEW_TIME, DECISION_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_workspace_and_review_item(store)
        store.fail_audit_write = True

        with self.assertRaises(AuditWriteError):
            store.record_human_decision(
                human_decision=copy.deepcopy(VALID_HUMAN_DECISION)
            )

        review_item = store.get_review_queue_item("review_item_001")
        self.assertIsNotNone(review_item)
        assert review_item is not None
        self.assertEqual(review_item["status"], "open")
        self.assertIsNone(review_item["decision"])
        self.assertEqual(review_item["record_revision"], 1)
        self.assertEqual(review_item["audit_record_id"], "audit_review_item_create_001")
        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 2)
        self.assertIsNone(store.get_human_decision("human_decision_001"))
        self.assertIsNone(store.get_audit_record("audit_human_decision_001"))

    def test_human_decision_rejects_already_resolved_review_item(self):
        audit_ids = iter(
            [
                "audit_workspace_config_create_001",
                "audit_review_item_create_001",
                "audit_human_decision_001",
                "audit_human_decision_002",
            ]
        )
        clock_values = iter([FIXED_TIME, REVIEW_TIME, DECISION_TIME, DECISION_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_workspace_and_review_item(store)
        store.record_human_decision(human_decision=copy.deepcopy(VALID_HUMAN_DECISION))

        with self.assertRaisesRegex(ValidationError, "already resolved"):
            store.record_human_decision(human_decision=copy.deepcopy(VALID_HUMAN_DECISION))

        self.assertEqual(store.count_human_decisions(), 1)
        self.assertEqual(store.count_audit_records(), 3)

    def test_human_decision_rejects_non_human_reviewer(self):
        store = self.make_store()
        self.create_workspace_and_review_item(store)
        payload = copy.deepcopy(VALID_HUMAN_DECISION)
        payload["reviewer_actor_id"] = "agent:reviewer"

        with self.assertRaisesRegex(ValidationError, "human actor"):
            store.record_human_decision(human_decision=payload)

        review_item = store.get_review_queue_item("review_item_001")
        self.assertIsNotNone(review_item)
        assert review_item is not None
        self.assertEqual(review_item["status"], "open")
        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 2)

    def test_human_decision_rejects_system_owned_fields(self):
        for system_owned_field in (
            "human_decision_id",
            "workspace_id",
            "decision_status",
            "audit_record_id",
            "decided_at",
            "created_at",
            "updated_at",
            "schema_version",
            "record_revision",
        ):
            with self.subTest(system_owned_field=system_owned_field):
                store = self.make_store()
                self.create_workspace_and_review_item(store)
                payload = copy.deepcopy(VALID_HUMAN_DECISION)
                payload[system_owned_field] = "forged"

                with self.assertRaisesRegex(ValidationError, "system-owned"):
                    store.record_human_decision(human_decision=payload)

                self.assertEqual(store.count_human_decisions(), 0)
                self.assertEqual(store.count_audit_records(), 2)

    def test_human_decision_rejects_unknown_fields(self):
        store = self.make_store()
        self.create_workspace_and_review_item(store)
        payload = copy.deepcopy(VALID_HUMAN_DECISION)
        payload["surprise_field"] = True

        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            store.record_human_decision(human_decision=payload)

        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 2)

    def test_human_decision_rejects_forbidden_metadata_and_custom_data(self):
        for forbidden_field in ("metadata", "custom_data"):
            with self.subTest(forbidden_field=forbidden_field):
                store = self.make_store()
                self.create_workspace_and_review_item(store)
                payload = copy.deepcopy(VALID_HUMAN_DECISION)
                payload[forbidden_field] = {}

                with self.assertRaisesRegex(ValidationError, "forbidden fields"):
                    store.record_human_decision(human_decision=payload)

                self.assertEqual(store.count_human_decisions(), 0)
                self.assertEqual(store.count_audit_records(), 2)

    def test_human_decision_rejects_unsupported_decision_type(self):
        store = self.make_store()
        self.create_workspace_and_review_item(store)
        payload = copy.deepcopy(VALID_HUMAN_DECISION)
        payload["decision_type"] = "override"

        with self.assertRaisesRegex(ValidationError, "unsupported decision_type"):
            store.record_human_decision(human_decision=payload)

        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 2)

    def test_human_decision_rejects_unsupported_decision_scope(self):
        store = self.make_store()
        self.create_workspace_and_review_item(store)
        payload = copy.deepcopy(VALID_HUMAN_DECISION)
        payload["decision_scope"] = "external_action"

        with self.assertRaisesRegex(ValidationError, "unsupported decision_scope"):
            store.record_human_decision(human_decision=payload)

        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 2)

    def test_human_decision_rejects_invalid_target_record_type(self):
        store = self.make_store()
        self.create_workspace_and_review_item(store)
        payload = copy.deepcopy(VALID_HUMAN_DECISION)
        payload["target_records"] = [
            {
                "record_type": "customer_order",
                "record_id": "order_001",
                "relationship": "reviewed_output",
            }
        ]

        with self.assertRaisesRegex(ValidationError, "unsupported linked record type"):
            store.record_human_decision(human_decision=payload)

        self.assertEqual(store.count_human_decisions(), 0)
        self.assertEqual(store.count_audit_records(), 2)

    def test_schema_initialization_includes_only_authorized_tables(self):
        store = self.make_store()
        rows = store.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()

        self.assertEqual(
            [row["name"] for row in rows],
            ["audit_records", "human_decisions", "review_queue_items", "signal_candidates", "workspace_configs"],
        )


if __name__ == "__main__":
    unittest.main()
