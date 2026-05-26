"""Result dataclasses for the Neon Ronin first persistence proof."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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


@dataclass(frozen=True)
class CreateArtifactMetadataResult:
    """Result of a successful artifact metadata create operation."""

    artifact_id: str
    audit_record_id: str
    artifact_metadata_record: dict[str, Any]
    audit_record: dict[str, Any]


@dataclass(frozen=True)
class CreateWorkflowRecordResult:
    """Result of a successful workflow record create operation."""

    workflow_id: str
    audit_record_id: str
    workflow_record: dict[str, Any]
    audit_record: dict[str, Any]
