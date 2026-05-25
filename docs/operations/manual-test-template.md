# Manual Test Template

## Purpose

This template defines how Neon Ronin records manual workflow validation before automation, agents, integrations, scheduled work, watch mode, or active workspace promotion.

Manual tests prove that a workspace workflow can be performed safely, reviewed, audited, and traced before Neon Ronin tries to assist or automate it.

## Core Rule

```text
Manual proof comes before automation.
```

If a workflow cannot be described and tested manually, it is not ready for agent assistance or automation.

## When To Use This Template

Use this template when validating:

- Internal Research workspace workflows
- SearchClarity future service workflows
- business intake conversion
- artifact production
- review queue behavior
- signal capture and sanitization
- human decision recording
- audit record coverage
- permission boundary assumptions
- external integration planning without live action

## Test Header

```yaml
manual_test_id:
test_name:
workspace_id:
workspace_name:
workspace_type:
workspace_status:
workflow_id:
workflow_name:
test_date:
test_operator:
test_status: planned | running | passed | passed_with_notes | failed | blocked | parked
```

## Test Goal

Describe the exact thing being validated.

```text
Goal:
```

Good examples:

```text
Validate that Internal Research can create a research artifact, queue a review item, record a human decision, and produce an audit trail.
```

```text
Validate that a SearchClarity-style service report workflow can move from intake summary to draft artifact to QA review without customer delivery automation.
```

Bad example:

```text
Test Neon Ronin.
```

Too vague. Goblin bait.

## Scope

### In Scope

- [ ] workspace config assumptions
- [ ] workflow steps
- [ ] artifact creation
- [ ] review queue item creation
- [ ] human decision recording
- [ ] audit record expectations
- [ ] signal candidate creation
- [ ] sanitization review
- [ ] permission boundary check
- [ ] failure/block behavior

### Out Of Scope

- [ ] autonomous execution
- [ ] external live writes
- [ ] customer delivery
- [ ] credential use
- [ ] scheduled jobs
- [ ] watch mode
- [ ] marketplace publishing
- [ ] paid actions
- [ ] destructive actions

Add test-specific out-of-scope items:

```text
Out of scope:
```

## Preconditions

Required before test starts:

- [ ] workspace type is known
- [ ] workspace status allows manual test
- [ ] workflow being tested is defined
- [ ] expected artifacts are identified
- [ ] expected review gates are identified
- [ ] expected audit events are identified
- [ ] hard-no rules are identified
- [ ] private data boundaries are identified
- [ ] no real credentials are needed
- [ ] no external live action is needed

Notes:

```text
Precondition notes:
```

## Inputs

List all inputs used by the manual test.

| Input | Type | Owner Boundary | Source Reference | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

Input rules:

- do not use real secrets
- do not use unnecessary customer data
- classify private data before use
- prefer fictional/sample data for early tests
- preserve source references

## Expected Outputs

List all outputs expected.

| Output | Type | Owner Boundary | Review Required? | Notes |
|---|---|---|---|---|
|  | artifact | workspace-owned content / core metadata | yes/no |  |
|  | review item | core-owned | yes |  |
|  | human decision | core-owned | n/a |  |
|  | audit record | core-owned | n/a |  |
|  | signal candidate | workspace-owned | yes |  |

## Workflow Steps

Record each manual step.

| Step | Actor | Action | Input Ref | Output Ref | Expected Gate/Audit | Result |
|---|---|---|---|---|---|---|
| 1 | human |  |  |  |  | planned |
| 2 | human |  |  |  |  | planned |
| 3 | human |  |  |  |  | planned |

## Review Gates Tested

- [ ] quality gate
- [ ] customer delivery gate
- [ ] data privacy gate
- [ ] rights and compliance gate
- [ ] signal sanitization gate
- [ ] strategy review gate
- [ ] external write gate
- [ ] credential permission gate

For each gate tested:

```text
Gate:
Input:
Decision needed:
Expected output:
```

## Human Decisions Expected

List expected human decisions.

| Decision | Target | Decision Type | Scope | Audit Required? |
|---|---|---|---|---|
|  |  | approve/reject/revise/park/block |  | yes |

Rules:

- decisions must be scoped
- decisions must not create broad permission by accident
- decisions must preserve provenance
- decisions must create audit records when meaningful

## Audit Events Expected

Check expected audit coverage.

- [ ] manual test started
- [ ] workspace config referenced
- [ ] workflow step completed
- [ ] artifact created
- [ ] review item created
- [ ] human decision recorded
- [ ] signal candidate created
- [ ] sanitization decision recorded
- [ ] blocked action recorded
- [ ] failed step recorded
- [ ] manual test completed

Additional expected audit events:

```text
Add here.
```

## Failure Cases To Test

At least one failure/block case should be tested where practical.

Potential failure cases:

- [ ] missing required input
- [ ] missing provenance
- [ ] artifact requires review before delivery
- [ ] signal candidate contains private data
- [ ] permission scope denies action
- [ ] workspace lifecycle disallows action
- [ ] external integration is deferred
- [ ] credential reference missing
- [ ] unknown field or forbidden field appears

Failure case selected:

```text
Failure case:
Expected result:
Expected audit:
Expected review/escalation:
```

## Signal Handling

If signals are part of the test:

- [ ] raw signal remains workspace-owned
- [ ] signal candidate is created separately
- [ ] private data removed/generalized
- [ ] sanitization review item created
- [ ] human decision required before Observatory intake
- [ ] rejected/parked signals do not proceed
- [ ] audit records trace signal lifecycle

Signal notes:

```text
Signal notes:
```

## Artifact Handling

If artifacts are part of the test:

- [ ] artifact metadata can be tracked
- [ ] artifact content owner is clear
- [ ] storage reference is safe
- [ ] review status is clear
- [ ] public-use/consent status is clear if applicable
- [ ] delivery-ready status is not assumed
- [ ] audit records trace artifact state changes

Artifact notes:

```text
Artifact notes:
```

## Permission And Hard-No Check

Confirm:

- [ ] no autonomous publishing
- [ ] no autonomous spending
- [ ] no autonomous customer messaging
- [ ] no autonomous customer delivery
- [ ] no autonomous credential changes
- [ ] no autonomous destructive actions
- [ ] no agent self-approval
- [ ] no raw data to Observatory
- [ ] no secrets in docs/artifacts/logs/prompts
- [ ] no external integration domain promoted by accident

Notes:

```text
Permission/hard-no notes:
```

## Test Result

Select one:

- [ ] passed
- [ ] passed with notes
- [ ] failed
- [ ] blocked
- [ ] parked

Summary:

```text
Result summary:
```

## Issues Found

| Issue | Severity | Boundary Affected | Follow-Up |
|---|---|---|---|
|  | low/medium/high/critical |  |  |

## Reusable Capability Findings

Did this test reveal reusable Neon Ronin capability needs?

| Finding | Classification | Promote? | Notes |
|---|---|---|---|
|  | core / adapter / workspace / integration / out-of-scope | yes/no/park |  |

## Workspace-Specific Findings

List items that must remain workspace-owned.

```text
Workspace-specific findings:
```

## Deferred Domain Warnings

List any deferred domains touched.

- [ ] marketplace integration
- [ ] Fiverr automation
- [ ] Etsy integration
- [ ] Printify integration
- [ ] scheduled agents
- [ ] watch mode
- [ ] customer messaging automation
- [ ] external live write
- [ ] Tauri UI
- [ ] LangGraph/Hermes
- [ ] multi-user roles
- [ ] cloud sync

Notes:

```text
Deferred domain notes:
```

## Follow-Up Actions

- [ ] Action 1
- [ ] Action 2
- [ ] Action 3

## Promotion Recommendation

Should the workflow move forward?

- [ ] remain in planning
- [ ] repeat manual test
- [ ] revise workflow
- [ ] revise schema/contract docs
- [ ] create ADR
- [ ] allow limited agent assistance later
- [ ] allow workspace promotion consideration
- [ ] park
- [ ] reject

Reason:

```text
Promotion recommendation reason:
```

## Example: Internal Research Manual Test

```yaml
manual_test_id: mt_internal_research_001
test_name: Internal Research Artifact Review And Signal Candidate Test
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
workspace_status: manual_test
workflow_id: wf_internal_research_packet_001
workflow_name: Internal Research Packet Workflow
test_date: 2026-05-24
test_operator: human_operator
test_status: planned
```

Goal:

```text
Validate that Internal Research can produce a research packet artifact, create a review item, record a human decision, draft a signal candidate, and preserve audit/provenance without external actions.
```

## Example: SearchClarity Future Manual Test

```yaml
manual_test_id: mt_searchclarity_report_001
test_name: SearchClarity Draft Report QA Flow
workspace_id: ws_searchclarity_future
workspace_name: SearchClarity
workspace_type: service
workspace_status: onboarding
workflow_id: wf_service_report_manual_test
workflow_name: Service Report Manual Test Workflow
test_date: TBD
test_operator: human_operator
test_status: planned
```

Goal:

```text
Validate that a SearchClarity-style report can move from intake summary to draft report artifact to QA review to delivery-ready decision without customer delivery automation or external live actions.
```

This example should not be run until SearchClarity business-readiness artifacts exist.

## Final Rule

```text
If it cannot pass manually, it has not earned automation.
```
