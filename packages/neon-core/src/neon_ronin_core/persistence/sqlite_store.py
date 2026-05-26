"""SQLite-backed first persistence proof for Neon Ronin.

This module intentionally implements only the approved persistence proof:

- workspace_configs
- audit_records
- review_queue_items
- human_decisions
- signal_candidates
- workspace_config_create
- workspace_config_update
- review_queue_item_create
- human_decision_record
- signal_candidate_create
- audit-first transaction behavior

It does not implement agents, UI, integrations, scheduled jobs, watch mode,
Observatory ingestion, customer-facing onboarding, or automation.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import sqlite3
from typing import Any
from uuid import uuid4

SCHEMA_VERSION = "schema_v1"
INITIAL_RECORD_REVISION = 1
INITIAL_REVIEW_STATUS = "open"
INITIAL_DECISION_STATUS = "recorded"
SIGNAL_CANDIDATE_FORM = "signal_candidate"
INITIAL_SIGNAL_CANDIDATE_STATUS = "candidate"

FORBIDDEN_FIELDS = frozenset({"metadata", "custom_data"})
SYSTEM_OWNED_WORKSPACE_FIELDS = frozenset(
    {
        "workspace_id",
        "created_at",
        "updated_at",
        "schema_version",
        "record_revision",
    }
)
SYSTEM_OWNED_REVIEW_FIELDS = frozenset(
    {
        "review_item_id",
        "status",
        "decision",
        "audit_record_id",
        "created_at",
        "updated_at",
        "schema_version",
        "record_revision",
    }
)
SYSTEM_OWNED_DECISION_FIELDS = frozenset(
    {
        "human_decision_id",
        "workspace_id",
        "decision_status",
        "audit_record_id",
        "decided_at",
        "created_at",
        "updated_at",
        "schema_version",
        "record_revision",
    }
)
SYSTEM_OWNED_SIGNAL_FIELDS = frozenset(
    {
        "signal_id",
        "signal_form",
        "status",
        "audit_record_id",
        "created_at",
        "updated_at",
        "schema_version",
        "record_revision",
    }
)
ALLOWED_WORKSPACE_CREATE_FIELDS = frozenset(
    {
        "workspace_name",
        "workspace_type",
        "status",
        "purpose",
        "channels",
        "adapter",
        "allowed_agents",
        "review_gates",
        "observatory",
        "storage_rules",
        "runtime",
        "hard_no_rules",
        "audit_requirements",
        "external_references",
        "tags",
    }
)
REQUIRED_WORKSPACE_CREATE_FIELDS = frozenset(
    {
        "workspace_name",
        "workspace_type",
        "status",
        "purpose",
        "channels",
        "adapter",
        "allowed_agents",
        "review_gates",
        "observatory",
        "storage_rules",
        "runtime",
        "hard_no_rules",
        "audit_requirements",
    }
)
ALLOWED_REVIEW_CREATE_FIELDS = frozenset(
    {
        "workspace_id",
        "review_type",
        "risk_categories",
        "source_actor_type",
        "source_actor_id",
        "title",
        "summary",
        "required_gates",
        "linked_records",
        "description",
        "priority",
        "sensitivity_rating",
        "confidence",
    }
)
REQUIRED_REVIEW_CREATE_FIELDS = frozenset(
    {
        "workspace_id",
        "review_type",
        "risk_categories",
        "source_actor_type",
        "source_actor_id",
        "title",
        "summary",
        "required_gates",
        "linked_records",
    }
)
ALLOWED_DECISION_CREATE_FIELDS = frozenset(
    {
        "review_item_id",
        "decision_type",
        "decision_scope",
        "reviewer_actor_id",
        "target_records",
        "decision_summary",
        "decision_notes",
        "conditions",
        "revision_instructions",
        "park_reason",
        "block_reason",
        "sensitivity_rating",
    }
)
REQUIRED_DECISION_CREATE_FIELDS = frozenset(
    {
        "review_item_id",
        "decision_type",
        "decision_scope",
        "reviewer_actor_id",
        "target_records",
        "decision_summary",
    }
)
ALLOWED_SIGNAL_CANDIDATE_CREATE_FIELDS = frozenset(
    {
        "workspace_id",
        "workspace_type",
        "signal_type",
        "source_actor_type",
        "source_actor_id",
        "source_references",
        "summary",
        "evidence_summary",
        "sensitivity_rating",
        "confidence",
        "private_data_removed",
        "remaining_sensitivity_notes",
        "parent_signal_id",
        "raw_signal_id",
        "tags",
    }
)
REQUIRED_SIGNAL_CANDIDATE_CREATE_FIELDS = frozenset(
    {
        "workspace_id",
        "workspace_type",
        "signal_type",
        "source_actor_type",
        "source_actor_id",
        "source_references",
        "summary",
        "evidence_summary",
        "sensitivity_rating",
        "confidence",
        "private_data_removed",
        "remaining_sensitivity_notes",
    }
)
ALLOWED_REVIEW_TYPES = frozenset(
    {
        "strategy_review",
        "workspace_promotion_review",
        "material_workflow_change_review",
        "signal_sanitization_review",
    }
)
ALLOWED_RISK_CATEGORIES = frozenset(
    {
        "workspace_lifecycle",
        "strategy",
        "quality",
        "privacy",
        "signal_sanitization",
        "material_change",
    }
)
ALLOWED_REQUIRED_GATES = frozenset(
    {
        "strategy_review_gate",
        "workspace_promotion_gate",
        "signal_sanitization_gate",
        "quality_review_gate",
    }
)
ALLOWED_SOURCE_ACTOR_TYPES = frozenset({"human", "system"})
ALLOWED_SIGNAL_SOURCE_ACTOR_TYPES = frozenset({"human", "system"})
ALLOWED_LINKED_RECORD_TYPES = frozenset(
    {
        "workspace_config",
        "audit_record",
        "artifact",
        "signal_candidate",
        "human_decision",
    }
)
ALLOWED_DECISION_TYPES = frozenset(
    {
        "approve",
        "approve_with_changes",
        "reject",
        "request_revision",
        "park",
        "block",
    }
)
ALLOWED_DECISION_SCOPES = frozenset({"review_item"})
ALLOWED_TARGET_RECORD_TYPES = frozenset(
    {
        "review_item",
        "workspace_config",
        "audit_record",
        "artifact",
        "signal_candidate",
    }
)
ALLOWED_SIGNAL_TYPES = frozenset(
    {
        "customer_need_pattern",
        "keyword_pattern",
        "market_gap",
        "competitor_pattern",
        "workflow_problem",
        "quality_issue",
        "content_gap",
        "service_demand_pattern",
        "product_opportunity",
        "policy_or_rights_risk",
        "data_quality_note",
        "research_finding",
        "strategy_observation",
        "other",
    }
)
ALLOWED_LOW_RISK_SIGNAL_SENSITIVITY_RATINGS = frozenset({"low", "medium"})
ALLOWED_SIGNAL_CONFIDENCE_VALUES = frozenset({"low", "medium", "high", "unknown"})
ALLOWED_SIGNAL_SOURCE_REFERENCE_TYPES = frozenset(
    {
        "artifact",
        "agent_run",
        "review_item",
        "human_decision",
        "audit_record",
        "workflow",
        "external_reference",
        "observatory_query_result",
        "manual_note",
        "business_intake",
        "workspace_config",
    }
)
REVIEW_STATUS_BY_DECISION_TYPE = {
    "approve": "approved",
    "approve_with_changes": "approved_with_changes",
    "reject": "rejected",
    "request_revision": "revision_requested",
    "park": "parked",
    "block": "blocked",
}
RESOLVED_REVIEW_STATUSES = frozenset(REVIEW_STATUS_BY_DECISION_TYPE.values())


class PersistenceProofError(Exception):
    """Base error for the persistence proof."""


class ValidationError(PersistenceProofError):
    """Raised when caller input violates the proof contract."""


class AuditWriteError(PersistenceProofError):
    """Raised when audit writing fails inside the transaction."""


class NotFoundError(PersistenceProofError):
    """Raised when an expected record does not exist."""


@dataclass(frozen=True)
class CreateWorkspaceConfigResult:
    """Result of a successful workspace config create operation."""

    workspace_id: str
    audit_record_id: str
    workspace_record: dict[str, Any]
    audit_record: dict[str, Any]


@dataclass(frozen=True)
class UpdateWorkspaceConfigResult:
    """Result of a successful workspace config update operation."""

    workspace_id: str
    audit_record_id: str
    workspace_record: dict[str, Any]
    audit_record: dict[str, Any]


@dataclass(frozen=True)
class CreateReviewQueueItemResult:
    """Result of a successful review queue item create operation."""

    review_item_id: str
    audit_record_id: str
    review_item_record: dict[str, Any]
    audit_record: dict[str, Any]


@dataclass(frozen=True)
class RecordHumanDecisionResult:
    """Result of a successful human decision record operation."""

    human_decision_id: str
    audit_record_id: str
    human_decision_record: dict[str, Any]
    review_item_record: dict[str, Any]
    audit_record: dict[str, Any]


@dataclass(frozen=True)
class CreateSignalCandidateResult:
    """Result of a successful signal candidate create operation."""

    signal_id: str
    audit_record_id: str
    signal_candidate_record: dict[str, Any]
    audit_record: dict[str, Any]


Clock = Callable[[], datetime]
IdFactory = Callable[[], str]


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""

    return datetime.now(UTC).replace(microsecond=0)


def format_timestamp(value: datetime) -> str:
    """Format timestamps as ISO 8601 UTC with a Z suffix."""

    if value.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
        self.fail_audit_write = fail_audit_write
        self.connection.row_factory = sqlite3.Row

    def initialize_schema(self) -> None:
        """Create only the tables authorized by the proof."""

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS workspace_configs (
                workspace_id TEXT PRIMARY KEY,
                record_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                record_revision INTEGER NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_records (
                audit_record_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor_type TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                result_status TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                record_revision INTEGER NOT NULL,
                record_json TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS review_queue_items (
                review_item_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                status TEXT NOT NULL,
                review_type TEXT NOT NULL,
                audit_record_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                record_revision INTEGER NOT NULL,
                record_json TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS human_decisions (
                human_decision_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                review_item_id TEXT NOT NULL,
                decision_type TEXT NOT NULL,
                decision_status TEXT NOT NULL,
                audit_record_id TEXT NOT NULL,
                decided_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                record_revision INTEGER NOT NULL,
                record_json TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS signal_candidates (
                signal_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                signal_form TEXT NOT NULL,
                status TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                audit_record_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                record_revision INTEGER NOT NULL,
                record_json TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def create_workspace_config(
        self,
        *,
        assigned_workspace_id: str,
        workspace_config: Mapping[str, Any],
        actor_id: str = "system:local_persistence_proof",
    ) -> CreateWorkspaceConfigResult:
        """Create a workspace config and its audit record in one transaction."""

        self._validate_assigned_workspace_id(assigned_workspace_id)
        clean_config = self._validate_workspace_config_payload(workspace_config)
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

        self._validate_assigned_workspace_id(workspace_id)
        clean_config = self._validate_workspace_config_payload(workspace_config)
        existing_record = self.get_workspace_config(workspace_id)
        if existing_record is None:
            raise NotFoundError("workspace config does not exist")
        self._validate_update_does_not_change_deferred_runtime_authority(
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

        clean_item = self._validate_review_queue_item_payload(review_item)
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

        clean_decision = self._validate_human_decision_payload(human_decision)
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

        clean_candidate = self._validate_signal_candidate_payload(signal_candidate)
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

    @staticmethod
    def _validate_update_does_not_change_deferred_runtime_authority(
        existing_record: Mapping[str, Any], clean_config: Mapping[str, Any]
    ) -> None:
        """Keep update proof from becoming lifecycle or runtime enablement."""

        if clean_config.get("status") != existing_record.get("status"):
            raise ValidationError("status changes are not authorized for the update proof")
        if clean_config.get("runtime") != existing_record.get("runtime"):
            raise ValidationError("runtime changes are not authorized for the update proof")

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

    @staticmethod
    def _validate_assigned_workspace_id(workspace_id: str) -> None:
        if not isinstance(workspace_id, str) or not workspace_id.strip():
            raise ValidationError("assigned_workspace_id must be a non-empty string")

    @staticmethod
    def _validate_workspace_config_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, Mapping):
            raise ValidationError("workspace_config must be a mapping")
        keys = set(payload.keys())
        forbidden = keys & FORBIDDEN_FIELDS
        if forbidden:
            raise ValidationError(f"forbidden fields present: {sorted(forbidden)}")
        forged = keys & SYSTEM_OWNED_WORKSPACE_FIELDS
        if forged:
            raise ValidationError(f"system-owned fields cannot be supplied: {sorted(forged)}")
        unknown = keys - ALLOWED_WORKSPACE_CREATE_FIELDS
        if unknown:
            raise ValidationError(f"unknown fields present: {sorted(unknown)}")
        missing = REQUIRED_WORKSPACE_CREATE_FIELDS - keys
        if missing:
            raise ValidationError(f"required fields missing: {sorted(missing)}")
        runtime = payload.get("runtime")
        if not isinstance(runtime, Mapping):
            raise ValidationError("runtime must be a mapping")
        if runtime.get("scheduled_allowed") is not False:
            raise ValidationError("scheduled_allowed must be false for the proof")
        if runtime.get("watch_mode_allowed") is not False:
            raise ValidationError("watch_mode_allowed must be false for the proof")
        if payload.get("allowed_agents") != []:
            raise ValidationError("allowed_agents must be empty for the proof")
        if payload.get("external_references", []) != []:
            raise ValidationError("external_references must be empty for the proof")
        return dict(payload)

    @staticmethod
    def _validate_review_queue_item_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, Mapping):
            raise ValidationError("review_item must be a mapping")
        keys = set(payload.keys())
        forbidden = keys & FORBIDDEN_FIELDS
        if forbidden:
            raise ValidationError(f"forbidden fields present: {sorted(forbidden)}")
        forged = keys & SYSTEM_OWNED_REVIEW_FIELDS
        if forged:
            raise ValidationError(f"system-owned fields cannot be supplied: {sorted(forged)}")
        unknown = keys - ALLOWED_REVIEW_CREATE_FIELDS
        if unknown:
            raise ValidationError(f"unknown fields present: {sorted(unknown)}")
        missing = REQUIRED_REVIEW_CREATE_FIELDS - keys
        if missing:
            raise ValidationError(f"required fields missing: {sorted(missing)}")

        clean_item = dict(payload)
        workspace_id = clean_item.get("workspace_id")
        if not isinstance(workspace_id, str) or not workspace_id.strip():
            raise ValidationError("workspace_id must be a non-empty string")
        _validate_non_empty_string(clean_item, "source_actor_id")
        _validate_non_empty_string(clean_item, "title")
        _validate_non_empty_string(clean_item, "summary")

        source_actor_type = clean_item.get("source_actor_type")
        if source_actor_type not in ALLOWED_SOURCE_ACTOR_TYPES:
            raise ValidationError("unsupported source_actor_type")
        review_type = clean_item.get("review_type")
        if review_type not in ALLOWED_REVIEW_TYPES:
            raise ValidationError("unsupported review_type")
        _validate_allowed_string_sequence(
            clean_item.get("risk_categories"),
            "risk_categories",
            ALLOWED_RISK_CATEGORIES,
            require_non_empty=True,
        )
        _validate_allowed_string_sequence(
            clean_item.get("required_gates"),
            "required_gates",
            ALLOWED_REQUIRED_GATES,
            require_non_empty=True,
        )
        _validate_linked_records(clean_item.get("linked_records"), ALLOWED_LINKED_RECORD_TYPES)
        return clean_item

    @staticmethod
    def _validate_human_decision_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, Mapping):
            raise ValidationError("human_decision must be a mapping")
        keys = set(payload.keys())
        forbidden = keys & FORBIDDEN_FIELDS
        if forbidden:
            raise ValidationError(f"forbidden fields present: {sorted(forbidden)}")
        forged = keys & SYSTEM_OWNED_DECISION_FIELDS
        if forged:
            raise ValidationError(f"system-owned fields cannot be supplied: {sorted(forged)}")
        unknown = keys - ALLOWED_DECISION_CREATE_FIELDS
        if unknown:
            raise ValidationError(f"unknown fields present: {sorted(unknown)}")
        missing = REQUIRED_DECISION_CREATE_FIELDS - keys
        if missing:
            raise ValidationError(f"required fields missing: {sorted(missing)}")

        clean_decision = dict(payload)
        _validate_non_empty_string(clean_decision, "review_item_id")
        _validate_non_empty_string(clean_decision, "reviewer_actor_id")
        _validate_non_empty_string(clean_decision, "decision_summary")
        if not clean_decision["reviewer_actor_id"].startswith("human:"):
            raise ValidationError("reviewer_actor_id must identify a human actor")
        decision_type = clean_decision.get("decision_type")
        if decision_type not in ALLOWED_DECISION_TYPES:
            raise ValidationError("unsupported decision_type")
        decision_scope = clean_decision.get("decision_scope")
        if decision_scope not in ALLOWED_DECISION_SCOPES:
            raise ValidationError("unsupported decision_scope")
        _validate_linked_records(clean_decision.get("target_records"), ALLOWED_TARGET_RECORD_TYPES)
        return clean_decision

    @staticmethod
    def _validate_signal_candidate_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, Mapping):
            raise ValidationError("signal_candidate must be a mapping")
        keys = set(payload.keys())
        forbidden = keys & FORBIDDEN_FIELDS
        if forbidden:
            raise ValidationError(f"forbidden fields present: {sorted(forbidden)}")
        forged = keys & SYSTEM_OWNED_SIGNAL_FIELDS
        if forged:
            raise ValidationError(f"system-owned fields cannot be supplied: {sorted(forged)}")
        unknown = keys - ALLOWED_SIGNAL_CANDIDATE_CREATE_FIELDS
        if unknown:
            raise ValidationError(f"unknown fields present: {sorted(unknown)}")
        missing = REQUIRED_SIGNAL_CANDIDATE_CREATE_FIELDS - keys
        if missing:
            raise ValidationError(f"required fields missing: {sorted(missing)}")

        clean_candidate = dict(payload)
        _validate_non_empty_string(clean_candidate, "workspace_id")
        _validate_non_empty_string(clean_candidate, "workspace_type")
        _validate_non_empty_string(clean_candidate, "source_actor_id")
        _validate_non_empty_string(clean_candidate, "summary")
        _validate_non_empty_string(clean_candidate, "evidence_summary")
        _validate_non_empty_string(clean_candidate, "remaining_sensitivity_notes")

        signal_type = clean_candidate.get("signal_type")
        if signal_type not in ALLOWED_SIGNAL_TYPES:
            raise ValidationError("unsupported signal_type")
        source_actor_type = clean_candidate.get("source_actor_type")
        if source_actor_type not in ALLOWED_SIGNAL_SOURCE_ACTOR_TYPES:
            raise ValidationError("unsupported source_actor_type")
        sensitivity = clean_candidate.get("sensitivity_rating")
        if sensitivity not in ALLOWED_LOW_RISK_SIGNAL_SENSITIVITY_RATINGS:
            raise ValidationError("unsupported sensitivity_rating for candidate proof")
        confidence = clean_candidate.get("confidence")
        if confidence not in ALLOWED_SIGNAL_CONFIDENCE_VALUES:
            raise ValidationError("unsupported confidence")
        if clean_candidate.get("private_data_removed") is not True:
            raise ValidationError("private_data_removed must be true for signal candidates")
        _validate_linked_records(
            clean_candidate.get("source_references"), ALLOWED_SIGNAL_SOURCE_REFERENCE_TYPES
        )
        tags = clean_candidate.get("tags", [])
        if not isinstance(tags, Sequence) or isinstance(tags, (str, bytes)):
            raise ValidationError("tags must be an array")
        if any(not isinstance(tag, str) or not tag.strip() for tag in tags):
            raise ValidationError("tags must contain only non-empty strings")
        return clean_candidate


def _validate_non_empty_string(payload: Mapping[str, Any], field_name: str) -> None:
    value = payload.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} must be a non-empty string")


def _validate_allowed_string_sequence(
    value: Any, field_name: str, allowed_values: frozenset[str], *, require_non_empty: bool
) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValidationError(f"{field_name} must be an array")
    if require_non_empty and not value:
        raise ValidationError(f"{field_name} must not be empty")
    invalid_values = [item for item in value if not isinstance(item, str) or item not in allowed_values]
    if invalid_values:
        raise ValidationError(f"unsupported {field_name}: {invalid_values}")


def _validate_linked_records(value: Any, allowed_record_types: frozenset[str]) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValidationError("linked_records must be an array")
    for record in value:
        if not isinstance(record, Mapping):
            raise ValidationError("linked_records entries must be mappings")
        record_type = record.get("record_type")
        record_id = record.get("record_id")
        relationship = record.get("relationship")
        if record_type not in allowed_record_types:
            raise ValidationError("unsupported linked record type")
        if not isinstance(record_id, str) or not record_id.strip():
            raise ValidationError("linked record_id must be a non-empty string")
        if not isinstance(relationship, str) or not relationship.strip():
            raise ValidationError("linked relationship must be a non-empty string")
        allowed_keys = {"record_type", "record_id", "relationship"}
        extra_keys = set(record.keys()) - allowed_keys
        if extra_keys:
            raise ValidationError(f"unknown linked record fields: {sorted(extra_keys)}")


def _json_dumps(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))