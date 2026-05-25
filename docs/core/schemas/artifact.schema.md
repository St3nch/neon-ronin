# Artifact Schema

## Purpose

This document defines the P1 artifact schema for Neon Ronin.

An artifact is a produced or referenced output from a workspace, workflow, human, agent, review process, or integration.

Artifacts include drafts, reports, research packets, QA checklists, recommendation packets, templates, exported files, delivery-ready files, sample assets, and supporting notes.

Artifact records exist so Neon Ronin can track what was produced, where it lives, who or what created it, what workflow it belongs to, what review state it is in, and what evidence/provenance supports it.

## Schema Status

```text
P1 planning schema
```

This is an implementation-facing planning document.

It is not yet a database migration, JSON Schema file, Pydantic model, TypeScript type, or API contract.

## Ownership Category

Artifact ownership is split:

| Artifact Layer | Ownership |
|---|---|
| Artifact metadata | Core-owned data |
| Artifact content | Usually workspace-owned data |
| External artifact reference | Referenced-only or integration-owned data |
| Derived artifact summary | Derived data |

Neon Ronin core may own artifact metadata so workflows, review items, agent runs, and audit records can reference artifacts consistently.

Neon Ronin core should not automatically own artifact contents.

## Core Rule

```text
Artifact metadata can be core-tracked.
Artifact content stays in its proper owner boundary.
```

A customer report, draft, client file, marketplace listing draft, or workspace strategy note is not global core data merely because Neon Ronin tracks it.

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `artifact_id` | string | system-owned | Stable unique artifact id |
| `workspace_id` | string | system/reference | Workspace that owns or scopes the artifact |
| `artifact_type` | enum | human/system-owned | Type of artifact |
| `status` | enum | system-governed | Current artifact lifecycle status |
| `content_scope` | enum | system/human-owned | Who owns or may access the content |
| `storage_reference` | object | referenced-only | Path, URI, external reference, or storage pointer |
| `title` | string | human/source-owned | Human-readable artifact title |
| `summary` | string | human/source-owned | Short summary without private payload dump |
| `creator_actor_type` | enum | system/source-owned | Actor type that created artifact metadata/content |
| `creator_actor_id` | string | system/source-owned | Actor id that created artifact metadata/content |
| `source_references` | array object | referenced-only | Inputs, runs, workflows, or prior artifacts that informed this artifact |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |
| `audit_record_ids` | array string | system/reference | Audit records related to artifact creation/change |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `workflow_id` | string/null | referenced-only | Workflow that produced or uses the artifact |
| `agent_run_id` | string/null | referenced-only | Agent run that produced the artifact if applicable |
| `review_item_ids` | array string | referenced-only | Review items linked to this artifact |
| `human_decision_ids` | array string | referenced-only | Human decisions linked to this artifact |
| `parent_artifact_id` | string/null | referenced-only | Prior artifact version/source artifact |
| `version_label` | string/null | human/system-owned | Human-readable version label |
| `content_format` | enum/string | source/system-owned | Markdown, PDF, CSV, XLSX, image, JSON, etc. |
| `file_name` | string/null | referenced-only | File name if file-backed |
| `file_hash` | string/null | system-owned | Optional content hash for integrity if available |
| `sensitivity_rating` | enum | source/system-owned | Sensitivity/privacy rating |
| `confidence` | enum/null | source/system-owned | Confidence if artifact is analytic/recommendation output |
| `delivery_ready` | boolean | system/human-owned | Whether artifact has passed required review for delivery |
| `public_use_allowed` | boolean | human/system-owned | Whether artifact may be used publicly |
| `consent_reference_id` | string/null | referenced-only | Consent record reference if public use depends on consent |
| `tags` | array string | bounded/source-owned | Bounded organizational tags |
| `schema_version` | string | system-owned | Schema/contract version used to validate this record shape |
| `record_revision` | integer | system-owned | Monotonic governed update/correction revision for this record |

## Valid Artifact Types

Initial artifact types:

```text
research_packet
recommendation_packet
draft_report
final_report
sample_report
report_template
qa_checklist
action_plan
keyword_table
spreadsheet_deliverable
pdf_export
markdown_source
public_preview
gallery_asset
video_script
intake_summary
delivery_message
signal_support_note
blocked_action_report
workflow_note
other
```

Artifact types should remain business-neutral.

Do not create specific-business, provider-specific, marketplace-specific, or channel-specific artifact types in core.

## Valid Statuses

Canonical artifact statuses:

```text
draft
in_review
approved
approved_with_changes
revision_requested
rejected
parked
blocked
delivery_ready
delivered
published
archived
retired
```

## Status Transition Rules

Allowed transitions:

| From | To | Requirement |
|---|---|---|
| `draft` | `in_review` | Artifact submitted for review |
| `draft` | `archived` | Artifact abandoned or preserved only for history |
| `in_review` | `approved` | Human approves |
| `in_review` | `approved_with_changes` | Human approves with edits |
| `in_review` | `revision_requested` | Human requests revision |
| `in_review` | `rejected` | Human rejects |
| `in_review` | `parked` | Human parks |
| `in_review` | `blocked` | System/human blocks |
| `revision_requested` | `draft` | Artifact revised |
| `approved` | `delivery_ready` | Delivery gate satisfied if applicable |
| `approved_with_changes` | `delivery_ready` | Required edits complete and delivery gate satisfied |
| `delivery_ready` | `delivered` | Human-approved delivery occurs |
| `delivery_ready` | `published` | Human-approved publishing occurs |
| any non-terminal | `archived` | Human/system archives with audit |
| any non-terminal | `retired` | Human/system retires with audit |

A status transition must not bypass required review gates.

## Content Scope Values

Canonical values:

```text
workspace_private
core_metadata_only
observatory_generalized
public_sample
external_reference_only
integration_owned
restricted
unknown
```

Default posture should be `workspace_private` unless clearly safer.

## Storage Reference Object

Recommended shape:

```yaml
storage_reference:
  storage_type: local_path | repo_path | external_uri | external_reference | object_store | none
  reference: string
  external_reference_id: string | null
  content_stored_in_core: false
```

Rules:

- storage references are pointers, not ownership transfers
- raw credentials must not appear in storage references
- external provider details belong in external reference records later
- core should not store private content by default

## System-Owned Fields

System-owned fields should include:

- `artifact_id`
- `created_at`
- `updated_at`
- `audit_record_ids`
- `file_hash` if computed by system
- system-computed status transitions
- `schema_version`
- `record_revision`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless governed correction allows change:

- `artifact_id`
- original `workspace_id`
- original `creator_actor_type`
- original `creator_actor_id`
- original `created_at`
- original source references for initial creation

Revisions should use versioning or parent artifact references instead of rewriting origin history.

## Provenance Requirements

Artifact records must preserve:

- workspace scope
- creator actor
- source inputs
- source workflow or run if applicable
- parent artifact/version if applicable
- review items and human decisions
- storage reference
- audit records for creation/status changes
- public-use consent if applicable

## Audit Requirements

The following events must generate audit records:

- artifact created
- artifact updated
- artifact submitted for review
- artifact approved
- artifact rejected
- revision requested
- artifact marked delivery ready
- artifact delivered
- artifact published
- artifact archived or retired
- public use permission changed
- storage reference changed

## Lifecycle Rules

Artifacts must obey workspace lifecycle:

- `idea` workspaces should not create operational artifacts.
- `onboarding` workspaces may create planning artifacts.
- `manual_test` workspaces may create draft/review artifacts through human-started workflows.
- `active` workspaces may create configured artifacts.
- `paused` workspaces may not create new artifacts.
- `retired` workspaces may not create new artifacts.

## Review Rules

Artifacts require review when they are:

- customer-facing
- public-facing
- external-write-related
- paid-action-related
- privacy-sensitive
- rights/IP/compliance-sensitive
- delivery-ready candidates
- Observatory-intake support artifacts

An artifact cannot approve itself.

An agent-created artifact requiring review must link to a review queue item.

## Public Use And Consent Rules

Artifacts based on fictional samples may be public if clearly labeled and approved.

Artifacts based on real client/customer work require consent before public use.

Consent should be referenced, not embedded as loose text.

No public use without consent where consent is required.

## Relationships To Other Records

Artifacts may reference or be referenced by:

- workspace config
- workflows
- agent runs
- review queue items
- human decisions
- audit records
- signal records
- external references
- business intake records

Artifacts should not own customer records, raw private evidence, or external provider resources.

## Forbidden Fields

Do not add fields such as:

```text
raw_customer_email
raw_customer_phone
full_customer_request
private_report_text
provider_token
api_key
oauth_refresh_token
full_external_payload
business_specific_report_template_body
etsy_listing_payload
printify_product_payload
fiverr_message_text
custom_data
```

Use workspace-owned content files, bounded summaries, references, or future governed schemas instead.

## Example Record

```yaml
artifact_id: art_service_sample_report_001
workspace_id: ws_future_service_workspace_001
artifact_type: sample_report
status: draft
content_scope: workspace_private
storage_reference:
  storage_type: repo_path
  reference: docs/workspaces/example-service-workspace/sample-report.md
  external_reference_id: null
  content_stored_in_core: false
title: Future Service Workspace Sample Report
summary: Fictional sample report source used as a service-workspace proof asset and future workflow input.
creator_actor_type: human
creator_actor_id: human_operator
source_references:
  - record_type: business_intake
    record_id: intake_future_service_workspace_001
    relationship: business_context
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
audit_record_ids:
  - audit_001
workflow_id: null
agent_run_id: null
review_item_ids: []
human_decision_ids: []
parent_artifact_id: null
version_label: draft-v1
content_format: markdown
file_name: sample-report.md
file_hash: null
sensitivity_rating: low
confidence: high
delivery_ready: false
public_use_allowed: false
consent_reference_id: null
tags:
  - sample
  - report
  - service-business
schema_version: schema_v1
record_revision: 1
```

## Validation Questions

Before accepting an artifact record, answer:

1. Is the artifact workspace-scoped?
2. Is the artifact type valid and business-neutral?
3. Is the content scope clear?
4. Is content stored in the right owner boundary?
5. Does the storage reference avoid credentials and private payload dumps?
6. Is creator provenance traceable?
7. Are source references thin references?
8. Does the artifact require review?
9. If public use is allowed, is consent or fictional-sample status clear?
10. Are audit records linked for meaningful state changes?
11. Does it avoid provider-specific fields in core?
12. Does it avoid unbounded metadata/custom data?

## Non-Goals

This schema does not define:

- artifact content body schema
- file storage architecture
- PDF generation implementation
- report template language
- customer records
- provider payload schemas
- UI preview behavior
- database tables

## Final Rule

```text
Track the artifact without stealing its ownership.
```
