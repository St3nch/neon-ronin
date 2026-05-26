"""SQLite-backed first persistence proof for Neon Ronin.

This module intentionally implements only the approved first proof:

- workspace_configs
- audit_records
- workspace_config_create
- audit-first transaction behavior

It does not implement agents, UI, integrations, scheduled jobs, watch mode,
Observatory ingestion, customer-facing onboarding, or automation.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import sqlite3
from typing import Any
from uuid import uuid4

SCHEMA_VERSION = "schema_v1"
INITIAL_RECORD_REVISION = 1

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


class PersistenceProofError(Exception):
    """Base error for the first persistence proof."""


class ValidationError(PersistenceProofError):
    """Raised when caller input violates the first-proof contract."""


class AuditWriteError(PersistenceProofError):
    """Raised when audit writing fails inside the transaction."""


@dataclass(frozen=True)
class CreateWorkspaceConfigResult:
    """Result of a successful workspace config create operation."""

    workspace_id: str
    audit_record_id: str
    workspace_record: dict[str, Any]
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
    """Tiny SQLite store for the approved first local persistence proof."""

    def __init__(
        self,
        connection: sqlite3.Connection,
        *,
        clock: Clock = utc_now,
        audit_id_factory: IdFactory | None = None,
        fail_audit_write: bool = False,
    ) -> None:
        self.connection = connection
        self.clock = clock
        self.audit_id_factory = audit_id_factory or (lambda: f"audit_{uuid4().hex}")
        self.fail_audit_write = fail_audit_write
        self.connection.row_factory = sqlite3.Row

    def initialize_schema(self) -> None:
        """Create only the two tables authorized by the first proof."""

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
        audit_record_id = self.audit_id_factory()
        audit_record = {
            "audit_record_id": audit_record_id,
            "event_type": "workspace_created",
            "workspace_id": assigned_workspace_id,
            "actor_type": "system",
            "actor_id": actor_id,
            "action_type": "workspace_config_create",
            "target_type": "workspace_config",
            "target_id": assigned_workspace_id,
            "result_status": "succeeded",
            "occurred_at": now,
            "source_references": [],
            "summary": "Workspace config created by first local persistence proof.",
            "created_at": now,
            "schema_version": SCHEMA_VERSION,
            "record_revision": INITIAL_RECORD_REVISION,
        }

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
            audit_record_id=audit_record_id,
            workspace_record=workspace_record,
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

    def count_audit_records(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM audit_records").fetchone()[0])

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
            raise ValidationError("scheduled_allowed must be false for the first proof")
        if runtime.get("watch_mode_allowed") is not False:
            raise ValidationError("watch_mode_allowed must be false for the first proof")
        if payload.get("allowed_agents") != []:
            raise ValidationError("allowed_agents must be empty for the first proof")
        if payload.get("external_references", []) != []:
            raise ValidationError("external_references must be empty for the first proof")
        return dict(payload)


def _json_dumps(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))