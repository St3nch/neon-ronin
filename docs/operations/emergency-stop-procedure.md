# Emergency Stop Procedure

## Purpose

This procedure defines how Neon Ronin stops work when safety, privacy, credentials, external actions, workspace boundaries, or platform trust may be at risk.

Emergency stop exists so Neon Ronin can fail safe instead of continuing risky work because a workflow, agent, integration, or human process was already in motion.

## Core Rule

```text
Emergency stop overrides normal operation.
```

When emergency stop is active, Neon Ronin must block new consequential work and stop or contain active work where possible.

## When To Use Emergency Stop

Use emergency stop when there is active or suspected risk involving:

- credential exposure
- raw secret in docs, artifacts, logs, prompts, or records
- unauthorized external action
- unknown external action outcome for consequential work
- customer/private data leakage
- raw workspace data sent to Observatory
- autonomous publishing attempt
- autonomous customer messaging or delivery attempt
- autonomous spending attempt
- destructive action attempt
- runaway agent/workflow behavior
- permission boundary bypass
- workspace-private data crossing boundaries
- provider account compromise
- unsafe integration behavior
- audit logging failure during consequential action
- schema/core corruption that affects safety controls

If uncertain, pause first and investigate.

## Emergency Stop Levels

Use the narrowest level that safely contains the issue.

| Level | Name | Meaning |
|---|---|---|
| 1 | Workspace stop | Stop one workspace |
| 2 | Integration stop | Stop one integration/provider path |
| 3 | Agent stop | Stop one agent or agent class |
| 4 | Observatory stop | Stop Observatory intake/query path |
| 5 | Platform stop | Stop all new Neon Ronin work |

Escalate if containment is unclear.

## Immediate Actions

When emergency stop is triggered:

1. Identify the stop level.
2. Stop new work at that level.
3. Stop or pause active runs where possible.
4. Block external writes and destructive actions.
5. Block credential-backed actions.
6. Block Observatory submissions if signal/privacy risk is involved.
7. Preserve audit trail.
8. Create or update review item.
9. Record human decision or operator note.
10. Begin triage.

Do not delete evidence during the initial stop.

## Required Emergency Stop Record

Create a record or note with:

```yaml
emergency_stop_id:
triggered_at:
triggered_by_actor_id:
stop_level: workspace | integration | agent | observatory | platform
affected_workspace_ids:
affected_agent_ids:
affected_integration_ids:
affected_records:
reason:
initial_risk_category:
status: active | contained | resolved | false_alarm
review_item_id:
human_decision_id:
audit_record_ids:
```

This is an operational record shape, not a final schema.

## Statuses

Canonical emergency stop statuses:

```text
active
contained
investigating
resolved
false_alarm
superseded
```

Meanings:

| Status | Meaning |
|---|---|
| `active` | Stop is currently blocking work |
| `contained` | Immediate risk is contained but investigation continues |
| `investigating` | Human review is analyzing cause and scope |
| `resolved` | Human decision allows stop to lift |
| `false_alarm` | Stop was triggered but no issue was found |
| `superseded` | Another stop/incident record replaced this one |

## Workspace Stop

Use when risk is contained to one workspace.

Actions:

- [ ] Set workspace runtime to paused/emergency stop posture.
- [ ] Block new agent runs.
- [ ] Block new workflows.
- [ ] Block new review items except incident/recovery reviews.
- [ ] Block new external actions.
- [ ] Block new Observatory submissions.
- [ ] Preserve existing artifacts and records.
- [ ] Triage open review items.
- [ ] Create audit record.
- [ ] Create human decision/review item.

## Integration Stop

Use when risk involves a provider, credential, OAuth connection, webhook, export path, or external API.

Actions:

- [ ] Pause or incident-lock the integration.
- [ ] Block credential-backed actions.
- [ ] Block external writes.
- [ ] Block destructive actions.
- [ ] Preserve external references.
- [ ] Check credential exposure risk.
- [ ] Rotate/revoke credentials if needed.
- [ ] Record provider state if safe.
- [ ] Create audit record.
- [ ] Create review item.

Do not retry unknown external outcomes automatically.

## Agent Stop

Use when one agent or class of agents may be unsafe.

Actions:

- [ ] Pause agent definition or permission scope.
- [ ] Stop active agent runs where possible.
- [ ] Block new runs from affected agent.
- [ ] Review recent outputs.
- [ ] Check for private data, credentials, or external-action attempts.
- [ ] Audit blocked/stopped runs.
- [ ] Create review item for investigation.

No agent may resume itself.

## Observatory Stop

Use when the risk involves signal intake, sanitization, scoring, query leakage, or cross-workspace intelligence.

Actions:

- [ ] Block new Observatory submissions.
- [ ] Block signal normalization if affected.
- [ ] Block query outputs if leakage risk exists.
- [ ] Freeze affected derived intelligence outputs.
- [ ] Review source/sanitized signal boundaries.
- [ ] Audit affected signal/query records.
- [ ] Create review item.

Raw workspace data must not be allowed into Observatory during recovery.

## Platform Stop

Use when scope is unclear or safety controls may be compromised across Neon Ronin.

Actions:

- [ ] Block all new agent runs.
- [ ] Block all new workflows.
- [ ] Block all external actions.
- [ ] Block all credential-backed actions.
- [ ] Block all Observatory submissions.
- [ ] Pause integrations where practical.
- [ ] Preserve audit/artifact/review records.
- [ ] Create platform-level review item.
- [ ] Start incident triage.

Platform stop is serious. Use it when narrower containment is not trustworthy.

## Triage Checklist

During triage:

- [ ] What happened?
- [ ] Which workspace(s) are affected?
- [ ] Which agent/workflow/integration is affected?
- [ ] Was any external action attempted?
- [ ] Is external outcome known?
- [ ] Was any credential exposed?
- [ ] Was any customer/private data exposed?
- [ ] Did raw data enter Observatory?
- [ ] Did audit logging succeed?
- [ ] Which records/artifacts/logs are contaminated?
- [ ] What must remain blocked?
- [ ] What can safely resume?

## Credential Incident Actions

If credentials may be exposed:

- [ ] Stop affected integration/credential use.
- [ ] Incident-lock credential reference if possible.
- [ ] Revoke or rotate credential where appropriate.
- [ ] Search for contaminated docs/artifacts/logs/prompts where feasible.
- [ ] Replace contaminated artifacts with redacted versions where possible.
- [ ] Create audit record.
- [ ] Create review item.
- [ ] Follow `docs/core/15-secrets-and-credentials.md`.

Do not paste the exposed secret into the incident notes.

## External Unknown Outcome Actions

If external outcome is unknown:

- [ ] Do not retry automatically.
- [ ] Record unknown status.
- [ ] Preserve request/reference ids if safe.
- [ ] Check provider state if safe.
- [ ] Create review item.
- [ ] Require human decision before retry.
- [ ] Audit the unknown outcome.

Unknown is not success.

Unknown is not safe to repeat blindly.

## Audit Requirements

Emergency stop events requiring audit:

- emergency stop triggered
- stop level changed
- workspace paused due to stop
- integration paused/incident-locked
- agent paused/stopped
- Observatory intake blocked
- credential revoked/rotated
- external unknown outcome recorded
- contaminated artifact/log identified
- review item created
- human decision recorded
- stop resolved/lifted

Audit summaries must be safe and must not contain raw secrets or private payload dumps.

## Review Requirements

Emergency stop should create or update review items for:

- incident triage
- credential action
- workspace resume decision
- integration resume decision
- agent resume decision
- contaminated artifact cleanup
- external unknown outcome reconciliation
- schema/core corruption review

Review decisions must be human decisions.

## Lifting Emergency Stop

Do not lift emergency stop until:

- [ ] cause is understood or safely bounded
- [ ] affected scope is known
- [ ] credentials are safe or revoked/rotated
- [ ] external unknown outcomes are reconciled or blocked
- [ ] contaminated records are handled
- [ ] audit records exist
- [ ] review item is resolved
- [ ] human decision approves lifting stop
- [ ] remaining restrictions are documented

Lift narrowly where possible.

Example:

```text
Resume Internal Research on-demand artifact work.
Keep Observatory submissions blocked until signal review is complete.
```

## False Alarm Handling

If emergency stop was a false alarm:

- [ ] Record why it was triggered.
- [ ] Record why no issue was found.
- [ ] Audit the false alarm resolution.
- [ ] Resume only through human decision.
- [ ] Update docs/runbooks if the false alarm revealed ambiguity.

False alarm is still useful evidence.

## SearchClarity Reminder

If SearchClarity later triggers emergency stop:

- customer data remains workspace-owned
- Fiverr/service-platform integration remains deferred unless promoted
- customer delivery automation is blocked by default
- public sample/consent issues should block public use
- raw market signals must not enter Observatory
- report artifacts may need privacy/credential review

## Final Rule

```text
When trust is uncertain, stop first and prove safe before resuming.
```
