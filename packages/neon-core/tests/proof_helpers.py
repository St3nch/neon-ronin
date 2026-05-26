"""Shared helpers for the Neon Ronin first persistence proof tests.

These helpers keep the hammer tests readable while preserving explicit proof cases.
They do not add persistence behavior, tables, agents, UI, integrations, scheduling,
watch mode, Observatory ingestion, customer-facing onboarding, SearchClarity
onboarding, or automation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
import re
import sqlite3
from collections.abc import Callable

from neon_ronin_core.persistence.sqlite_store import SQLitePersistenceProofStore
from workspace_config_fixture import (
    INTERNAL_RESEARCH_WORKSPACE_CONFIG,
    INTERNAL_RESEARCH_WORKSPACE_ID,
)

FIXED_TIME = datetime(2026, 5, 26, 12, 0, 0, tzinfo=UTC)
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
AUTHORIZED_TABLES = [
    "artifact_metadata",
    "audit_records",
    "human_decisions",
    "review_queue_items",
    "signal_candidates",
    "workflow_records",
    "workspace_configs",
]

ClockFactory = Callable[[], datetime]
IdFactory = Callable[[], str]


def make_store(
    *,
    fail_audit_write: bool = False,
    clock: ClockFactory | None = None,
    audit_id_factory: IdFactory | None = None,
    review_item_id_factory: IdFactory | None = None,
    human_decision_id_factory: IdFactory | None = None,
    signal_id_factory: IdFactory | None = None,
    artifact_id_factory: IdFactory | None = None,
    workflow_id_factory: IdFactory | None = None,
) -> SQLitePersistenceProofStore:
    """Create an initialized in-memory store for proof tests."""

    connection = sqlite3.connect(":memory:")
    store = SQLitePersistenceProofStore(
        connection,
        clock=clock or (lambda: FIXED_TIME),
        audit_id_factory=audit_id_factory,
        review_item_id_factory=review_item_id_factory,
        human_decision_id_factory=human_decision_id_factory,
        signal_id_factory=signal_id_factory,
        artifact_id_factory=artifact_id_factory,
        workflow_id_factory=workflow_id_factory,
        fail_audit_write=fail_audit_write,
    )
    store.initialize_schema()
    return store


def create_base_workspace(store: SQLitePersistenceProofStore) -> None:
    """Create the Internal Research workspace fixture in the provided store."""

    store.create_workspace_config(
        assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
        workspace_config=deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
    )


def assert_authorized_tables_only(testcase, store: SQLitePersistenceProofStore) -> None:
    """Assert schema initialization created exactly the authorized proof tables."""

    rows = store.connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()
    testcase.assertEqual([row["name"] for row in rows], AUTHORIZED_TABLES)
