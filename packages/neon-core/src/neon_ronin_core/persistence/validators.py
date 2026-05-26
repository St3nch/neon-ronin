"""Payload validators for the Neon Ronin first persistence proof."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .constants import (
    ALLOWED_ARTIFACT_CONFIDENCE_VALUES,
    ALLOWED_ARTIFACT_CONTENT_SCOPES,
    ALLOWED_ARTIFACT_CREATOR_ACTOR_TYPES,
    ALLOWED_ARTIFACT_METADATA_CREATE_FIELDS,
    ALLOWED_ARTIFACT_SENSITIVITY_RATINGS,
    ALLOWED_ARTIFACT_SOURCE_REFERENCE_TYPES,
    ALLOWED_ARTIFACT_TYPES,
    ALLOWED_CONTENT_FORMATS,
    ALLOWED_DECISION_CREATE_FIELDS,
    ALLOWED_DECISION_SCOPES,
    ALLOWED_DECISION_TYPES,
    ALLOWED_LINKED_RECORD_TYPES,
    ALLOWED_LOW_RISK_SIGNAL_SENSITIVITY_RATINGS,
    ALLOWED_REQUIRED_GATES,
    ALLOWED_REVIEW_CREATE_FIELDS,
    ALLOWED_REVIEW_TYPES,
    ALLOWED_RISK_CATEGORIES,
    ALLOWED_SIGNAL_CANDIDATE_CREATE_FIELDS,
    ALLOWED_SIGNAL_CONFIDENCE_VALUES,
    ALLOWED_SIGNAL_SOURCE_ACTOR_TYPES,
    ALLOWED_SIGNAL_SOURCE_REFERENCE_TYPES,
    ALLOWED_SIGNAL_TYPES,
    ALLOWED_SOURCE_ACTOR_TYPES,
    ALLOWED_STORAGE_TYPES,
    ALLOWED_TARGET_RECORD_TYPES,
    ALLOWED_WORKFLOW_CREATE_FIELDS,
    ALLOWED_WORKFLOW_INPUT_TYPES,
    ALLOWED_WORKFLOW_LIFECYCLE_STATUSES,
    ALLOWED_WORKFLOW_OUTPUT_TYPES,
    ALLOWED_WORKFLOW_RUNTIME_MODES,
    ALLOWED_WORKFLOW_SCOPE_TYPES,
    ALLOWED_WORKFLOW_STEP_ACTOR_TYPES,
    ALLOWED_WORKFLOW_STEP_TYPES,
    ALLOWED_WORKFLOW_TRIGGER_TYPES,
    ALLOWED_WORKFLOW_TYPES,
    FORBIDDEN_FIELDS,
    FORBIDDEN_STORAGE_REFERENCE_KEYS,
    FORBIDDEN_WORKFLOW_STEP_KEYS,
    FORBIDDEN_WORKFLOW_TRIGGER_TYPES,
    REQUIRED_ARTIFACT_METADATA_CREATE_FIELDS,
    REQUIRED_DECISION_CREATE_FIELDS,
    REQUIRED_REVIEW_CREATE_FIELDS,
    REQUIRED_SIGNAL_CANDIDATE_CREATE_FIELDS,
    REQUIRED_WORKFLOW_CREATE_FIELDS,
    REQUIRED_WORKSPACE_CREATE_FIELDS,
    SYSTEM_OWNED_ARTIFACT_FIELDS,
    SYSTEM_OWNED_DECISION_FIELDS,
    SYSTEM_OWNED_REVIEW_FIELDS,
    SYSTEM_OWNED_SIGNAL_FIELDS,
    SYSTEM_OWNED_WORKFLOW_FIELDS,
    SYSTEM_OWNED_WORKSPACE_FIELDS,
    ALLOWED_WORKSPACE_CREATE_FIELDS,
)
from .errors import ValidationError

def validate_update_does_not_change_deferred_runtime_authority(
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


def validate_assigned_workspace_id(workspace_id: str) -> None:
    if not isinstance(workspace_id, str) or not workspace_id.strip():
        raise ValidationError("assigned_workspace_id must be a non-empty string")


def validate_workspace_config_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
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


def validate_review_queue_item_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
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


def validate_human_decision_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
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


def validate_signal_candidate_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
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


def validate_artifact_metadata_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ValidationError("artifact_metadata must be a mapping")
    keys = set(payload.keys())
    forbidden = keys & FORBIDDEN_FIELDS
    if forbidden:
        raise ValidationError(f"forbidden fields present: {sorted(forbidden)}")
    forged = keys & SYSTEM_OWNED_ARTIFACT_FIELDS
    if forged:
        raise ValidationError(f"system-owned fields cannot be supplied: {sorted(forged)}")
    unknown = keys - ALLOWED_ARTIFACT_METADATA_CREATE_FIELDS
    if unknown:
        raise ValidationError(f"unknown fields present: {sorted(unknown)}")
    missing = REQUIRED_ARTIFACT_METADATA_CREATE_FIELDS - keys
    if missing:
        raise ValidationError(f"required fields missing: {sorted(missing)}")

    clean_artifact = dict(payload)
    _validate_non_empty_string(clean_artifact, "workspace_id")
    _validate_non_empty_string(clean_artifact, "title")
    _validate_non_empty_string(clean_artifact, "summary")
    _validate_non_empty_string(clean_artifact, "creator_actor_id")

    artifact_type = clean_artifact.get("artifact_type")
    if artifact_type not in ALLOWED_ARTIFACT_TYPES:
        raise ValidationError("unsupported artifact_type")
    content_scope = clean_artifact.get("content_scope")
    if content_scope not in ALLOWED_ARTIFACT_CONTENT_SCOPES:
        raise ValidationError("unsupported content_scope")
    creator_actor_type = clean_artifact.get("creator_actor_type")
    if creator_actor_type not in ALLOWED_ARTIFACT_CREATOR_ACTOR_TYPES:
        raise ValidationError("unsupported creator_actor_type")
    _validate_storage_reference(clean_artifact.get("storage_reference"))
    _validate_linked_records(
        clean_artifact.get("source_references"), ALLOWED_ARTIFACT_SOURCE_REFERENCE_TYPES
    )
    _validate_optional_string_array(clean_artifact.get("review_item_ids", []), "review_item_ids")
    _validate_optional_string_array(
        clean_artifact.get("human_decision_ids", []), "human_decision_ids"
    )
    if clean_artifact.get("delivery_ready", False) is not False:
        raise ValidationError("delivery_ready must be false for metadata create proof")
    if clean_artifact.get("public_use_allowed", False) is not False:
        raise ValidationError("public_use_allowed must be false for metadata create proof")
    content_format = clean_artifact.get("content_format")
    if content_format is not None and content_format not in ALLOWED_CONTENT_FORMATS:
        raise ValidationError("unsupported content_format")
    sensitivity = clean_artifact.get("sensitivity_rating")
    if sensitivity is not None and sensitivity not in ALLOWED_ARTIFACT_SENSITIVITY_RATINGS:
        raise ValidationError("unsupported sensitivity_rating")
    confidence = clean_artifact.get("confidence")
    if confidence is not None and confidence not in ALLOWED_ARTIFACT_CONFIDENCE_VALUES:
        raise ValidationError("unsupported confidence")
    tags = clean_artifact.get("tags", [])
    if not isinstance(tags, Sequence) or isinstance(tags, (str, bytes)):
        raise ValidationError("tags must be an array")
    if any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        raise ValidationError("tags must contain only non-empty strings")
    return clean_artifact


def validate_workflow_record_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ValidationError("workflow_record must be a mapping")
    keys = set(payload.keys())
    forbidden = keys & FORBIDDEN_FIELDS
    if forbidden:
        raise ValidationError(f"forbidden fields present: {sorted(forbidden)}")
    forged = keys & SYSTEM_OWNED_WORKFLOW_FIELDS
    if forged:
        raise ValidationError(f"system-owned fields cannot be supplied: {sorted(forged)}")
    unknown = keys - ALLOWED_WORKFLOW_CREATE_FIELDS
    if unknown:
        raise ValidationError(f"unknown fields present: {sorted(unknown)}")
    missing = REQUIRED_WORKFLOW_CREATE_FIELDS - keys
    if missing:
        raise ValidationError(f"required fields missing: {sorted(missing)}")

    clean_workflow = dict(payload)
    _validate_non_empty_string(clean_workflow, "workflow_name")
    _validate_non_empty_string(clean_workflow, "workspace_id")
    workflow_type = clean_workflow.get("workflow_type")
    if workflow_type not in ALLOWED_WORKFLOW_TYPES:
        raise ValidationError("unsupported workflow_type")
    scope_type = clean_workflow.get("scope_type")
    if scope_type not in ALLOWED_WORKFLOW_SCOPE_TYPES:
        raise ValidationError("unsupported scope_type")
    if clean_workflow.get("adapter_id") is not None:
        raise ValidationError("adapter_id must be null for workspace-scoped proof")
    _validate_allowed_string_sequence(
        clean_workflow.get("allowed_workspace_types"),
        "allowed_workspace_types",
        frozenset({"internal_research"}),
        require_non_empty=True,
    )
    _validate_allowed_string_sequence(
        clean_workflow.get("allowed_lifecycle_statuses"),
        "allowed_lifecycle_statuses",
        ALLOWED_WORKFLOW_LIFECYCLE_STATUSES,
        require_non_empty=True,
    )
    _validate_allowed_string_sequence(
        clean_workflow.get("allowed_runtime_modes"),
        "allowed_runtime_modes",
        ALLOWED_WORKFLOW_RUNTIME_MODES,
        require_non_empty=True,
    )
    triggers = clean_workflow.get("trigger_types", ["human_started"])
    _validate_allowed_string_sequence(
        triggers,
        "trigger_types",
        ALLOWED_WORKFLOW_TRIGGER_TYPES,
        require_non_empty=True,
    )
    forbidden_triggers = set(triggers) & FORBIDDEN_WORKFLOW_TRIGGER_TYPES
    if forbidden_triggers:
        raise ValidationError(f"forbidden trigger_types: {sorted(forbidden_triggers)}")
    if clean_workflow.get("allowed_agents", []) != []:
        raise ValidationError("allowed_agents must be empty for workflow proof")
    _validate_workflow_steps(clean_workflow.get("steps"))
    _validate_optional_string_array(
        clean_workflow.get("required_review_gates"), "required_review_gates"
    )
    _validate_workflow_io(
        clean_workflow.get("expected_inputs"), "expected_inputs", ALLOWED_WORKFLOW_INPUT_TYPES
    )
    _validate_workflow_io(
        clean_workflow.get("expected_outputs"), "expected_outputs", ALLOWED_WORKFLOW_OUTPUT_TYPES
    )
    _validate_optional_string_array(clean_workflow.get("audit_requirements"), "audit_requirements")
    _validate_optional_string_array(clean_workflow.get("forbidden_actions", []), "forbidden_actions")
    _validate_optional_string_array(
        clean_workflow.get("provenance_requirements", []), "provenance_requirements"
    )
    tags = clean_workflow.get("tags", [])
    _validate_optional_string_array(tags, "tags")
    return clean_workflow
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


def _validate_optional_string_array(value: Any, field_name: str) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValidationError(f"{field_name} must be an array")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValidationError(f"{field_name} must contain only non-empty strings")


def _validate_storage_reference(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise ValidationError("storage_reference must be a mapping")
    storage_type = value.get("storage_type")
    if storage_type not in ALLOWED_STORAGE_TYPES:
        raise ValidationError("unsupported storage_type")
    if value.get("content_stored_in_core") is not False:
        raise ValidationError("content_stored_in_core must be false")
    extra_forbidden = set(value.keys()) & FORBIDDEN_STORAGE_REFERENCE_KEYS
    if extra_forbidden:
        raise ValidationError(f"forbidden storage_reference fields: {sorted(extra_forbidden)}")
    allowed_keys = {
        "storage_type",
        "content_stored_in_core",
        "reference",
        "description",
    }
    extra_keys = set(value.keys()) - allowed_keys
    if extra_keys:
        raise ValidationError(f"unknown storage_reference fields: {sorted(extra_keys)}")
    reference = value.get("reference")
    if reference is not None and not isinstance(reference, str):
        raise ValidationError("storage_reference.reference must be a string when present")


def _validate_workflow_steps(value: Any) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValidationError("steps must be an array")
    if not value:
        raise ValidationError("steps must not be empty")
    seen_step_ids: set[str] = set()
    for step in value:
        if not isinstance(step, Mapping):
            raise ValidationError("steps entries must be mappings")
        forbidden_keys = set(step.keys()) & FORBIDDEN_WORKFLOW_STEP_KEYS
        if forbidden_keys:
            raise ValidationError(f"forbidden workflow step fields: {sorted(forbidden_keys)}")
        for field_name in ("step_id", "step_name", "step_type", "actor_type", "audit_event_type"):
            if not isinstance(step.get(field_name), str) or not step.get(field_name).strip():
                raise ValidationError(f"workflow step {field_name} must be a non-empty string")
        step_id = step["step_id"]
        if step_id in seen_step_ids:
            raise ValidationError("workflow step ids must be unique")
        seen_step_ids.add(step_id)
        if step.get("step_type") not in ALLOWED_WORKFLOW_STEP_TYPES:
            raise ValidationError("unsupported workflow step_type")
        if step.get("actor_type") not in ALLOWED_WORKFLOW_STEP_ACTOR_TYPES:
            raise ValidationError("unsupported workflow step actor_type")
        if step.get("allowed_agent_ids", []) != []:
            raise ValidationError("workflow step allowed_agent_ids must be empty")
        if not isinstance(step.get("required"), bool):
            raise ValidationError("workflow step required must be boolean")
        _validate_optional_string_array(step.get("input_refs", []), "workflow step input_refs")
        _validate_optional_string_array(step.get("output_refs", []), "workflow step output_refs")
        review_gate = step.get("review_gate")
        if review_gate is not None and not isinstance(review_gate, str):
            raise ValidationError("workflow step review_gate must be a string or null")
        allowed_keys = {
            "step_id",
            "step_name",
            "step_type",
            "required",
            "actor_type",
            "allowed_agent_ids",
            "input_refs",
            "output_refs",
            "review_gate",
            "audit_event_type",
        }
        extra_keys = set(step.keys()) - allowed_keys
        if extra_keys:
            raise ValidationError(f"unknown workflow step fields: {sorted(extra_keys)}")


def _validate_workflow_io(value: Any, field_name: str, allowed_types: frozenset[str]) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValidationError(f"{field_name} must be an array")
    for item in value:
        if not isinstance(item, Mapping):
            raise ValidationError(f"{field_name} entries must be mappings")
        type_key = "input_type" if field_name == "expected_inputs" else "output_type"
        item_type = item.get(type_key)
        if item_type not in allowed_types:
            raise ValidationError(f"unsupported {field_name} type")
        if not isinstance(item.get("required"), bool):
            raise ValidationError(f"{field_name} required must be boolean")
        ownership = item.get("ownership")
        if ownership is not None and ownership not in {"workspace_owned", "core_owned", "referenced_only"}:
            raise ValidationError(f"unsupported {field_name} ownership")
        if "requires_review" in item and not isinstance(item["requires_review"], bool):
            raise ValidationError(f"{field_name} requires_review must be boolean")
        allowed_keys = {type_key, "required", "ownership", "requires_review", "artifact_type", "review_type"}
        extra_keys = set(item.keys()) - allowed_keys
        if extra_keys:
            raise ValidationError(f"unknown {field_name} fields: {sorted(extra_keys)}")
