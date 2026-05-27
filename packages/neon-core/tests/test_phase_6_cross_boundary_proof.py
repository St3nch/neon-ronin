"""Cross-boundary Phase 6 proof tests for the first persistence slice.

These tests intentionally compose existing authorized persistence operations.
They do not add tables, schemas, runtime surfaces, agents, integrations,
scheduled jobs, watch mode, Observatory ingestion, customer-facing onboarding,
SearchClarity onboarding, or automation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
import unittest

from proof_helpers import (
    assert_authorized_tables_only,
    make_store,
)
from test_artifact_metadata_create import VALID_ARTIFACT_METADATA
from test_human_decision_record import VALID_HUMAN_DECISION
from test_review_queue_item_create import VALID_REVIEW_ITEM
from test_signal_candidate_create import VALID_SIGNAL_CANDIDATE
from test_workflow_record_create import VALID_WORKFLOW_RECORD
from workspace_config_fixture import (
    INTERNAL_RESEARCH_WORKSPACE_CONFIG,
    INTERNAL_RESEARCH_WORKSPACE_ID,
)

BASE_TIME = datetime(2026, 5, 26, 12, 0, 0, tzinfo=UTC)
WORKFLOW_TIME = datetime(2026, 5, 26, 13, 0, 0, tzinfo=UTC)
ARTIFACT_TIME = datetime(2026, 5, 26, 14, 0, 0, tzinfo=UTC)
REVIEW_TIME = datetime(2026, 5, 26, 15, 0, 0, tzinfo=UTC)
DECISION_TIME = datetime(2026, 5, 26, 16, 0, 0, tzinfo=UTC)
SIGNAL_TIME = datetime(2026, 5, 26, 17, 0, 0, tzinfo=UTC)


class Phase6CrossBoundaryProofTests(unittest.TestCase):
    def test_manual_workflow_artifact_review_decision_chain_uses_existing_boundaries(self):
        audit_ids = iter(
            [
                "audit_workspace_config_create_001",
                "audit_workflow_record_create_001",
                "audit_artifact_metadata_create_001",
                "audit_artifact_review_create_001",
                "audit_artifact_human_decision_001",
            ]
        )
        clock_values = iter(
            [BASE_TIME, WORKFLOW_TIME, ARTIFACT_TIME, REVIEW_TIME, DECISION_TIME]
        )
        store = make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
            workflow_id_factory=lambda: "workflow_record_001",
            artifact_id_factory=lambda: "artifact_metadata_001",
            review_item_id_factory=lambda: "review_item_artifact_001",
            human_decision_id_factory=lambda: "human_decision_artifact_001",
        )

        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )
        workflow_result = store.create_workflow_record(
            workflow_record=deepcopy(VALID_WORKFLOW_RECORD)
        )

        artifact_payload = deepcopy(VALID_ARTIFACT_METADATA)
        artifact_payload["workflow_id"] = workflow_result.workflow_id
        artifact_payload["source_references"] = [
            {
                "record_type": "workspace_config",
                "record_id": INTERNAL_RESEARCH_WORKSPACE_ID,
                "relationship": "artifact_context",
            },
            {
                "record_type": "workflow",
                "record_id": workflow_result.workflow_id,
                "relationship": "produced_by_manual_workflow_definition",
            },
        ]
        artifact_result = store.create_artifact_metadata(
            artifact_metadata=artifact_payload
        )

        review_payload = deepcopy(VALID_REVIEW_ITEM)
        review_payload.update(
            {
                "review_type": "strategy_review",
                "risk_categories": ["quality"],
                "title": "Review metadata-only internal research artifact",
                "summary": "Review a metadata-only artifact produced by the manual workflow proof.",
                "required_gates": ["quality_review_gate"],
                "linked_records": [
                    {
                        "record_type": "artifact",
                        "record_id": artifact_result.artifact_id,
                        "relationship": "review_target",
                    }
                ],
            }
        )
        review_result = store.create_review_queue_item(review_item=review_payload)

        decision_payload = deepcopy(VALID_HUMAN_DECISION)
        decision_payload.update(
            {
                "review_item_id": review_result.review_item_id,
                "decision_type": "approve_with_changes",
                "target_records": [
                    {
                        "record_type": "review_item",
                        "record_id": review_result.review_item_id,
                        "relationship": "resolves_review",
                    },
                    {
                        "record_type": "artifact",
                        "record_id": artifact_result.artifact_id,
                        "relationship": "reviewed_output",
                    },
                ],
                "decision_summary": "Approved metadata-only artifact evidence with human review notes.",
                "decision_notes": "No delivery, public use, execution, agent, or automation is authorized.",
                "conditions": ["artifact remains metadata-only proof evidence"],
            }
        )
        decision_result = store.record_human_decision(human_decision=decision_payload)

        assert_authorized_tables_only(self, store)
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_workflow_records(), 1)
        self.assertEqual(store.count_artifact_metadata(), 1)
        self.assertEqual(store.count_review_queue_items(), 1)
        self.assertEqual(store.count_human_decisions(), 1)
        self.assertEqual(store.count_signal_candidates(), 0)
        self.assertEqual(store.count_audit_records(), 5)

        workflow = store.get_workflow_record(workflow_result.workflow_id)
        artifact = store.get_artifact_metadata(artifact_result.artifact_id)
        review_item = store.get_review_queue_item(review_result.review_item_id)
        decision = store.get_human_decision(decision_result.human_decision_id)

        self.assertIsNotNone(workflow)
        self.assertIsNotNone(artifact)
        self.assertIsNotNone(review_item)
        self.assertIsNotNone(decision)
        assert workflow is not None
        assert artifact is not None
        assert review_item is not None
        assert decision is not None

        self.assertEqual(workflow["status"], "manual_test")
        self.assertEqual(workflow["allowed_agents"], [])
        self.assertEqual(workflow["trigger_types"], ["human_started"])
        self.assertEqual(workflow["allowed_runtime_modes"], ["on_demand"])

        self.assertEqual(artifact["workflow_id"], workflow_result.workflow_id)
        self.assertEqual(artifact["status"], "draft")
        self.assertEqual(artifact["content_scope"], "core_metadata_only")
        self.assertIs(artifact["storage_reference"]["content_stored_in_core"], False)
        self.assertIs(artifact["delivery_ready"], False)
        self.assertIs(artifact["public_use_allowed"], False)

        self.assertEqual(review_item["status"], "approved_with_changes")
        self.assertEqual(review_item["record_revision"], 2)
        self.assertEqual(
            review_item["decision"]["human_decision_id"],
            decision_result.human_decision_id,
        )
        self.assertEqual(decision["decision_type"], "approve_with_changes")
        self.assertEqual(decision["reviewer_actor_id"], "human:operator")

        for audit_id in (
            "audit_workspace_config_create_001",
            "audit_workflow_record_create_001",
            "audit_artifact_metadata_create_001",
            "audit_artifact_review_create_001",
            "audit_artifact_human_decision_001",
        ):
            self.assertIsNotNone(store.get_audit_record(audit_id))

    def test_signal_candidate_rejection_is_reviewed_without_observatory_ingestion(self):
        audit_ids = iter(
            [
                "audit_workspace_config_create_001",
                "audit_signal_candidate_create_001",
                "audit_signal_review_create_001",
                "audit_signal_rejection_decision_001",
            ]
        )
        clock_values = iter([BASE_TIME, SIGNAL_TIME, REVIEW_TIME, DECISION_TIME])
        store = make_store(
            clock=lambda: next(clock_values),
            audit_id_factory=lambda: next(audit_ids),
            signal_id_factory=lambda: "signal_candidate_001",
            review_item_id_factory=lambda: "review_item_signal_001",
            human_decision_id_factory=lambda: "human_decision_signal_001",
        )

        store.create_workspace_config(
            assigned_workspace_id=INTERNAL_RESEARCH_WORKSPACE_ID,
            workspace_config=deepcopy(INTERNAL_RESEARCH_WORKSPACE_CONFIG),
        )
        signal_result = store.create_signal_candidate(
            signal_candidate=deepcopy(VALID_SIGNAL_CANDIDATE)
        )

        review_payload = deepcopy(VALID_REVIEW_ITEM)
        review_payload.update(
            {
                "review_type": "signal_sanitization_review",
                "risk_categories": ["signal_sanitization", "privacy"],
                "title": "Review signal candidate for sanitization rejection",
                "summary": "Human review decides this candidate should not move forward.",
                "required_gates": ["signal_sanitization_gate"],
                "linked_records": [
                    {
                        "record_type": "signal_candidate",
                        "record_id": signal_result.signal_id,
                        "relationship": "sanitization_review_target",
                    }
                ],
            }
        )
        review_result = store.create_review_queue_item(review_item=review_payload)

        decision_payload = deepcopy(VALID_HUMAN_DECISION)
        decision_payload.update(
            {
                "review_item_id": review_result.review_item_id,
                "decision_type": "reject",
                "target_records": [
                    {
                        "record_type": "review_item",
                        "record_id": review_result.review_item_id,
                        "relationship": "resolves_review",
                    },
                    {
                        "record_type": "signal_candidate",
                        "record_id": signal_result.signal_id,
                        "relationship": "rejected_sanitization_candidate",
                    },
                ],
                "decision_summary": "Rejected signal candidate during human sanitization review.",
                "decision_notes": "No Observatory ingestion or sanitized signal persistence is authorized.",
                "conditions": [],
            }
        )
        decision_result = store.record_human_decision(human_decision=decision_payload)

        assert_authorized_tables_only(self, store)
        self.assertEqual(store.count_workspace_configs(), 1)
        self.assertEqual(store.count_signal_candidates(), 1)
        self.assertEqual(store.count_review_queue_items(), 1)
        self.assertEqual(store.count_human_decisions(), 1)
        self.assertEqual(store.count_audit_records(), 4)

        signal = store.get_signal_candidate(signal_result.signal_id)
        review_item = store.get_review_queue_item(review_result.review_item_id)
        decision = store.get_human_decision(decision_result.human_decision_id)

        self.assertIsNotNone(signal)
        self.assertIsNotNone(review_item)
        self.assertIsNotNone(decision)
        assert signal is not None
        assert review_item is not None
        assert decision is not None

        self.assertEqual(signal["signal_form"], "signal_candidate")
        self.assertEqual(signal["status"], "candidate")
        self.assertIs(signal["private_data_removed"], True)
        self.assertEqual(review_item["status"], "rejected")
        self.assertEqual(review_item["decision"]["decision_type"], "reject")
        self.assertEqual(decision["decision_type"], "reject")
        self.assertEqual(
            decision["target_records"][1]["relationship"],
            "rejected_sanitization_candidate",
        )

        table_names = [
            row["name"]
            for row in store.connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
            ).fetchall()
        ]
        self.assertNotIn("sanitized_signals", table_names)
        self.assertNotIn("observatory_records", table_names)


if __name__ == "__main__":
    unittest.main()
