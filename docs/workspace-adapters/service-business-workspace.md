# Service Business Workspace Adapter

## Purpose

This adapter defines the generic pattern for a service business workspace.

It should not name a specific business.

## Typical Needs

- customer intake
- customer/order history
- research workflow
- deliverable drafting
- QA review
- delivery prep
- customer-safe file storage
- raw signal capture
- signal sanitization

## Typical Agents

| Agent | Role |
|---|---|
| Intake Agent | Normalizes customer inputs |
| Research Agent | Gathers required research/context |
| Drafting Agent | Drafts customer-facing deliverables |
| QA Agent | Checks completeness, tone, quality, and claims |
| Delivery Prep Agent | Packages approved deliverables |
| Signal Capture Agent | Extracts sanitized reusable signals |

## Generic Workflow

```text
Customer request received
-> Intake Agent normalizes request
-> Research Agent gathers context
-> Drafting Agent creates deliverable draft
-> QA Agent reviews draft
-> Human approves final deliverable
-> Delivery Prep Agent prepares output
-> Workspace history saved
-> Sanitized signals submitted to Observatory
```

## Review Gates

- customer delivery gate
- data privacy gate
- quality gate
- signal sanitization gate

## Rule

```text
Service business agents may draft and prepare.
They may not deliver customer-facing outputs without human approval.
```
