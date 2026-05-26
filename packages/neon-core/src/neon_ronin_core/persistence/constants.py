"""Constants for the Neon Ronin first persistence proof."""

from __future__ import annotations

SCHEMA_VERSION = "schema_v1"
INITIAL_RECORD_REVISION = 1
INITIAL_REVIEW_STATUS = "open"
INITIAL_DECISION_STATUS = "recorded"
SIGNAL_CANDIDATE_FORM = "signal_candidate"
INITIAL_SIGNAL_CANDIDATE_STATUS = "candidate"
INITIAL_ARTIFACT_STATUS = "draft"
INITIAL_WORKFLOW_STATUS = "manual_test"

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
SYSTEM_OWNED_ARTIFACT_FIELDS = frozenset(
    {
        "artifact_id",
        "status",
        "audit_record_ids",
        "created_at",
        "updated_at",
        "schema_version",
        "record_revision",
    }
)
SYSTEM_OWNED_WORKFLOW_FIELDS = frozenset(
    {
        "workflow_id",
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
ALLOWED_ARTIFACT_METADATA_CREATE_FIELDS = frozenset(
    {
        "workspace_id",
        "artifact_type",
        "content_scope",
        "storage_reference",
        "title",
        "summary",
        "creator_actor_type",
        "creator_actor_id",
        "source_references",
        "workflow_id",
        "agent_run_id",
        "review_item_ids",
        "human_decision_ids",
        "parent_artifact_id",
        "version_label",
        "content_format",
        "file_hash",
        "sensitivity_rating",
        "confidence",
        "delivery_ready",
        "public_use_allowed",
        "tags",
    }
)
REQUIRED_ARTIFACT_METADATA_CREATE_FIELDS = frozenset(
    {
        "workspace_id",
        "artifact_type",
        "content_scope",
        "storage_reference",
        "title",
        "summary",
        "creator_actor_type",
        "creator_actor_id",
        "source_references",
    }
)
ALLOWED_WORKFLOW_CREATE_FIELDS = frozenset(
    {
        "workflow_name",
        "workflow_type",
        "scope_type",
        "workspace_id",
        "adapter_id",
        "allowed_workspace_types",
        "allowed_lifecycle_statuses",
        "allowed_runtime_modes",
        "steps",
        "required_review_gates",
        "expected_inputs",
        "expected_outputs",
        "audit_requirements",
        "description",
        "version_label",
        "trigger_types",
        "allowed_agents",
        "forbidden_actions",
        "handoff_rules",
        "failure_behavior",
        "provenance_requirements",
        "tags",
    }
)
REQUIRED_WORKFLOW_CREATE_FIELDS = frozenset(
    {
        "workflow_name",
        "workflow_type",
        "scope_type",
        "workspace_id",
        "adapter_id",
        "allowed_workspace_types",
        "allowed_lifecycle_statuses",
        "allowed_runtime_modes",
        "steps",
        "required_review_gates",
        "expected_inputs",
        "expected_outputs",
        "audit_requirements",
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
ALLOWED_ARTIFACT_CREATOR_ACTOR_TYPES = frozenset({"human", "system"})
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
ALLOWED_ARTIFACT_TYPES = frozenset(
    {
        "keyword_table",
        "markdown_source",
        "public_preview",
        "research_note",
        "review_packet",
        "recommendation_packet",
        "template",
        "supporting_note",
    }
)
ALLOWED_ARTIFACT_CONTENT_SCOPES = frozenset(
    {"core_metadata_only", "workspace_private", "referenced_external"}
)
ALLOWED_STORAGE_TYPES = frozenset(
    {"local_path", "repo_path", "external_uri", "external_reference", "object_store", "none"}
)
ALLOWED_CONTENT_FORMATS = frozenset(
    {"markdown", "pdf", "csv", "xlsx", "image", "json", "text", "unknown"}
)
ALLOWED_ARTIFACT_SENSITIVITY_RATINGS = frozenset({"low", "medium", "unknown"})
ALLOWED_ARTIFACT_CONFIDENCE_VALUES = frozenset({"low", "medium", "high", "unknown"})
ALLOWED_ARTIFACT_SOURCE_REFERENCE_TYPES = frozenset(
    {
        "workspace_config",
        "review_item",
        "human_decision",
        "audit_record",
        "signal_candidate",
        "manual_note",
        "workflow",
        "agent_run",
        "artifact",
    }
)
FORBIDDEN_STORAGE_REFERENCE_KEYS = frozenset(
    {
        "credential",
        "credentials",
        "api_key",
        "token",
        "oauth_token",
        "oauth_refresh_token",
        "password",
        "secret",
        "content_body",
        "raw_content",
        "payload",
        "blob",
    }
)
ALLOWED_WORKFLOW_TYPES = frozenset(
    {
        "business_intake",
        "manual_research",
        "report_production",
        "artifact_review",
        "signal_capture",
        "signal_sanitization",
        "qa_review",
        "internal_strategy",
        "other",
    }
)
ALLOWED_WORKFLOW_SCOPE_TYPES = frozenset({"workspace"})
ALLOWED_WORKFLOW_LIFECYCLE_STATUSES = frozenset({"manual_test"})
ALLOWED_WORKFLOW_RUNTIME_MODES = frozenset({"on_demand"})
ALLOWED_WORKFLOW_TRIGGER_TYPES = frozenset({"human_started", "manual_test_started"})
FORBIDDEN_WORKFLOW_TRIGGER_TYPES = frozenset({"scheduled", "watch_mode", "external_event"})
ALLOWED_WORKFLOW_STEP_TYPES = frozenset(
    {
        "human_task",
        "review_gate",
        "artifact_creation",
        "signal_capture",
        "human_decision",
        "audit_event",
        "handoff",
        "blocked_or_escalated",
    }
)
ALLOWED_WORKFLOW_STEP_ACTOR_TYPES = frozenset({"human", "system"})
ALLOWED_WORKFLOW_INPUT_TYPES = frozenset(
    {"workspace_config", "artifact", "signal_candidate", "review_item", "human_decision", "manual_note"}
)
ALLOWED_WORKFLOW_OUTPUT_TYPES = frozenset(
    {"artifact", "signal_candidate", "review_queue_item", "human_decision", "audit_record"}
)
FORBIDDEN_WORKFLOW_STEP_KEYS = frozenset(
    {
        "provider_payload",
        "api_payload",
        "private_content",
        "content_body",
        "raw_content",
        "customer_record",
        "credential",
        "token",
        "api_key",
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
