# Internal Research Workspace Adapter

## Purpose

This adapter defines the generic pattern for an internal research or laboratory workspace.

It should not depend on any external business brand, customer, marketplace, or publishing channel.

## Typical Needs

- market observation
- hypothesis tracking
- experiment planning
- signal analysis
- strategy scoring
- research queue management
- Observatory feedback

## Typical Agents

| Agent | Role |
|---|---|
| Research Agent | Collects and organizes approved research inputs |
| Pattern Analysis Agent | Identifies recurring themes or anomalies |
| Scoring Agent | Applies scoring logic to opportunities or findings |
| Queue Agent | Routes findings into review or research queues |
| QA Agent | Checks consistency and evidence quality |
| Signal Capture Agent | Submits generalized signals to the Observatory |

## Generic Workflow

```text
Human defines research goal
-> Workspace gathers approved inputs
-> Research and scoring occur
-> Findings are organized into review packets
-> Human reviews conclusions
-> Approved generalized signals enter the Observatory
-> Research history and audit logs are stored
```

## Review Gates

- quality gate
- strategy review gate
- signal sanitization gate

## Rule

```text
Internal research workspace agents may analyze and organize.
They may not trigger external actions without human approval.
```
