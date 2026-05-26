"""SQLite schema creation for the Neon Ronin first persistence proof."""

from __future__ import annotations

import sqlite3

def initialize_schema(connection: sqlite3.Connection) -> None:
    """Create only the tables authorized by the proof."""

    connection.execute(
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
    connection.execute(
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
    connection.execute(
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
    connection.execute(
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
    connection.execute(
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
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS artifact_metadata (
            artifact_id TEXT PRIMARY KEY,
            workspace_id TEXT NOT NULL,
            artifact_type TEXT NOT NULL,
            status TEXT NOT NULL,
            content_scope TEXT NOT NULL,
            audit_record_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            schema_version TEXT NOT NULL,
            record_revision INTEGER NOT NULL,
            record_json TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS workflow_records (
            workflow_id TEXT PRIMARY KEY,
            workspace_id TEXT NOT NULL,
            workflow_type TEXT NOT NULL,
            scope_type TEXT NOT NULL,
            status TEXT NOT NULL,
            audit_record_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            schema_version TEXT NOT NULL,
            record_revision INTEGER NOT NULL,
            record_json TEXT NOT NULL
        )
        """
    )
    connection.commit()

