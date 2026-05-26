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
ARTIFACT_TIME = datetime(2026, 5, 26, 17, 0, 0, tzinfo=UTC)
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


VALID_ARTIFACT_METADATA = {
    "workspace_id": INTERNAL_RESEARCH_WORKSPACE_ID,
    "artifact_type": "markdown_source",
    "content_scope": "core_metadata_only",
    "storage_reference": {
        "storage_type": "repo_path",
        "content_stored_in_core": False,
        "reference": "docs/workspaces/internal-research/example-artifact.md",
        "description": "Metadata pointer only; content is not stored in core persistence.",
    },
    "title": "Internal research proof note",
    "summary": "Metadata-only artifact record for the persistence proof.",
    "creator_actor_type": "human",
    "creator_actor_id": "human:operator",
    "source_references": [
        {
            "record_type": "workspace_config",
            "record_id": INTERNAL_RESEARCH_WORKSPACE_ID,
            "relationship": "artifact_context",
        }
    ],
    "review_item_ids": [],
    "human_decision_ids": [],
    "content_format": "markdown",
    "sensitivity_rating": "low",
    "confidence": "high",
    "delivery_ready": False,
    "public_use_allowed": False,
    "tags": ["persistence-proof"],
}


class ArtifactMetadataCreateProofTests(unittest.TestCase):
    def make_store(self, *, fail_audit_write=False, clock=None, audit_id_factory=None):
        connection = sqlite3.connect(":memory:")
        default_audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_artifact_metadata_create_001"]
        )
        store = SQLitePersistenceProofStore(
            connection,
            clock=clock or (lambda: FIXED_TIME),
            audit_id_factory=audit_id_factory or (lambda: next(default_audit_ids)),
            artifact_id_factory=lambda: "artifact_metadata_001",
            fail_audit_write=fail_audit_write,
        )
        store.initialize_schema()
        return store

    def create_base_workspace(self, store):
        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )

    def test_positive_artifact_metadata_create_writes_artifact_and_audit_record(self):
        audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_artifact_metadata_create_001"]
        )
        clock_values = iter([FIXED_TIME, ARTIFACT_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)

        result = store.create_artifact_metadata(
            artifact_metadata=copy.deepcopy(VALID_ARTIFACT_METADATA)
        )

        self.assertEqual(result.artifact_id, "artifact_metadata_001")
        self.assertEqual(result.audit_record_id, "audit_artifact_metadata_create_001")
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_artifact_metadata(), 1)
        self.assertEqual(store.count_audit_records(), 2)

        artifact = store.get_artifact_metadata("artifact_metadata_001")
        audit = store.get_audit_record("audit_artifact_metadata_create_001")

        self.assertIsNotNone(artifact)
        self.assertIsNotNone(audit)
        assert artifact is not None
        assert audit is not None

        self.assertEqual(artifact["artifact_id"], "artifact_metadata_001")
        self.assertEqual(artifact["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(artifact["status"], "draft")
        self.assertEqual(artifact["artifact_type"], "markdown_source")
        self.assertEqual(artifact["content_scope"], "core_metadata_only")
        self.assertEqual(artifact["audit_record_ids"], ["audit_artifact_metadata_create_001"])
        self.assertIs(artifact["storage_reference"]["content_stored_in_core"], False)
        self.assertEqual(artifact["created_at"], "2026-05-26T17:00:00Z")
        self.assertEqual(artifact["updated_at"], "2026-05-26T17:00:00Z")
        self.assertEqual(artifact["schema_version"], SCHEMA_VERSION)
        self.assertEqual(artifact["record_revision"], 1)
        self.assertRegex(artifact["created_at"], TIMESTAMP_PATTERN)

        self.assertEqual(audit["event_type"], "artifact_metadata_created")
        self.assertEqual(audit["action_type"], "artifact_metadata_create")
        self.assertEqual(audit["target_type"], "artifact_metadata")
        self.assertEqual(audit["target_id"], "artifact_metadata_001")
        self.assertEqual(audit["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(audit["result_status"], "succeeded")
        self.assertEqual(audit["schema_version"], SCHEMA_VERSION)
        self.assertEqual(audit["record_revision"], 1)

    def test_artifact_metadata_requires_existing_workspace(self):
        store = self.make_store(audit_id_factory=lambda: "audit_artifact_metadata_create_001")

        with self.assertRaises(NotFoundError):
            store.create_artifact_metadata(
                artifact_metadata=copy.deepcopy(VALID_ARTIFACT_METADATA)
            )

        self.assertEqual(store.count_artifact_metadata(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_forced_audit_failure_rolls_back_artifact_metadata_create(self):
        audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_artifact_metadata_create_001"]
        )
        clock_values = iter([FIXED_TIME, ARTIFACT_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)
        store.fail_audit_write = True

        with self.assertRaises(AuditWriteError):
            store.create_artifact_metadata(
                artifact_metadata=copy.deepcopy(VALID_ARTIFACT_METADATA)
            )

        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_artifact_metadata(), 0)
        self.assertEqual(store.count_audit_records(), 1)
        self.assertIsNone(store.get_artifact_metadata("artifact_metadata_001"))
        self.assertIsNone(store.get_audit_record("audit_artifact_metadata_create_001"))

    def test_schema_initialization_includes_only_authorized_tables(self):
        store = self.make_store()
        rows = store.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()

        self.assertEqual(
            [row["name"] for row in rows],
            [
                "artifact_metadata",
                "audit_records",
                "human_decisions",
                "review_queue_items",
                "signal_candidates",
                "workflow_records",
                "workspace_configs",
            ],
        )

    def test_artifact_metadata_rejects_system_owned_fields(self):
        for system_owned_field in (
            "artifact_id",
            "status",
            "audit_record_ids",
            "created_at",
            "updated_at",
            "schema_version",
            "record_revision",
        ):
            with self.subTest(system_owned_field=system_owned_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
                payload[system_owned_field] = "forged"

                with self.assertRaisesRegex(ValidationError, "system-owned"):
                    store.create_artifact_metadata(artifact_metadata=payload)

                self.assertEqual(store.count_artifact_metadata(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_artifact_metadata_rejects_unknown_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
        payload["surprise_field"] = True

        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            store.create_artifact_metadata(artifact_metadata=payload)

        self.assertEqual(store.count_artifact_metadata(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_artifact_metadata_rejects_forbidden_metadata_and_custom_data(self):
        for forbidden_field in ("metadata", "custom_data"):
            with self.subTest(forbidden_field=forbidden_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
                payload[forbidden_field] = {}

                with self.assertRaisesRegex(ValidationError, "forbidden fields"):
                    store.create_artifact_metadata(artifact_metadata=payload)

                self.assertEqual(store.count_artifact_metadata(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_artifact_metadata_rejects_missing_required_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
        payload.pop("summary")

        with self.assertRaisesRegex(ValidationError, "required fields missing"):
            store.create_artifact_metadata(artifact_metadata=payload)

        self.assertEqual(store.count_artifact_metadata(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_artifact_metadata_rejects_core_content_storage(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
        payload["storage_reference"]["content_stored_in_core"] = True

        with self.assertRaisesRegex(ValidationError, "content_stored_in_core"):
            store.create_artifact_metadata(artifact_metadata=payload)

        self.assertEqual(store.count_artifact_metadata(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_artifact_metadata_rejects_storage_reference_payload_fields(self):
        for forbidden_storage_field in ("api_key", "token", "content_body", "payload"):
            with self.subTest(forbidden_storage_field=forbidden_storage_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
                payload["storage_reference"][forbidden_storage_field] = "nope"

                with self.assertRaisesRegex(ValidationError, "forbidden storage_reference"):
                    store.create_artifact_metadata(artifact_metadata=payload)

                self.assertEqual(store.count_artifact_metadata(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_artifact_metadata_rejects_delivery_and_public_use_shortcuts(self):
        for field_name in ("delivery_ready", "public_use_allowed"):
            with self.subTest(field_name=field_name):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
                payload[field_name] = True

                with self.assertRaisesRegex(ValidationError, field_name):
                    store.create_artifact_metadata(artifact_metadata=payload)

                self.assertEqual(store.count_artifact_metadata(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_artifact_metadata_rejects_unsupported_artifact_type(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
        payload["artifact_type"] = "etsy_listing_payload"

        with self.assertRaisesRegex(ValidationError, "unsupported artifact_type"):
            store.create_artifact_metadata(artifact_metadata=payload)

        self.assertEqual(store.count_artifact_metadata(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_artifact_metadata_rejects_invalid_source_reference_type(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_ARTIFACT_METADATA)
        payload["source_references"] = [
            {
                "record_type": "customer_order",
                "record_id": "order_001",
                "relationship": "source_material",
            }
        ]

        with self.assertRaisesRegex(ValidationError, "unsupported linked record type"):
            store.create_artifact_metadata(artifact_metadata=payload)

        self.assertEqual(store.count_artifact_metadata(), 0)
        self.assertEqual(store.count_audit_records(), 1)


if __name__ == "__main__":
    unittest.main()
