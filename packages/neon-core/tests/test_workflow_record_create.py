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
from proof_payloads import VALID_WORKFLOW_RECORD


FIXED_TIME = datetime(2026, 5, 26, 12, 0, 0, tzinfo=UTC)
WORKFLOW_TIME = datetime(2026, 5, 26, 18, 0, 0, tzinfo=UTC)
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class WorkflowRecordCreateProofTests(unittest.TestCase):
    def make_store(self, *, fail_audit_write=False, clock=None, audit_id_factory=None):
        connection = sqlite3.connect(":memory:")
        default_audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_workflow_record_create_001"]
        )
        store = SQLitePersistenceProofStore(
            connection,
            clock=clock or (lambda: FIXED_TIME),
            audit_id_factory=audit_id_factory or (lambda: next(default_audit_ids)),
            workflow_id_factory=lambda: "workflow_record_001",
            fail_audit_write=fail_audit_write,
        )
        store.initialize_schema()
        return store

    def create_base_workspace(self, store):
        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=copy.deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )

    def test_positive_workflow_record_create_writes_workflow_and_audit_record(self):
        audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_workflow_record_create_001"]
        )
        clock_values = iter([FIXED_TIME, WORKFLOW_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)

        result = store.create_workflow_record(
            workflow_record=copy.deepcopy(VALID_WORKFLOW_RECORD)
        )

        self.assertEqual(result.workflow_id, "workflow_record_001")
        self.assertEqual(result.audit_record_id, "audit_workflow_record_create_001")
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_workflow_records(), 1)
        self.assertEqual(store.count_audit_records(), 2)

        workflow = store.get_workflow_record("workflow_record_001")
        audit = store.get_audit_record("audit_workflow_record_create_001")

        self.assertIsNotNone(workflow)
        self.assertIsNotNone(audit)
        assert workflow is not None
        assert audit is not None

        self.assertEqual(workflow["workflow_id"], "workflow_record_001")
        self.assertEqual(workflow["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(workflow["workflow_type"], "manual_research")
        self.assertEqual(workflow["scope_type"], "workspace")
        self.assertEqual(workflow["status"], "manual_test")
        self.assertEqual(workflow["audit_record_id"], "audit_workflow_record_create_001")
        self.assertEqual(workflow["allowed_runtime_modes"], ["on_demand"])
        self.assertEqual(workflow["trigger_types"], ["human_started"])
        self.assertEqual(workflow["allowed_agents"], [])
        self.assertEqual(workflow["created_at"], "2026-05-26T18:00:00Z")
        self.assertEqual(workflow["updated_at"], "2026-05-26T18:00:00Z")
        self.assertEqual(workflow["schema_version"], SCHEMA_VERSION)
        self.assertEqual(workflow["record_revision"], 1)
        self.assertRegex(workflow["created_at"], TIMESTAMP_PATTERN)

        self.assertEqual(audit["event_type"], "workflow_record_created")
        self.assertEqual(audit["action_type"], "workflow_record_create")
        self.assertEqual(audit["target_type"], "workflow_record")
        self.assertEqual(audit["target_id"], "workflow_record_001")
        self.assertEqual(audit["workspace_id"], INTERNAL_RESEARCH_WORKSPACE_ID)
        self.assertEqual(audit["result_status"], "succeeded")
        self.assertEqual(audit["schema_version"], SCHEMA_VERSION)
        self.assertEqual(audit["record_revision"], 1)

    def test_workflow_record_requires_existing_workspace(self):
        store = self.make_store(audit_id_factory=lambda: "audit_workflow_record_create_001")

        with self.assertRaises(NotFoundError):
            store.create_workflow_record(
                workflow_record=copy.deepcopy(VALID_WORKFLOW_RECORD)
            )

        self.assertEqual(store.count_workflow_records(), 0)
        self.assertEqual(store.count_audit_records(), 0)

    def test_forced_audit_failure_rolls_back_workflow_record_create(self):
        audit_ids = iter(
            ["audit_workspace_config_create_001", "audit_workflow_record_create_001"]
        )
        clock_values = iter([FIXED_TIME, WORKFLOW_TIME])
        store = self.make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
        )
        self.create_base_workspace(store)
        store.fail_audit_write = True

        with self.assertRaises(AuditWriteError):
            store.create_workflow_record(
                workflow_record=copy.deepcopy(VALID_WORKFLOW_RECORD)
            )

        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_workflow_records(), 0)
        self.assertEqual(store.count_audit_records(), 1)
        self.assertIsNone(store.get_workflow_record("workflow_record_001"))
        self.assertIsNone(store.get_audit_record("audit_workflow_record_create_001"))

    def test_schema_initialization_includes_only_authorized_tables(self):
        store = self.make_store()
        assert_authorized_tables_only(self, store)

    def test_workflow_record_rejects_system_owned_fields(self):
        for system_owned_field in (
            "workflow_id",
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
                payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
                payload[system_owned_field] = "forged"

                with self.assertRaisesRegex(ValidationError, "system-owned"):
                    store.create_workflow_record(workflow_record=payload)

                self.assertEqual(store.count_workflow_records(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_unknown_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
        payload["surprise_field"] = True

        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            store.create_workflow_record(workflow_record=payload)

        self.assertEqual(store.count_workflow_records(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_forbidden_metadata_and_custom_data(self):
        for forbidden_field in ("metadata", "custom_data"):
            with self.subTest(forbidden_field=forbidden_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
                payload[forbidden_field] = {}

                with self.assertRaisesRegex(ValidationError, "forbidden fields"):
                    store.create_workflow_record(workflow_record=payload)

                self.assertEqual(store.count_workflow_records(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_missing_required_fields(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
        payload.pop("workflow_name")

        with self.assertRaisesRegex(ValidationError, "required fields missing"):
            store.create_workflow_record(workflow_record=payload)

        self.assertEqual(store.count_workflow_records(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_unsupported_workflow_type(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
        payload["workflow_type"] = "etsy_listing_automation"

        with self.assertRaisesRegex(ValidationError, "unsupported workflow_type"):
            store.create_workflow_record(workflow_record=payload)

        self.assertEqual(store.count_workflow_records(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_scheduled_watch_and_external_triggers(self):
        for trigger_type in ("scheduled", "watch_mode", "external_event"):
            with self.subTest(trigger_type=trigger_type):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
                payload["trigger_types"] = [trigger_type]

                with self.assertRaisesRegex(ValidationError, "trigger_types"):
                    store.create_workflow_record(workflow_record=payload)

                self.assertEqual(store.count_workflow_records(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_runtime_modes_other_than_on_demand(self):
        for runtime_mode in ("scheduled", "watch", "live"):
            with self.subTest(runtime_mode=runtime_mode):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
                payload["allowed_runtime_modes"] = [runtime_mode]

                with self.assertRaisesRegex(ValidationError, "allowed_runtime_modes"):
                    store.create_workflow_record(workflow_record=payload)

                self.assertEqual(store.count_workflow_records(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_non_empty_allowed_agents(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
        payload["allowed_agents"] = ["agent:researcher"]

        with self.assertRaisesRegex(ValidationError, "allowed_agents"):
            store.create_workflow_record(workflow_record=payload)

        self.assertEqual(store.count_workflow_records(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_agent_or_integration_step_actor(self):
        for actor_type in ("agent", "integration"):
            with self.subTest(actor_type=actor_type):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
                payload["steps"][0]["actor_type"] = actor_type

                with self.assertRaisesRegex(ValidationError, "actor_type"):
                    store.create_workflow_record(workflow_record=payload)

                self.assertEqual(store.count_workflow_records(), 0)
                self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_step_agent_ids(self):
        store = self.make_store()
        self.create_base_workspace(store)
        payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
        payload["steps"][0]["allowed_agent_ids"] = ["agent:researcher"]

        with self.assertRaisesRegex(ValidationError, "allowed_agent_ids"):
            store.create_workflow_record(workflow_record=payload)

        self.assertEqual(store.count_workflow_records(), 0)
        self.assertEqual(store.count_audit_records(), 1)

    def test_workflow_record_rejects_step_payload_fields(self):
        for forbidden_step_field in ("provider_payload", "private_content", "api_key"):
            with self.subTest(forbidden_step_field=forbidden_step_field):
                store = self.make_store()
                self.create_base_workspace(store)
                payload = copy.deepcopy(VALID_WORKFLOW_RECORD)
                payload["steps"][0][forbidden_step_field] = "nope"

                with self.assertRaisesRegex(ValidationError, "forbidden workflow step"):
                    store.create_workflow_record(workflow_record=payload)

                self.assertEqual(store.count_workflow_records(), 0)
                self.assertEqual(store.count_audit_records(), 1)


if __name__ == "__main__":
    unittest.main()
