# 18 - External Integration Contract

## Purpose

This document defines Neon Ronin's contract for external integrations.

An external integration connects Neon Ronin to an outside system, provider, API, marketplace, file store, communication platform, payment provider, LLM provider, or other external service.

It exists to answer:

```text
What may an external integration do, what must gate it, what records must it create, what must it never own, and how does Neon Ronin prevent providers from defining core platform behavior?
```

External integrations are powerful and dangerous.

They must remain subordinate to Neon Ronin's workspace, lifecycle, runtime, permission, review, audit, secrets, and failure-handling rules.

## Core Rule

```text
External integrations obey Neon Ronin boundaries.
External providers do not define Neon Ronin authority.
```

An external API may permit an action.

Neon Ronin may still forbid it.

## Scope

This contract applies to integrations such as:

- marketplace APIs
- service-platform APIs
- print-on-demand providers
- payment providers
- file stores
- email/SMS/messaging systems
- LLM providers
- analytics/research tools
- webhooks
- OAuth providers
- browser/automation tools
- future plugin systems

This contract does not promote any specific integration.

Etsy, Printify, Fiverr automation, marketplace publishing, cloud sync, plugin marketplaces, scheduled agents, and watch mode remain deferred unless promoted by roadmap/ADR.

## Integration Ownership

External integration records are usually:

```text
Integration-owned records or referenced-only data
```

Core may own generic integration governance concepts, such as:

- external reference pattern
- credential reference pattern
- permission/review/audit requirements
- provider capability declarations
- integration status

Core must not own provider-specific payload shape as generic platform truth.

## External Reference Pattern

Use external references instead of provider-specific fields in core records.

Bad core pattern:

```yaml
workspace:
  etsy_shop_id: abc123
  printify_product_id: prod_456
```

Better generic pattern:

```yaml
external_reference:
  external_reference_id: extref_001
  provider: etsy
  resource_type: shop
  provider_resource_id: abc123
  workspace_id: ws_001
```

Provider-specific detail may exist later in integration-specific contracts.

It must not leak into generic core schemas.

## Integration Action Classes

External integrations must declare allowed action classes.

Canonical action classes:

```text
read
analyze
draft
queue
external_draft
live_write
destructive
```

Default posture:

| Action Class | Default Integration Posture |
|---|---|
| `read` | allowed only if credential/reference/permission scope allows |
| `analyze` | internal analysis only; no external mutation |
| `draft` | internal draft only |
| `queue` | may queue review item if allowed |
| `external_draft` | requires explicit integration permission and review posture |
| `live_write` | human-approved only, strongly gated |
| `destructive` | human-approved only, rare, strongly gated |

An integration must not perform an action class that is not explicitly allowed.

## Integration Statuses

Canonical integration statuses:

```text
planned
draft
manual_test
active
paused
deprecated
retired
incident_locked
```

Status meanings:

| Status | Meaning |
|---|---|
| `planned` | Integration is conceptual only |
| `draft` | Integration contract/config is being defined; no live use |
| `manual_test` | Limited human-started testing only |
| `active` | May operate within configured limits |
| `paused` | New integration actions are blocked |
| `deprecated` | Should not be used for new workflows |
| `retired` | Closed for new use and preserved for history |
| `incident_locked` | Blocked due to security, credential, privacy, or external-action incident |

## Required Integration Metadata

Any future integration config should define:

- provider name
- integration purpose
- workspace scope
- integration status
- allowed action classes
- allowed resource types
- required credential references
- required permission scopes
- required review gates
- audit requirements
- failure behavior
- provider capability limits
- rate limit posture if known
- data import/export boundaries
- forbidden actions
- non-goals

If these are unclear, the integration is not ready.

## Provider Capability Declaration

An integration should declare what the provider can do separately from what Neon Ronin allows.

Example:

```yaml
provider_capabilities:
  can_read_listings: true
  can_create_drafts: true
  can_publish: true
  can_delete: true
neon_ronin_allowed_actions:
  - read
  - external_draft
forbidden_actions:
  - autonomous_publishing
  - autonomous_deletion
```

Provider capability is not permission.

## Credential Boundary

Integrations must use credential references.

They must not store raw secrets in normal records.

External integrations must follow `docs/core/15-secrets-and-credentials.md`.

Integration records may reference:

- credential reference id
- provider
- account label
- scope labels
- status
- audit records

Integration records must not store:

- API keys
- OAuth access tokens
- OAuth refresh tokens
- passwords
- private keys
- webhook signing secrets
- provider tokens
- session cookies

## Permission Boundary

Integrations must use permission scopes.

A valid credential is not enough.

A valid integration config is not enough.

A valid provider API response is not enough.

Before meaningful external action, Neon Ronin must confirm:

1. workspace lifecycle allows it
2. runtime mode allows it
3. integration status allows it
4. permission scope allows it
5. credential reference is valid and scoped
6. review gate requirements are satisfied
7. human decision exists if required
8. hard-no rules are not violated
9. audit logging is available

If any check fails, block the action and audit when meaningful.

## Review Gate Boundary

External integrations must preserve review gates.

Human review is required for:

- publishing
- customer messaging
- customer delivery
- spending
- refunds/payments
- destructive actions
- credential changes
- permission changes
- public-facing edits
- marketplace/account changes
- privacy-sensitive exports
- rights/IP/compliance-sensitive actions

An integration must not turn a review queue item into an executed action by existing.

A human decision may authorize a bounded external action.

It does not create broad permanent provider authority.

## Workspace Boundary

Integration use must be workspace-scoped.

A workspace integration must not access another workspace's private data, credentials, artifacts, customers, or provider resources.

Cross-workspace integration sharing is forbidden by default.

If a future shared integration exists, it must be explicitly governed by ADR and permission scopes.

## Runtime Boundary

Integration actions must obey runtime mode.

Rules:

- `off` blocks new integration actions
- `on_demand` allows only human-started integration actions if configured
- `scheduled` remains deferred unless promoted
- `watch_mode` remains deferred unless promoted
- `paused` blocks new integration actions
- `emergency_stop` blocks new integration actions and should stop active ones where possible

Manual-test workspaces may not use scheduled or watch-mode integration behavior.

## Lifecycle Boundary

Integration actions must obey workspace lifecycle.

Examples:

- `idea` workspaces cannot use integrations
- `onboarding` workspaces may plan integration needs but cannot execute external writes
- `manual_test` workspaces may use limited human-started read/draft tests only if configured
- `active` workspaces may use approved integration modes
- `paused` workspaces cannot start new integration actions
- `retired` workspaces cannot start new integration actions

## External Read Rules

External reads may be lower risk than writes, but they are not automatically safe.

External reads must still obey:

- credential scope
- provider terms
- workspace scope
- permission scope
- data privacy boundaries
- audit requirements where meaningful

External reads may bring private/provider data into Neon Ronin.

Imported data must be classified before storage.

## External Draft Rules

External drafts are not live external actions, but they still interact with outside systems.

External drafts require:

- integration permission
- credential reference
- workspace scope
- review posture
- audit record
- external reference

An external draft must not be treated as published, delivered, or customer-approved.

## Live Write Rules

Live writes change public, customer-facing, marketplace-visible, or external state.

Live writes require:

- human decision
- review queue item
- permission scope
- credential reference
- integration status allowing the action
- workspace lifecycle allowing the action
- runtime mode allowing the action
- audit logging

No autonomous live writes in early Neon Ronin.

## Destructive Action Rules

Destructive actions include deleting, cancelling, refunding, revoking, removing, overwriting, disabling, or otherwise damaging state.

Destructive actions require strict human review and should be rare.

Destructive actions must preserve:

- target external reference
- human decision id
- review item id
- reason
- audit record id
- provider response status summary

Autonomous destructive actions are forbidden.

## External Payload Rules

External payloads must not become core semantic truth.

Provider request/response payloads may be stored only if:

- allowed by future integration-specific contract
- bounded
- redacted
- provider-specific
- not treated as generic core truth
- not containing secrets
- not containing raw private customer data unless workspace-owned and allowed

Core records should prefer external references, summaries, and audit records.

## Imported Data Rules

Data imported from an external system must be classified before durable storage.

Classify imported data as:

- workspace-owned data
- integration-owned record
- referenced-only data
- core-owned metadata
- Observatory-eligible only after sanitization
- forbidden-in-core data

Imported data must not be dumped into core as generic JSON.

## Webhook Rules

Webhooks are external events and must be treated carefully.

Webhook handling must:

- verify authenticity using secret mechanisms later
- avoid storing raw signing secrets
- classify event payloads
- preserve external reference ids
- create audit records for meaningful events
- avoid direct external action without review
- obey workspace scope
- handle duplicate events safely

Webhook receipt is not permission to act.

## Rate Limit And Quota Rules

Integration configs should record rate limit posture when known.

Rate limit failures should follow `docs/core/16-error-and-failure-handling.md`.

Rate limits must not cause uncontrolled retry loops.

Automatic retry remains deferred unless governed.

## Idempotency Rules

External actions should be designed to avoid duplicate harmful effects.

Where provider supports idempotency keys, future implementation should use them for consequential actions.

Unknown external outcomes must not be retried automatically.

If outcome is unknown:

1. audit it
2. create/update review item
3. reconcile provider state if possible
4. require human decision before retry

## External Error Rules

Integration failures must produce safe summaries.

They must not expose:

- tokens
- credentials
- authorization headers
- cookies
- full customer payloads
- full provider responses
- private artifact contents

Safe external error summaries may include:

- provider
- external reference id
- action class
- safe provider error code
- result status
- retry eligibility
- next required action

## Audit Requirements

External integration events that should be audited include:

- integration config created
- integration config updated
- integration status changed
- credential reference linked/unlinked
- permission scope changed
- external read attempted
- external draft attempted
- external write requested
- external write approved
- external write attempted
- external write failed
- external outcome unknown
- destructive action requested
- destructive action approved
- destructive action attempted
- webhook received
- provider error received
- rate limit encountered
- integration paused
- integration incident locked

Audit records should reference external references and safe summaries, not raw payloads.

## Failure Handling

External integration failures must follow `docs/core/16-error-and-failure-handling.md`.

Important external failure states:

```text
failed
blocked
unknown
cancelled
expired
incident_locked
```

A blocked external action often means Neon Ronin protected the platform correctly.

Do not treat blocked as success.

Do not treat unknown as failure or success without reconciliation.

## Incident Rules

Integration incidents include:

- credential exposure
- unauthorized provider access
- provider action executed without review
- duplicate live write
- customer/private data leaked externally
- provider account compromised
- webhook authenticity failure
- destructive action mistake
- external outcome unknown for consequential action

Incidents may require:

- emergency stop
- integration pause
- credential revocation/rotation
- audit records
- review item
- contaminated artifact/log cleanup
- ADR or contract update

## Data Export Rules

Exporting data to external systems is an external action.

Exports must obey:

- workspace scope
- customer privacy
- permission scope
- review gates
- credential scope
- audit requirements
- sanitization if Observatory-derived data is involved

Private workspace data must not be exported to another workspace or public provider by accident.

## LLM Provider Rules

LLM providers are external integrations.

Sending data to an LLM provider is an external data transfer.

LLM provider use must obey:

- workspace privacy rules
- data minimization
- credential reference rules
- audit requirements where meaningful
- no raw credentials in prompts
- no unnecessary customer/private data in prompts
- no raw private Observatory source details in prompts

LLM output is derived unless promoted through review/schema/ADR path.

## Future Service Workspace Boundary Example

A future service workspace may eventually need integrations with service platforms, research tools, file export pipelines, or marketplace-related references.

Those integrations must remain workspace-scoped.

Specific-business integration needs must not become Neon Ronin core fields.

Examples:

```text
Service-platform profile copy -> workspace-owned artifact
Service-platform automation -> deferred integration domain
Marketplace shop/listing references -> external references or workspace-owned input
PDF export pipeline -> artifact/workflow capability, not customer delivery automation
```

A future workspace may inform integration requirements.

A future workspace must not define core integration authority.

## Forbidden Integration Patterns

Do not allow:

- provider-specific fields in generic core schemas
- raw credentials in integration records
- external writes without review
- autonomous customer messaging
- autonomous publishing
- autonomous spending
- autonomous destructive actions
- workspace-private data exported across workspace boundaries
- raw signals submitted to Observatory through integration shortcuts
- provider payload JSON used as core semantic truth
- integration status overriding emergency stop
- provider capability treated as Neon Ronin permission

## Conceptual Integration Config Shape

This is a conceptual shape, not a final schema.

```yaml
integration_id: integ_future_service_provider_readonly
provider: example_service_provider
integration_status: planned
workspace_id: ws_future_service_workspace_001
purpose: Future service-platform reference or read-only integration planning.
allowed_action_classes:
  - read
required_credential_references:
  - credref_future_service_provider_readonly_001
required_permission_scopes:
  - perm_future_service_provider_readonly_001
required_review_gates:
  - credential_permission_gate
  - data_privacy_gate
forbidden_actions:
  - autonomous_customer_messaging
  - autonomous_publishing
  - autonomous_spending
  - autonomous_destructive_actions
provider_capabilities:
  can_read_orders: true
  can_message_customers: true
neon_ronin_allowed_actions:
  - read
external_references:
  - extref_example_service_account_001
audit_requirements:
  - integration_config_created
  - external_read_attempted
  - provider_error_received
failure_behavior:
  on_permission_denied: block_and_audit
  on_unknown_external_outcome: require_human_review
  on_credential_failure: block_and_review
```

This example does not promote service-platform automation.

## Promotion Requirements

A deferred integration domain may be promoted only when:

1. roadmap phase allows it
2. ownership is clear
3. credential boundary is clear
4. permission scope is clear
5. review gates are clear
6. audit events are clear
7. failure behavior is clear
8. provider-specific records are isolated
9. workspace privacy is protected
10. human approval gates are preserved
11. an ADR is created if the integration changes platform authority

## Relationship To Other Docs

This document depends on:

- `docs/core/07-permissions-and-audit.md`
- `docs/core/09-workspace-lifecycle.md`
- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/14-schema-authority.md`
- `docs/core/15-secrets-and-credentials.md`
- `docs/core/16-error-and-failure-handling.md`
- `docs/core/schemas/permission-scope.schema.md`
- `docs/core/schemas/human-decision.schema.md`
- `docs/core/schemas/audit-record.schema.md`

This document informs:

- future integration schemas
- future external reference schema
- future credential implementation
- future provider-specific adapters
- future operations runbooks
- future emergency stop procedure

## Non-Goals

This document does not define:

- any provider-specific API contract
- OAuth implementation
- webhook implementation
- marketplace publishing implementation
- Tauri UI integration
- cloud sync
- plugin marketplace
- scheduler/watch implementation
- database tables
- specific provider rate-limit policies

## Final Rule

```text
Integrations may extend Neon Ronin's reach, but never its authority.
```
