import copy
import re
import sqlite3
import tempfile
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
UPDATED_TIME = datetime(2026, 5, 26, 13, 30, 0, tzinfo=UTC)
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class WorkspaceConfigCreateProofTests(unittest.TestCase):
    def make_store(self, *, fail_audit_write=False, clock=None, audit_id_factory=None):
        connection = sqlite3.connect(":memory:")
        store = SQLitePersistenceProofStore(
            connection,
            clock=clock or (lambda: FIXED_TIME),
            audit_id_factory=audit_id_factory or (lambda: "audit_workspace_config_create_001"),
            fail_audit_write=fail_audit_write,
        )
        store.initialize_schema()
        return store

    def create_base_workspace(self, store):
        return store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )

    def test_positive_create_writes_workspace_config_and_audit_record(self):
        store = self.make_store()

        result = self.create_base_workspace(store)

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

    def test_positive_update_preserves_created_at_and_increments_revision(self):
        audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_workspace_config_update_001"]
        )
        clock_values = iter([FIXED_TIME, UPDATED_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)

        updated_config = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        updated_config["purpose"] = "Updated internal research purpose for persistence proof coverage."
        updated_config["tags"] = ["persistence-proof"]

        result = store.update_workspace_config(
            workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=updated_config,
        )

        self.assertEqual(result.workspace_id, INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(result.audit_record_id, "audit_workspace_config_update_001")
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_audit_records(), 2)

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        audit = store.get_audit_record("audit_workspace_config_update_001")

        self.assertIsNotNone(workspace)
        self.assertIsNotNone(audit)
        assert workspace is not None
        assert audit is not None

        self.assertEqual(workspace["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(workspace["purpose"], updated_config["purpose"])
        self.assertEqual(workspace["tags"], ["persistence-proof"])
        self.assertEqual(workspace["created_at"], "2026-05-26T12:00:00Z")
        self.assertEqual(workspace["updated_at"], "2026-05-26T13:30:00Z")
        self.assertEqual(workspace["schema_version"], SCHEMA_VERSION)
        self.assertEqual(workspace["record_revision"], 2)

        self.assertEqual(audit["target_type"], "workspace_config")
        self.assertEqual(audit["target_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(audit["action_type"], "workspace_config_update")
        self.assertEqual(audit["event_type"], "workspace_updated")
        self.assertEqual(audit["result_status"], "succeeded")
        self.assertEqual(audit["created_at"], "2026-05-26T13:30:00Z")
        self.assertEqual(audit["schema_version"], SCHEMA_VERSION)
        self.assertEqual(audit["record_revision"], 1)

    def test_update_missing_workspace_does_not_create_audit_record(self):
        store = self.make_store(audit_id_factory=lambda: "audit_workspace_config_update_001")

        with self.assertRaises(NotFoundError):
            store.update_workspace_config(
                workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
            )

        self.assertEqual(store.count_workspace_configs(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_forced_audit_failure_rolls_back_workspace_config_update(self):
        audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_workspace_config_update_001"]
        )
        clock_values = iter([FIXED_TIME, UPDATED_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)
        store.fail_audit_write = True

        updated_config = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        updated_config["purpose"] = "This update should roll back."

        with self.assertRaises(AuditWriteError):
            store.update_workspace_config(
                workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=updated_config,
            )

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertIsNotNone(workspace)
        assert workspace is not None
        self.assertEqual(workspace["purpose"], INTERNAL_RESEARCH_WORKSPACE_CONFIG["purpose"])
        self.assertEqual(workspace["created_at"], "2026-05-26T12:00:00Z")
        self.assertEqual(workspace["updated_at"], "2026-05-26T12:00:00Z")
        self.assertEqual(workspace["record_revision"], 1)
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_audit_records(), 1)
        self.assertIsNone(store.get_audit_record("audit_workspace_config_update_001"))

    def test_update_validation_failure_does_not_change_workspace_config(self):
        store = self.make_store()
        self.create_base_workspace(store)

        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload["metadata"] = {}

        with self.assertRaisesRegex(ValidationError, "forbidden fields"):
            store.update_workspace_config(
                workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertIsNotNone(workspace)
        assert workspace is not None
        self.assertEqual(workspace["record_revision"], 1)
        self.assertEqual(store.count_audit_records(), 1)

    def test_update_rejects_system_owned_fields_from_caller_payload(self):
        for system_owned_field in (
            "workspace_id",
            "created_at",
            "updated_at",
            "schema_version",
            "record_revision",
        ):
            with self.subTest(system_owned_field=system_owned_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
                payload[system_owned_field] = "forged"

                with self.assertRaisesRegex(ValidationError, "system-owned"):
                    store.update_workspace_config(
                        workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                        workspace_config=payload,
                    )

                workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
                self.assertIsNotNone(workspace)
                assert workspace is not None
                self.assertEqual(workspace["record_revision"], 1)
                self.assertEqual(store.count_audit_records(), 1)

    def test_update_rejects_unknown_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload["surprise_field"] = True

        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            store.update_workspace_config(
                workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertIsNotNone(workspace)
        assert workspace is not None
        self.assertEqual(workspace["record_revision"], 1)
        self.assertEqual(store.count_audit_records(), 1)

    def test_update_rejects_non_empty_allowed_agents(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload["allowed_agents"] = ["research_agent"]

        with self.assertRaisesRegex(ValidationError, "allowed_agents"):
            store.update_workspace_config(
                workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertIsNotNone(workspace)
        assert workspace is not None
        self.assertEqual(workspace["record_revision"], 1)
        self.assertEqual(store.count_audit_records(), 1)

    def test_update_rejects_external_references(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload["external_references"] = [{"provider": "example"}]

        with self.assertRaisesRegex(ValidationError, "external_references"):
            store.update_workspace_config(
                workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertIsNotNone(workspace)
        assert workspace is not None
        self.assertEqual(workspace["record_revision"], 1)
        self.assertEqual(store.count_audit_records(), 1)

    def test_update_rejects_runtime_scheduled_or_watch_mode(self):
        for runtime_key in ("scheduled_allowed", "watch_mode_allowed"):
            with self.subTest(runtime_key=runtime_key):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
                runtime = dict(payload["runtime"])
                runtime[runtime_key] = True
                payload["runtime"] = runtime

                with self.assertRaisesRegex(ValidationError, runtime_key):
                    store.update_workspace_config(
                        workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                        workspace_config=payload,
                    )

                workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
                self.assertIsNotNone(workspace)
                assert workspace is not None
                self.assertEqual(workspace["record_revision"], 1)
                self.assertEqual(store.count_audit_records(), 1)

    def test_update_rejects_status_change(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        payload["status"] = "active"

        with self.assertRaisesRegex(ValidationError, "status changes"):
            store.update_workspace_config(
                workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertIsNotNone(workspace)
        assert workspace is not None
        self.assertEqual(workspace["status"], "manual_test")
        self.assertEqual(workspace["record_revision"], 1)
        self.assertEqual(store.count_audit_records(), 1)

    def test_update_rejects_runtime_mode_shape_change(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
        runtime = dict(payload["runtime"])
        runtime["allowed_modes"] = ["off", "on_demand"]
        payload["runtime"] = runtime

        with self.assertRaisesRegex(ValidationError, "runtime changes"):
            store.update_workspace_config(
                workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=payload,
            )

        workspace = store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertIsNotNone(workspace)
        assert workspace is not None
        self.assertEqual(workspace["runtime"], INTERNAL_RESEARCH_WORKSPACE_CONFIG["runtime"])
        self.assertEqual(workspace["record_revision"], 1)
        self.assertEqual(store.count_audit_records(), 1)

    def test_schema_initialization_creates_only_authorized_tables(self):
        store = self.make_store()
        rows = store.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()

        self.assertEqual(
            [row["name"] for row in rows],
            ["audit_records", "human_decisions", "review_queue_items", "workspace_configs"],
        )

    def test_file_backed_sqlite_store_persists_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = f"{temp_dir}/neon_ronin_proof.sqlite3"
            connection = sqlite3.connect(db_path)
            store = SQLitePersistenceProofStore(
                connection,
                clock=lambda: FIXED_TIME,
                audit_id_factory=lambda: "audit_workspace_config_create_file_001",
            )
            store.initialize_schema()
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
            )
            connection.close()

            reopened = sqlite3.connect(db_path)
            reopened_store = SQLitePersistenceProofStore(reopened, clock=lambda: FIXED_TIME)

            self.assertEqual(reopened_store.count_workspace_configs(), 1)
            self.assertEqual(reopened_store.count_audit_records(), 1)
            self.assertIsNotNone(reopened_store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID))
            self.assertIsNotNone(
                reopened_store.get_audit_record("audit_workspace_config_create_file_001")
            )
            reopened.close()

    def test_forced_audit_failure_rolls_back_workspace_config(self):
        store = self.make_store(fail_audit_write=True)

        with self.assertRaises(AuditWriteError):
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
            )

        self.assertEqual(store.count_workspace_configs(), 0)
        self.assertEqual(store.count_audit_records(), 0)
        self.assertIsNone(store.get_workspace_config(INTERNAL_RESEARCH_WORKSPACE_ID))

    def test_duplicate_workspace_id_does_not_create_second_audit_record(self):
        store = self.make_store()
        self.create_base_workspace(store)

        with self.assertRaises(Exception):
            store.create_workspace_config(
                assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
                workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
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
                payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
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
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
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
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
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
                payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
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
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
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
        payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
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
                payload = copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG)
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
