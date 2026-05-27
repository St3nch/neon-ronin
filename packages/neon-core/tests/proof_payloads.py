"""Shared valid payloads for Neon Ronin first persistence proof tests.

These are test fixtures only. They do not add persistence behavior, tables,
schemas, runtime surfaces, agents, integrations, scheduled jobs, watch mode,
Observatory ingestion, customer-facing onboarding, SearchClarity onboarding,
or automation.
"""

from __future__ import annotations

from workspace_config_fixture import INTERNAL_RESEARCH_WORKSPACE_ID

VALID_REVIEW_ITEM = {
    "workspace_id": INTERNAL_RESEARCH_WORKSPACE_ID,
    "review_type": "strategy_review",
    "risk_categories": ["strategy"],
    "source_actor_type": "human",
    "source_actor_id": "human:operator",
    "title": "Review internal research direction",
    "summary": "Human review of a bounded internal research planning item.",
    "required_gates": ["strategy_review_gate"],
    "linked_records": [
        {
            "record_type": "workspace_config",
            "record_id": INTERNAL_RESEARCH_WORKSPACE_ID,
            "relationship": "review_context",
        }
    ],
    "description": "Keep the first executable review queue proof bounded.",
    "priority": "normal",
    "sensitivity_rating": "low",
    "confidence": "medium",
}

VALID_HUMAN_DECISION = {
    "review_item_id": "review_item_001",
    "decision_type": "approve",
    "decision_scope": "review_item",
    "reviewer_actor_id": "human:operator",
    "target_records": [
        {
            "record_type": "review_item",
            "record_id": "review_item_001",
            "relationship": "resolves_review",
        }
    ],
    "decision_summary": "Approved this bounded internal research review item.",
    "decision_notes": "No external action is authorized by this proof.",
    "conditions": [],
    "sensitivity_rating": "low",
}

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

VALID_WORKFLOW_RECORD = {
    "workflow_name": "Internal Research Manual Proof Workflow",
    "workflow_type": "manual_research",
    "scope_type": "workspace",
    "workspace_id": INTERNAL_RESEARCH_WORKSPACE_ID,
    "adapter_id": None,
    "allowed_workspace_types": ["internal_research"],
    "allowed_lifecycle_statuses": ["manual_test"],
    "allowed_runtime_modes": ["on_demand"],
    "steps": [
        {
            "step_id": "step_001",
            "step_name": "Capture manual research note",
            "step_type": "human_task",
            "required": True,
            "actor_type": "human",
            "allowed_agent_ids": [],
            "input_refs": ["workspace_config"],
            "output_refs": ["artifact"],
            "review_gate": None,
            "audit_event_type": "workflow_step_completed",
        },
        {
            "step_id": "step_002",
            "step_name": "Create metadata-only artifact",
            "step_type": "artifact_creation",
            "required": True,
            "actor_type": "human",
            "allowed_agent_ids": [],
            "input_refs": ["manual_note"],
            "output_refs": ["artifact"],
            "review_gate": None,
            "audit_event_type": "artifact_metadata_created",
        },
    ],
    "required_review_gates": ["quality_review_gate"],
    "expected_inputs": [
        {
            "input_type": "workspace_config",
            "required": True,
            "ownership": "workspace_owned",
        }
    ],
    "expected_outputs": [
        {
            "output_type": "artifact",
            "artifact_type": "markdown_source",
            "required": True,
            "ownership": "workspace_owned",
            "requires_review": True,
        }
    ],
    "audit_requirements": ["workflow_record_created", "artifact_metadata_created"],
    "description": "Manual workflow definition only; not a workflow engine or automation grant.",
    "version_label": "manual-test-v1",
    "trigger_types": ["human_started"],
    "allowed_agents": [],
    "forbidden_actions": ["external_action_execution", "scheduled_execution"],
    "handoff_rules": {
        "artifacts_requiring_review_go_to_review_queue": True,
        "failed_steps_create_audit_record": True,
    },
    "failure_behavior": {
        "on_missing_input": "block_or_request_revision",
        "on_failed_step": "create_audit_record",
    },
    "provenance_requirements": ["workspace_config", "audit_record"],
    "tags": ["persistence-proof"],
}
