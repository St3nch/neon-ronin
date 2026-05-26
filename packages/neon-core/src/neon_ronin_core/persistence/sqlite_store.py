"""SQLite-backed first persistence proof for Neon Ronin.

This module intentionally implements only the approved persistence proof and
keeps transaction/read/write orchestration in one store class. Domain constants,
validators, schema setup, errors, and result dataclasses live in sibling modules.

It does not implement agents, UI, integrations, scheduled jobs, watch mode,
Observatory ingestion, customer-facing onboarding, or automation.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
import json
import sqlite3
from typing import Any
from uuid import uuid4

from .common import (
    Clock,
    IdFactory,
    _json_dumps,
    format_timestamp,
    utc_now,
)
from .constants import (
    INITIAL_ARTIFACT_STATUS,
    INITIAL_DECISION_STATUS,
    INITIAL_RECORD_REVISION,
    INITIAL_REVIEW_STATUS,
    INITIAL_SIGNAL_CANDIDATE_STATUS,
    INITIAL_WORKFLOW_STATUS,
    REVIEW_STATUS_BY_DECISION_TYPE,
    SCHEMA_VERSION,
    SIGNAL_CANDIDATE_FORM,
)
from .errors import (
    AuditWriteError,
    NotFoundError,
    PersistenceProofError,
    ValidationError,
)
from .results import (
    CreateArtifactMetadataResult,
    CreateReviewQueueItemResult,
    CreateSignalCandidateResult,
    CreateWorkflowRecordResult,
    CreateWorkspaceConfigResult,
    RecordHumanDecisionResult,
    UpdateWorkspaceConfigResult,
)
from .schema import initialize_schema as initialize_sqlite_schema
from .validators import (
    validate_artifact_metadata_payload,
    validate_assigned_workspace_id,
    validate_human_decision_payload,
    validate_review_queue_item_payload,
    validate_signal_candidate_payload,
    validate_update_does_not_change_deferred_runtime_authority,
    validate_workflow_record_payload,
    validate_workspace_config_payload,
)

class SQLitePersistenceProofStore:
    """Tiny SQLite store for the approved local persistence proof."""

    def __init__(
        self,
        connection: sqlite3.Connection,
        *,
        clock: Clock = utc_now,
        audit_id_factory: IdFactory | None = None,
        review_item_id_factory: IdFactory | None = None,
        human_decision_id_factory: IdFactory | None = None,
        signal_id_factory: IdFactory | None = None,
        artifact_id_factory: IdFactory | None = None,
        workflow_id_factory: IdFactory | None = None,
        fail_audit_write: bool = False,
    ) -> None:
        self.connection = connection
        self.clock = clock
        self.audit_id_factory = audit_id_factory or (lambda: f"audit_{uuid4().hex}")
        self.review_item_id_factory = review_item_id_factory or (
            lambda: f"review_{uuid4().hex}"
        )
        self.human_decision_id_factory = human_decision_id_factory or (
            lambda: f"hdec_{uuid4().hex}"
        )
        self.signal_id_factory = signal_id_factory or (lambda: f"sigcand_{uuid4().hex}")
        self.artifact_id_factory = artifact_id_factory or (lambda: f"art_{uuid4().hex}")
        self.workflow_id_factory = workflow_id_factory or (lambda: f"wf_{uuid4().hex}")
        self.fail_audit_write = fail_audit_write
        self.connection.row_factory = sqlite3.Row

    def initialize_schema(self) -> None:
        """Create only the tables authorized by the proof."""

        initialize_sqlite_schema(self.connection)

    def create_workspace_config(
        self,
        *,
        assigned_workspace_id: str,
        workspace_config: Mapping[str, Any],
        actor_id: str = "system:local_persistence_proof",
    ) -> CreateWorkspaceConfigResult:
        """Create a workspace config and its audit record in one transaction."""

        validate_assigned_workspace_id(assigned_workspace_id)
        clean_config = validate_workspace_config_payload(workspace_config)
        now = format_timestamp(self.clock())

        workspace_record = {
            "workspace_id": assigned_workspace_id,
            **clean_config,
            "created_at": now,
            "updated_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": INITIAL_RECORD_REVISION,
        }
        audit_record = self._build_audit_record(
            audit_record_id=self.audit_id_factory(),
            workspace_id=assigned_workspace_id,
            actor_id=actor_id,
            action_type="workspace_config_create",
            event_type="workspace_created",
            target_type="workspace_config",
            target_id=assigned_workspace_id,
            summary="Workspace config created by local persistence proof.",
            now=now,
        )

        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO workspace_configs (
                        workspace_id,
                        record_json,
                        created_at,
                        updated_at,
                        schema_version,
                        record_revision
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        assigned_workspace_id,
                        _json_dumps(workspace_record),
                        now,
                        now,
                        SCHEMA_VERSION,
                        INITIAL_RECORD_REVISION,
                    ),
                )
                self._insert_audit_record(audit_record)
        except AuditWriteError:
            raise
        except sqlite3.Error as exc:
            raise PersistenceProofError(str(exc)) from exc

        return CreateWorkspaceConfigResult(
            workspace_id=assigned_workspace_id,
            audit_record_id=audit_record["audit_record_id"],
            workspace_record=workspace_record,
            audit_record=audit_record,
        )

    def update_workspace_config(
        self,
        *,
        workspace_id: str,
        workspace_config: Mapping[str, Any],
        actor_id: str = "system:local_persistence_proof",
    ) -> UpdateWorkspaceConfigResult:
        """Update an existing workspace config and its audit record in one transaction."""

        validate_assigned_workspace_id(workspace_id)
        clean_config = validate_workspace_config_payload(workspace_config)
        existing_record = self.get_workspace_config(workspace_id)
        if existing_record is None:
            raise NotFoundError("workspace config does not exist")
        validate_update_does_not_change_deferred_runtime_authority(
            existing_record, clean_config
        )

        now = format_timestamp(self.clock())
        next_revision = int(existing_record["record_revision"]) + 1
        workspace_record = {
            "workspace_id": workspace_id,
            **clean_config,
            "created_at": existing_record["created_at"],
            "updated_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": next_revision,
        }
        audit_record = self._build_audit_record(
            audit_record_id=self.audit_id_factory(),
            workspace_id=workspace_id,
            actor_id=actor_id,
            action_type="workspace_config_update",
            event_type="workspace_updated",
            target_type="workspace_config",
            target_id=workspace_id,
            summary="Workspace config updated by local persistence proof.",
            now=now,
        )

        try:
            with self.connection:
                cursor = self.connection.execute(
                    """
                    UPDATE workspace_configs
                    SET record_json = ?,
                        updated_at = ?,
                        schema_version = ?,
                        record_revision = ?
                    WHERE workspace_id = ?
                    """,
                    (
                        _json_dumps(workspace_record),
                        now,
                        SCHEMA_VERSION,
                        next_revision,
                        workspace_id,
                    ),
                )
                if cursor.rowcount != 1:
                    raise NotFoundError("workspace config does not exist")
                self._insert_audit_record(audit_record)
        except (AuditWriteError, NotFoundError):
            raise
        except sqlite3.Error as exc:
            raise PersistenceProofError(str(exc)) from exc

        return UpdateWorkspaceConfigResult(
            workspace_id=workspace_id,
            audit_record_id=audit_record["audit_record_id"],
            workspace_record=workspace_record,
            audit_record=audit_record,
        )

    def create_review_queue_item(
        self,
        *,
        review_item: Mapping[str, Any],
        actor_id: str = "system:local_persistence_proof",
    ) -> CreateReviewQueueItemResult:
        """Create a review queue item and its audit record in one transaction."""

        clean_item = validate_review_queue_item_payload(review_item)
        workspace_id = clean_item["workspace_id"]
        if self.get_workspace_config(workspace_id) is None:
            raise NotFoundError("workspace config does not exist")

        now = format_timestamp(self.clock())
        review_item_id = self.review_item_id_factory()
        audit_record_id = self.audit_id_factory()
        review_item_record = {
            "review_item_id": review_item_id,
            **clean_item,
            "status": INITIAL_REVIEW_STATUS,
            "decision": None,
            "audit_record_id": audit_record_id,
            "created_at": now,
            "updated_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": INITIAL_RECORD_REVISION,
        }
        audit_record = self._build_audit_record(
            audit_record_id=audit_record_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            action_type="review_queue_item_create",
            event_type="review_item_created",
            target_type="review_item",
            target_id=review_item_id,
            summary="Review queue item created by local persistence proof.",
            now=now,
        )

        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO review_queue_items (
                        review_item_id,
                        workspace_id,
                        status,
                        review_type,
                        audit_record_id,
                        created_at,
                        updated_at,
                        schema_version,
                        record_revision,
                        record_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        review_item_id,
                        workspace_id,
                        INITIAL_REVIEW_STATUS,
                        clean_item["review_type"],
                        audit_record_id,
                        now,
                        now,
                        SCHEMA_VERSION,
                        INITIAL_RECORD_REVISION,
                        _json_dumps(review_item_record),
                    ),
                )
                self._insert_audit_record(audit_record)
        except AuditWriteError:
            raise
        except sqlite3.Error as exc:
            raise PersistenceProofError(str(exc)) from exc

        return CreateReviewQueueItemResult(
            review_item_id=review_item_id,
            audit_record_id=audit_record_id,
            review_item_record=review_item_record,
            audit_record=audit_record,
        )

    def record_human_decision(
        self,
        *,
        human_decision: Mapping[str, Any],
        actor_id: str = "system:local_persistence_proof",
    ) -> RecordHumanDecisionResult:
        """Record a human decision and resolve one review item in one transaction."""

        clean_decision = validate_human_decision_payload(human_decision)
        review_item_id = clean_decision["review_item_id"]
        review_item_record = self.get_review_queue_item(review_item_id)
        if review_item_record is None:
            raise NotFoundError("review queue item does not exist")
        if review_item_record["status"] != INITIAL_REVIEW_STATUS:
            raise ValidationError("review item is already resolved")

        workspace_id = review_item_record["workspace_id"]
        now = format_timestamp(self.clock())
        human_decision_id = self.human_decision_id_factory()
        audit_record_id = self.audit_id_factory()
        next_review_revision = int(review_item_record["record_revision"]) + 1
        resolved_status = REVIEW_STATUS_BY_DECISION_TYPE[clean_decision["decision_type"]]

        decision_record = {
            "human_decision_id": human_decision_id,
            "workspace_id": workspace_id,
            **clean_decision,
            "decision_status": INITIAL_DECISION_STATUS,
            "audit_record_id": audit_record_id,
            "decided_at": now,
            "created_at": now,
            "updated_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": INITIAL_RECORD_REVISION,
        }
        embedded_decision = {
            "human_decision_id": human_decision_id,
            "decision_type": clean_decision["decision_type"],
            "decision_status": INITIAL_DECISION_STATUS,
            "reviewer_actor_id": clean_decision["reviewer_actor_id"],
            "decision_summary": clean_decision["decision_summary"],
            "audit_record_id": audit_record_id,
            "decided_at": now,
        }
        updated_review_item = {
            **review_item_record,
            "status": resolved_status,
            "decision": embedded_decision,
            "audit_record_id": audit_record_id,
            "updated_at": now,
            "record_revision": next_review_revision,
        }
        audit_record = self._build_audit_record(
            audit_record_id=audit_record_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            action_type="human_decision_record",
            event_type="human_decision_recorded",
            target_type="human_decision",
            target_id=human_decision_id,
            summary="Human decision recorded by local persistence proof.",
            now=now,
        )

        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO human_decisions (
                        human_decision_id,
                        workspace_id,
                        review_item_id,
                        decision_type,
                        decision_status,
                        audit_record_id,
                        decided_at,
                        created_at,
                        updated_at,
                        schema_version,
                        record_revision,
                        record_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        human_decision_id,
                        workspace_id,
                        review_item_id,
                        clean_decision["decision_type"],
                        INITIAL_DECISION_STATUS,
                        audit_record_id,
                        now,
                        now,
                        now,
                        SCHEMA_VERSION,
                        INITIAL_RECORD_REVISION,
                        _json_dumps(decision_record),
                    ),
                )
                self.connection.execute(
                    """
                    UPDATE review_queue_items
                    SET status = ?,
                        audit_record_id = ?,
                        updated_at = ?,
                        record_revision = ?,
                        record_json = ?
                    WHERE review_item_id = ?
                    """,
                    (
                        resolved_status,
                        audit_record_id,
                        now,
                        next_review_revision,
                        _json_dumps(updated_review_item),
                        review_item_id,
                    ),
                )
                self._insert_audit_record(audit_record)
        except AuditWriteError:
            raise
        except sqlite3.Error as exc:
            raise PersistenceProofError(str(exc)) from exc

        return RecordHumanDecisionResult(
            human_decision_id=human_decision_id,
            audit_record_id=audit_record_id,
            human_decision_record=decision_record,
            review_item_record=updated_review_item,
            audit_record=audit_record,
        )

    def create_signal_candidate(
        self,
        *,
        signal_candidate: Mapping[str, Any],
        actor_id: str = "system:local_persistence_proof",
    ) -> CreateSignalCandidateResult:
        """Create a workspace-owned signal candidate and its audit record."""

        clean_candidate = validate_signal_candidate_payload(signal_candidate)
        workspace_id = clean_candidate["workspace_id"]
        if self.get_workspace_config(workspace_id) is None:
            raise NotFoundError("workspace config does not exist")

        now = format_timestamp(self.clock())
        signal_id = self.signal_id_factory()
        audit_record_id = self.audit_id_factory()
        signal_record = {
            "signal_id": signal_id,
            "signal_form": SIGNAL_CANDIDATE_FORM,
            **clean_candidate,
            "status": INITIAL_SIGNAL_CANDIDATE_STATUS,
            "audit_record_id": audit_record_id,
            "created_at": now,
            "updated_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": INITIAL_RECORD_REVISION,
        }
        audit_record = self._build_audit_record(
            audit_record_id=audit_record_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            action_type="signal_candidate_create",
            event_type="signal_candidate_created",
            target_type="signal_candidate",
            target_id=signal_id,
            summary="Signal candidate created by local persistence proof.",
            now=now,
        )

        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO signal_candidates (
                        signal_id,
                        workspace_id,
                        signal_form,
                        status,
                        signal_type,
                        audit_record_id,
                        created_at,
                        updated_at,
                        schema_version,
                        record_revision,
                        record_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        signal_id,
                        workspace_id,
                        SIGNAL_CANDIDATE_FORM,
                        INITIAL_SIGNAL_CANDIDATE_STATUS,
                        clean_candidate["signal_type"],
                        audit_record_id,
                        now,
                        now,
                        SCHEMA_VERSION,
                        INITIAL_RECORD_REVISION,
                        _json_dumps(signal_record),
                    ),
                )
                self._insert_audit_record(audit_record)
        except AuditWriteError:
            raise
        except sqlite3.Error as exc:
            raise PersistenceProofError(str(exc)) from exc

        return CreateSignalCandidateResult(
            signal_id=signal_id,
            audit_record_id=audit_record_id,
            signal_candidate_record=signal_record,
            audit_record=audit_record,
        )

    def create_artifact_metadata(
        self,
        *,
        artifact_metadata: Mapping[str, Any],
        actor_id: str = "system:local_persistence_proof",
    ) -> CreateArtifactMetadataResult:
        """Create artifact metadata and its audit record without storing content."""

        clean_artifact = validate_artifact_metadata_payload(artifact_metadata)
        workspace_id = clean_artifact["workspace_id"]
        if self.get_workspace_config(workspace_id) is None:
            raise NotFoundError("workspace config does not exist")

        now = format_timestamp(self.clock())
        artifact_id = self.artifact_id_factory()
        audit_record_id = self.audit_id_factory()
        artifact_record = {
            "artifact_id": artifact_id,
            **clean_artifact,
            "status": INITIAL_ARTIFACT_STATUS,
            "audit_record_ids": [audit_record_id],
            "created_at": now,
            "updated_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": INITIAL_RECORD_REVISION,
        }
        audit_record = self._build_audit_record(
            audit_record_id=audit_record_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            action_type="artifact_metadata_create",
            event_type="artifact_metadata_created",
            target_type="artifact_metadata",
            target_id=artifact_id,
            summary="Artifact metadata created by local persistence proof.",
            now=now,
        )

        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO artifact_metadata (
                        artifact_id,
                        workspace_id,
                        artifact_type,
                        status,
                        content_scope,
                        audit_record_id,
                        created_at,
                        updated_at,
                        schema_version,
                        record_revision,
                        record_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        artifact_id,
                        workspace_id,
                        clean_artifact["artifact_type"],
                        INITIAL_ARTIFACT_STATUS,
                        clean_artifact["content_scope"],
                        audit_record_id,
                        now,
                        now,
                        SCHEMA_VERSION,
                        INITIAL_RECORD_REVISION,
                        _json_dumps(artifact_record),
                    ),
                )
                self._insert_audit_record(audit_record)
        except AuditWriteError:
            raise
        except sqlite3.Error as exc:
            raise PersistenceProofError(str(exc)) from exc

        return CreateArtifactMetadataResult(
            artifact_id=artifact_id,
            audit_record_id=audit_record_id,
            artifact_metadata_record=artifact_record,
            audit_record=audit_record,
        )

    def create_workflow_record(
        self,
        *,
        workflow_record: Mapping[str, Any],
        actor_id: str = "system:local_persistence_proof",
    ) -> CreateWorkflowRecordResult:
        """Create a workflow definition record and its audit record."""

        clean_workflow = validate_workflow_record_payload(workflow_record)
        workspace_id = clean_workflow["workspace_id"]
        if self.get_workspace_config(workspace_id) is None:
            raise NotFoundError("workspace config does not exist")

        now = format_timestamp(self.clock())
        workflow_id = self.workflow_id_factory()
        audit_record_id = self.audit_id_factory()
        record = {
            "workflow_id": workflow_id,
            **clean_workflow,
            "status": INITIAL_WORKFLOW_STATUS,
            "audit_record_id": audit_record_id,
            "created_at": now,
            "updated_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": INITIAL_RECORD_REVISION,
        }
        audit_record = self._build_audit_record(
            audit_record_id=audit_record_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            action_type="workflow_record_create",
            event_type="workflow_record_created",
            target_type="workflow_record",
            target_id=workflow_id,
            summary="Workflow definition created by local persistence proof.",
            now=now,
        )

        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO workflow_records (
                        workflow_id,
                        workspace_id,
                        workflow_type,
                        scope_type,
                        status,
                        audit_record_id,
                        created_at,
                        updated_at,
                        schema_version,
                        record_revision,
                        record_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        workflow_id,
                        workspace_id,
                        clean_workflow["workflow_type"],
                        clean_workflow["scope_type"],
                        INITIAL_WORKFLOW_STATUS,
                        audit_record_id,
                        now,
                        now,
                        SCHEMA_VERSION,
                        INITIAL_RECORD_REVISION,
                        _json_dumps(record),
                    ),
                )
                self._insert_audit_record(audit_record)
        except AuditWriteError:
            raise
        except sqlite3.Error as exc:
            raise PersistenceProofError(str(exc)) from exc

        return CreateWorkflowRecordResult(
            workflow_id=workflow_id,
            audit_record_id=audit_record_id,
            workflow_record=record,
            audit_record=audit_record,
        )

    def get_workspace_config(self, workspace_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT record_json FROM workspace_configs WHERE workspace_id = ?",
            (workspace_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["record_json"])

    def get_review_queue_item(self, review_item_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT record_json FROM review_queue_items WHERE review_item_id = ?",
            (review_item_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["record_json"])

    def get_human_decision(self, human_decision_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT record_json FROM human_decisions WHERE human_decision_id = ?",
            (human_decision_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["record_json"])

    def get_signal_candidate(self, signal_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT record_json FROM signal_candidates WHERE signal_id = ?",
            (signal_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["record_json"])

    def get_artifact_metadata(self, artifact_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT record_json FROM artifact_metadata WHERE artifact_id = ?",
            (artifact_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["record_json"])

    def get_workflow_record(self, workflow_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT record_json FROM workflow_records WHERE workflow_id = ?",
            (workflow_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["record_json"])

    def get_audit_record(self, audit_record_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT record_json FROM audit_records WHERE audit_record_id = ?",
            (audit_record_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row["record_json"])

    def count_workspace_configs(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM workspace_configs").fetchone()[0])

    def count_review_queue_items(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM review_queue_items").fetchone()[0])

    def count_human_decisions(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM human_decisions").fetchone()[0])

    def count_signal_candidates(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM signal_candidates").fetchone()[0])

    def count_artifact_metadata(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM artifact_metadata").fetchone()[0])

    def count_workflow_records(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM workflow_records").fetchone()[0])

    def count_audit_records(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM audit_records").fetchone()[0])

    def _build_audit_record(
        self,
        *,
        audit_record_id: str,
        workspace_id: str,
        actor_id: str,
        action_type: str,
        event_type: str,
        target_type: str,
        target_id: str,
        summary: str,
        now: str,
    ) -> dict[str, Any]:
        return {
            "audit_record_id": audit_record_id,
            "event_type": event_type,
            "workspace_id": workspace_id,
            "actor_type": "system",
            "actor_id": actor_id,
            "action_type": action_type,
            "target_type": target_type,
            "target_id": target_id,
            "result_status": "succeeded",
            "occurred_at": now,
            "source_references": [],
            "summary": summary,
            "created_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": INITIAL_RECORD_REVISION,
        }

    def _insert_audit_record(self, audit_record: Mapping[str, Any]) -> None:
        if self.fail_audit_write:
            raise AuditWriteError("forced audit write failure")
        self.connection.execute(
            """
            INSERT INTO audit_records (
                audit_record_id,
                workspace_id,
                event_type,
                actor_type,
                actor_id,
                action_type,
                target_type,
                target_id,
                result_status,
                occurred_at,
                created_at,
                schema_version,
                record_revision,
                record_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                audit_record["audit_record_id"],
                audit_record["workspace_id"],
                audit_record["event_type"],
                audit_record["actor_type"],
                audit_record["actor_id"],
                audit_record["action_type"],
                audit_record["target_type"],
                audit_record["target_id"],
                audit_record["result_status"],
                audit_record["occurred_at"],
                audit_record["created_at"],
                audit_record["schema_version"],
                audit_record["record_revision"],
                _json_dumps(audit_record),
            ),
        )
