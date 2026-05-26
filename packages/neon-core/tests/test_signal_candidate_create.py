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


FIXED_TIME = datetime(2026, 5, 26, 12, 0, 0, tzinfo=UTC)
SIGNAL_TIME = datetime(2026, 5, 26, 16, 0, 0, tzinfo=UTC)
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


VALID_SIGNAL_CANDIDATE = {
    "workspace_id": INTERNAL_RESEARCH_WORKSPACE_ID,
    "workspace_type": "internal_research",
    "signal_type": "workflow_problem",
    "source_actor_type": "human",
    "source_actor_id": "human:operator",
    "source_references": [
        {
            "record_type": "manual_note",
            "record_id": "note_001",
            "relationship": "source_observation",
        }
    ],
    "summary": "Manual workflow proofs benefit from narrow persistence boundaries.",
    "evidence_summary": "Current implementation slices stayed small and audit-first.",
    "sensitivity_rating": "low",
    "confidence": "high",
    "private_data_removed": True,
    "remaining_sensitivity_notes": "No customer, credential, provider, or business-private data included.",
    "tags": ["persistence-proof"],
}


class SignalCandidateCreateProofTests(unittest.TestCase):
    def make_store(self, *, fail_audit_write=False, clock=None, audit_id_factory=None):
        connection = sqlite3.connect(":memory:")
        default_audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_signal_candidate_create_001"]
        )
        store = SQLitePersistenceProofStore(
            connection,
            clock=clock or (lambda: FIXED_TIME),
            audit_id_factory=audit_id_factory or (lambda: next(default_audit_ids)),
            signal_id_factory=lambda: "signal_candidate_001",
            fail_audit_write=fail_audit_write,
        )
        store.initialize_schema()
        return store

    def create_base_workspace(self, store):
        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )

    def test_positive_signal_candidate_create_writes_signal_and_audit_record(self):
        audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_signal_candidate_create_001"]
        )
        clock_values = iter([FIXED_TIME, SIGNAL_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)

        result = store.create_signal_candidate(
            signal_candidate=copy.deepcopy(VALID_SIGNAL_CANDIDATE)
        )

        self.assertEqual(result.signal_id, "signal_candidate_001")
        self.assertEqual(result.audit_record_id, "audit_signal_candidate_create_001")
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_signal_candidates(), 1)
        self.assertEqual(store.count_audit_records(), 2)

        signal = store.get_signal_candidate("signal_candidate_001")
        audit = store.get_audit_record("audit_signal_candidate_create_001")

        self.assertIsNotNone(signal)
        self.assertIsNotNone(audit)
        assert signal is not None
        assert audit is not None

        self.assertEqual(signal["signal_id"], "signal_candidate_001")
        self.assertEqual(signal["signal_form"], "signal_candidate")
        self.assertEqual(signal["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(signal["status"], "candidate")
        self.assertEqual(signal["signal_type"], "workflow_problem")
        self.assertIs(signal["private_data_removed"], True)
        self.assertEqual(signal["audit_record_id"], "audit_signal_candidate_create_001")
        self.assertEqual(signal["created_at"], "2026-05-26T16:00:00Z")
        self.assertEqual(signal["updated_at"], "2026-05-26T16:00:00Z")
        self.assertEqual(signal["schema_version"], SCHEMA_VERSION)
        self.assertEqual(signal["record_revision"], 1)
        self.assertRegex(signal["created_at"], TIMESTAMP_PATTERN)

        self.assertEqual(audit["event_type"], "signal_candidate_created")
        self.assertEqual(audit["action_type"], "signal_candidate_create")
        self.assertEqual(audit["target_type"], "signal_candidate")
        self.assertEqual(audit["target_id"], "signal_candidate_001")
        self.assertEqual(audit["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(audit["result_status"], "succeeded")
        self.assertEqual(audit["schema_version"], SCHEMA_VERSION)
        self.assertEqual(audit["record_revision"], 1)

    def test_signal_candidate_requires_existing_workspace(self):
        store = self.make_store(audit_id_factory=lambda: "audit_signal_candidate_create_001")

        with self.assertRaises(NotFoundError):
            store.create_signal_candidate(
                signal_candidate=copy.deepcopy(VALID_SIGNAL_CANDIDATE)
            )

        self.assertEqual(store.count_signal_candidates(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_forced_audit_failure_rolls_back_signal_candidate_create(self):
        audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_signal_candidate_create_001"]
        )
        clock_values = iter([FIXED_TIME, SIGNAL_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)
        store.fail_audit_write = True

        with self.assertRaises(AuditWriteError):
            store.create_signal_candidate(
                signal_candidate=copy.deepcopy(VALID_SIGNAL_CANDIDATE)
            )

        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_signal_candidates(), 0)
        self.assertEqual(store.count_audit_records(), 1)
        self.assertIsNone(store.get_signal_candidate("signal_candidate_001"))
        self.assertIsNone(store.get_audit_record("audit_signal_candidate_create_001"))

    def test_schema_initialization_includes_only_authorized_tables(self):
        store = self.make_store()
        rows = store.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()

        self.assertEqual(
            [row["name"] for row in rows],
            [
                "audit_records",
                "human_decisions",
                "review_queue_items",
                "signal_candidates",
                "workspace_configs",
            ],
        )

    def test_signal_candidate_rejects_system_owned_fields(self):
        for system_owned_field in (
            "signal_id",
            "signal_form",
            "status",
            "audit_record_id",
            "created_at",
            "updated_at",
            "schema_version",
            "record_revision",
        ):
            with self.subTest(system_owned_field=system_owned_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_SIGNAL_CANDIDATE)
                payload[system_owned_field] = "forged"

                with self.assertRaisesRegex(ValidationError, "system-owned"):
                    store.create_signal_candidate(signal_candidate=payload)

                self.assertEqual(store.count_signal_candidates(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_signal_candidate_rejects_unknown_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_SIGNAL_CANDIDATE)
        payload["surprise_field"] = True

        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            store.create_signal_candidate(signal_candidate=payload)

        self.assertEqual(store.count_signal_candidates(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_signal_candidate_rejects_forbidden_metadata_and_custom_data(self):
        for forbidden_field in ("metadata", "custom_data"):
            with self.subTest(forbidden_field=forbidden_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_SIGNAL_CANDIDATE)
                payload[forbidden_field] = {}

                with self.assertRaisesRegex(ValidationError, "forbidden fields"):
                    store.create_signal_candidate(signal_candidate=payload)

                self.assertEqual(store.count_signal_candidates(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_signal_candidate_rejects_missing_required_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_SIGNAL_CANDIDATE)
        payload.pop("summary")

        with self.assertRaisesRegex(ValidationError, "required fields missing"):
            store.create_signal_candidate(signal_candidate=payload)

        self.assertEqual(store.count_signal_candidates(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_signal_candidate_rejects_private_data_not_removed(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_SIGNAL_CANDIDATE)
        payload["private_data_removed"] = False

        with self.assertRaisesRegex(ValidationError, "private_data_removed"):
            store.create_signal_candidate(signal_candidate=payload)

        self.assertEqual(store.count_signal_candidates(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_signal_candidate_rejects_unsupported_signal_type(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_SIGNAL_CANDIDATE)
        payload["signal_type"] = "etsy_listing_payload"

        with self.assertRaisesRegex(ValidationError, "unsupported signal_type"):
            store.create_signal_candidate(signal_candidate=payload)

        self.assertEqual(store.count_signal_candidates(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_signal_candidate_rejects_unsupported_sensitivity(self):
        for sensitivity in ("high", "restricted", "unknown"):
            with self.subTest(sensitivity=sensitivity):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_SIGNAL_CANDIDATE)
                payload["sensitivity_rating"] = sensitivity

                with self.assertRaisesRegex(ValidationError, "sensitivity_rating"):
                    store.create_signal_candidate(signal_candidate=payload)

                self.assertEqual(store.count_signal_candidates(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_signal_candidate_rejects_invalid_source_reference_type(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_SIGNAL_CANDIDATE)
        payload["source_references"] = [
            {
                "record_type": "customer_order",
                "record_id": "order_001",
                "relationship": "source_observation",
            }
        ]

        with self.assertRaisesRegex(ValidationError, "unsupported linked record type"):
            store.create_signal_candidate(signal_candidate=payload)

        self.assertEqual(store.count_signal_candidates(), 0)
        self.assertEqual(store.count_audit_records(), 1)


if __name__ == "__main__":
    unittest.main()
