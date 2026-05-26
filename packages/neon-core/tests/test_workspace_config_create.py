import re
import sqlite3
import unittest
from datetime import UTC, datetime

from neon_ronin_core.persistence.sqlite_store import (
    AuditWriteError,
    SCHEMA_VERSION,
    SQLitePersistenceProofStore,
    ValidationError,
)
from workspace_config_fixture import (
    INTERNAL_RESEARCH_WORKSPACE_CONFIG,
    INTERNAL_RESEARCH_WORKSPACE_ID,
)


FIXED_TIME = datetime(2026, 5, 26, 12, 0, 0, tzinfo=UTC)
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class WorkspaceConfigCreateProofTests(unittest.TestCase):
    def make_store(self, *, fail_audit_write=False):
        connection = sqlite3.connect(":memory:")
        store = SQLitePersistenceProofStore(
            connection,
            clock=lambda: FIXED_TIME,
            audit_id_factory=lambda: "audit_workspace_config_create_001",
            fail_audit_write=fail_audit_write,
        )
        store.initialize_schema()
        return store

    def test_positive_create_writes_workspace_config_and_audit_record(self):
        store = self.make_store()

        result = store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=INTERNAL_RESEARCH_WORKSPACE_CONFIG,
        )

        self.assertEqual(result.workspace_id, INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(result.audit_record_id, "audit_workspace_config_create_001")
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_audit_records(), 1)

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        audit = store.get_audit_record("audit_workspace_config_create_001")

        self.assertIsNotNone(workspace)
        self.assertIsNotNone(audit)
        assert workspace is not None
        assert audit is not None

        self.assertEqual(workspace["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(workspace["schema_version"], SCHEMA_VERSION)
        self.assertEqual(workspace["record_revision"], 1)
        self.assertEqual(workspace["created_at"], "2026-05-26T12:00:00Z")
        self.assertEqual(workspace["updated_at"], "2026-05-26T12:00:00Z")
        self.assertRegex(workspace["created_at"], TIMESTAMP_PATTERN)

        self.assertEqual(audit["target_type"], "workspace_config")
        self.assertEqual(audit["target_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(audit["action_type"], "workspace_config_create")
        self.assertEqual(audit["result_status"], "succeeded")
        self.assertEqual(audit["schema_version"], SCHEMA_VERSION)
        self.assertEqual(audit["record_revision"], 1)
        self.assertRegex(audit["created_at"], TIMESTAMP_PATTERN)

    def test_forced_audit_failure_rolls_back_workspace_config(self):
        store = self.make_store(fail_audit_write=True)

        with self.assertRaises(AuditWriteError):
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=INTERNAL_RESEARCH_WORKSPACE_CONFIG,
            )

        self.assertEqual(store.count_workspace_configs(), 0)
        self.assertEqual(store.count_audit_records(), 0)
        self.assertIsNone(store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID))

    def test_duplicate_workspace_id_does_not_create_second_audit_record(self):
        store = self.make_store()
        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=INTERNAL_RESEARCH_WORKSPACE_CONFIG,
        )

        with self.assertRaises(Exception):
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=INTERNAL_RESEARCH_WORKSPACE_CONFIG,
            )

        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_audit_records(), 1)

    def test_rejects_system_owned_fields_from_caller_payload(self):
        for system_owned_field in (
            "workspace_id",
            "created_at",
            "updated_at",
            "schema_version",
            "record_revision",
        ):
            with self.subTest(system_owned_field=system_owned_field):
                store = self.make_store()
                payload = dict(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
                payload[system_owned_field] = "forged"

                with self.assertRaisesRegex(ValidationError, "system-owned"):
                    store.create_workspace_config(
                        assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                        workspace_config=payload,
                    )

                self.assertEqual(store.count_workspace_configs(), 0)
                self.assertEqual(store.count_audit_records(), 0)

    def test_rejects_unknown_fields(self):
        store = self.make_store()
        payload = dict(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload["surprise_field"] = True

        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        self.assertEqual(store.count_workspace_configs(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_rejects_missing_required_fields(self):
        store = self.make_store()
        payload = dict(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload.pop("purpose")

        with self.assertRaisesRegex(ValidationError, "required fields missing"):
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        self.assertEqual(store.count_workspace_configs(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_rejects_forbidden_metadata_and_custom_data(self):
        for forbidden_field in ("metadata", "custom_data"):
            with self.subTest(forbidden_field=forbidden_field):
                store = self.make_store()
                payload = dict(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
                payload[forbidden_field] = {}

                with self.assertRaisesRegex(ValidationError, "forbidden fields"):
                    store.create_workspace_config(
                        assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                        workspace_config=payload,
                    )

                self.assertEqual(store.count_workspace_configs(), 0)
                self.assertEqual(store.count_audit_records(), 0)

    def test_rejects_non_empty_allowed_agents(self):
        store = self.make_store()
        payload = dict(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload["allowed_agents"] = ["research_agent"]

        with self.assertRaisesRegex(ValidationError, "allowed_agents"):
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        self.assertEqual(store.count_workspace_configs(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_rejects_external_references(self):
        store = self.make_store()
        payload = dict(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload["external_references"] = [{"provider": "example"}]

        with self.assertRaisesRegex(ValidationError, "external_references"):
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        self.assertEqual(store.count_workspace_configs(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_rejects_runtime_scheduled_or_watch_mode(self):
        for runtime_key in ("scheduled_allowed", "watch_mode_allowed"):
            with self.subTest(runtime_key=runtime_key):
                store = self.make_store()
                payload = dict(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
                runtime = dict(payload["runtime"])
                runtime[runtime_key] = True
                payload["runtime"] = runtime

                with self.assertRaisesRegex(ValidationError, runtime_key):
                    store.create_workspace_config(
                        assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                        workspace_config=payload,
                    )

                self.assertEqual(store.count_workspace_configs(), 0)
                self.assertEqual(store.count_audit_records(), 0)


if __name__ == "__main__":
    unittest.main()
