# 15 - Secrets And Credentials

## Purpose

This document defines Neon Ronin's boundary for secrets, credentials, tokens, keys, OAuth material, external account access, and credential references.

It exists to answer:

```text
What counts as a secret, where may it live, who may reference it, what must never enter docs/schemas/artifacts/logs, and how do future integrations use credentials without leaking them into core?
```

Neon Ronin is not ready to store or use real secrets until this boundary is implemented.

## Core Rule

```text
Secrets are never normal data.
```

Secrets must not be stored in core docs, workspace docs, schemas, artifacts, audit payloads, agent outputs, prompts, logs, review items, signal records, Observatory records, or examples.

Neon Ronin may reference a secret through a bounded credential reference.

Neon Ronin must not copy the secret value.

## What Counts As A Secret

Secrets include:

- API keys
- OAuth access tokens
- OAuth refresh tokens
- passwords
- private keys
- signing keys
- webhook signing secrets
- session cookies
- database passwords
- service account keys
- recovery codes
- personal access tokens
- provider tokens
- payment provider secrets
- SMTP credentials
- SSH keys
- encryption keys
- customer credentials
- marketplace account credentials
- any value that grants access, impersonation, spending, publishing, deletion, messaging, or data export

If exposing a value could grant access or cause harm, treat it as a secret.

## Credential Reference

A credential reference is a safe pointer to a secret managed outside normal Neon Ronin records.

A credential reference may contain:

- credential reference id
- provider name
- provider account label
- workspace scope
- allowed action classes
- creation timestamp
- expiration timestamp if known
- status
- required review gates
- audit references

A credential reference must not contain:

- raw secret value
- token value
- password
- private key material
- refresh token
- unredacted provider credential payload

Example safe reference:

```yaml
credential_reference_id: credref_example_provider_readonly_001
provider: example_service_provider
provider_account_label: future_service_workspace_readonly
workspace_id: ws_future_service_workspace_001
allowed_action_classes:
  - read
status: active
secret_value_stored_here: false
```

## Secret Ownership

Secrets are not core-owned business data.

Credential references may be core-owned or integration-owned governance records.

Secret values must live in a dedicated secrets mechanism later, such as:

- operating-system secret store
- encrypted local vault
- environment-specific secret manager
- cloud secret manager
- external provider-managed OAuth connection

The exact storage technology is deferred.

The boundary is not deferred.

## Forbidden Locations

Raw secret values must never appear in:

- `docs/`
- schema examples
- workspace docs
- adapter docs
- research docs
- artifacts
- review queue items
- audit record payloads
- signal records
- Observatory records
- agent outputs
- prompts
- source code comments
- test fixtures
- screenshots
- exported reports
- logs
- error messages
- git commits

If a secret appears in any of these places, treat it as a credential incident.

## Allowed Locations

A future implementation may store or access secrets only through approved secret storage.

Allowed patterns:

```text
credential reference -> secret store lookup -> scoped use -> audit event
```

Forbidden pattern:

```text
record field -> raw token -> agent/tool sees token -> logs/output may leak it
```

## Agent Rules

Agents must not receive raw secrets by default.

Agents may receive bounded capability through tools or integrations that hide the secret value.

Agents may reference:

- credential reference id
- provider name
- allowed action class
- whether credential exists
- whether credential is active/expired/revoked
- what review gate is required

Agents must not see:

- API key
- OAuth token
- refresh token
- password
- private key
- signing secret
- session cookie
- raw credential payload

Agents must not ask users to paste secrets into chat, docs, artifacts, prompts, or review items.

## Human Rules

Humans may authorize credential setup, revocation, rotation, or provider connection.

Human approval must be recorded for:

- adding credential reference
- connecting external account
- expanding credential scope
- enabling write capability
- enabling paid action capability
- rotating credential
- revoking credential
- deleting credential reference

Human approval does not mean the secret value becomes visible to agents or normal records.

## Workspace Scope Rules

Credentials must be scoped as narrowly as possible.

Default posture:

```text
one credential reference -> one provider -> one workspace -> least privilege
```

A credential for one workspace must not be reused by another workspace unless explicitly governed and audited.

Cross-workspace credential sharing is forbidden by default.

## Action Class Rules

Credential use must be tied to action classes.

Recommended posture:

| Action Class | Default Credential Posture |
|---|---|
| `read` | Allowed only if explicitly scoped |
| `analyze` | Usually does not need raw credential access |
| `draft` | Usually does not need raw credential access |
| `queue` | Does not need raw credential access |
| `external_draft` | Requires review and scoped integration |
| `live_write` | Human-approved only, strongly gated |
| `destructive` | Human-approved only, rare, strongly gated |

Credentials must not automatically allow external action.

A valid credential plus permission scope plus human decision may authorize a bounded action.

## External Integration Rules

External integrations must hide raw secret values from core records and agents.

An integration may use a credential reference to perform a bounded action.

Every meaningful credential-backed external action must preserve:

- workspace id
- credential reference id
- provider
- action class
- actor that requested the action
- review item id if required
- human decision id if required
- audit record id
- result status

External provider convenience does not override Neon Ronin review gates.

## OAuth Rules

OAuth is an integration mechanism, not a core shortcut.

OAuth connection records may reference:

- provider
- account label
- scopes granted
- workspace id
- connection status
- expiration/refresh metadata without token values
- audit records

OAuth connection records must not store raw access tokens or refresh tokens in normal records.

OAuth scope expansion requires human review and audit.

## Secrets And Audit

Audit records should record credential-related events without storing the secret value.

Audit records should capture:

- credential reference created
- credential reference activated
- credential reference scope changed
- credential reference paused
- credential reference revoked
- credential rotated
- credential-backed action requested
- credential-backed action approved
- credential-backed action rejected
- credential-backed action attempted
- credential-backed action failed
- credential incident detected

Audit records must not contain raw secrets.

## Secrets And Review Queue

Review queue items may request credential-related decisions.

Examples:

- approve connecting provider account
- approve credential scope expansion
- approve external write using credential reference
- approve credential revocation
- approve credential rotation

Review items must reference credential references, not secret values.

## Secrets And Permission Scopes

Permission scopes may allow actions involving credential references.

Permission scopes must not contain raw secrets.

A permission scope may contain:

- allowed credential reference ids
- allowed providers
- allowed action classes
- required review gates
- expiration
- denied actions

Permission scopes must not contain:

- API keys
- passwords
- OAuth tokens
- refresh tokens
- private keys

## Secrets And Artifacts

Artifacts must not contain raw secrets.

If a source artifact accidentally contains a secret, it must be treated as contaminated.

Contaminated artifacts should be:

1. blocked from review/delivery/publishing
2. removed from normal use where possible
3. replaced with a redacted version
4. audited as a credential incident
5. reviewed for credential rotation or revocation

## Secrets And Signals

Signals must never contain secrets.

Raw signals containing credentials must not become signal candidates.

Signal candidates containing credentials must be rejected or blocked.

Sanitized signals must not include secret values, credential identifiers that expose sensitive access, or provider account details that create risk.

The Observatory must never receive raw secrets.

## Secrets And Logs

Logs must not contain raw secrets.

If future tooling captures request/response metadata, it must redact:

- authorization headers
- cookies
- tokens
- passwords
- API keys
- OAuth refresh tokens
- signed URLs when sensitive
- provider secret payload fields

Error messages should use safe summaries.

Bad:

```text
Provider rejected token sk_live_abc123...
```

Good:

```text
Provider rejected credential reference credref_payment_001 with authentication_failed.
```

## Secret Redaction Rules

Future implementation should redact known secret shapes before writing logs, audit summaries, review items, or artifacts.

Redaction output should preserve usefulness without exposing values.

Example:

```text
redacted_secret(type=api_key, provider=unknown, last4=1234)
```

Never rely only on redaction as the safety model.

The primary rule is not to put secrets in normal records at all.

## Credential Lifecycle

Canonical credential reference statuses:

```text
planned
active
paused
expired
revoked
rotated
retired
incident_locked
unknown
```

Status meanings:

| Status | Meaning |
|---|---|
| `planned` | Reference planned but no usable credential is connected |
| `active` | Credential reference may be used within scope |
| `paused` | Credential exists but must not be used for new work |
| `expired` | Credential is no longer valid due to time/provider state |
| `revoked` | Credential has been explicitly revoked |
| `rotated` | Credential was replaced by a newer credential |
| `retired` | Credential reference closed for history |
| `incident_locked` | Credential is blocked due to suspected exposure or misuse |
| `unknown` | State has not been confirmed |

## Credential Incident

A credential incident occurs when a secret is:

- committed to git
- written to docs
- exposed to an agent output
- included in an artifact
- included in a signal
- included in an audit payload
- included in logs
- sent to the wrong provider/tool
- scoped too broadly
- used without approval
- suspected compromised

Credential incidents should trigger:

1. emergency stop if risk is active
2. credential lock or revocation where possible
3. rotation where appropriate
4. audit record
5. review item
6. contaminated artifact/log cleanup where possible
7. post-incident note or ADR if architecture must change

## Examples Of Forbidden Schema Fields

Do not add fields like:

```text
api_key
access_token
refresh_token
password
secret
private_key
oauth_token
provider_token
session_cookie
webhook_secret
etsy_access_token
fiverr_password
printify_api_key
```

Use credential references instead.

## Example Credential Reference Record

```yaml
credential_reference_id: credref_future_service_provider_readonly_001
provider: example_service_provider
provider_account_label: future_service_workspace
workspace_id: ws_future_service_workspace_001
status: planned
allowed_action_classes:
  - read
required_review_gates:
  - credential_permission_gate
  - data_privacy_gate
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
secret_value_stored_here: false
audit_record_ids:
  - audit_credential_reference_created_001
```

This is only a reference pattern.

It is not permission to implement service-platform automation.

Service-platform automation remains deferred.

## Deferred Implementation

This document does not choose:

- local vault technology
- cloud secret manager
- encryption implementation
- OAuth library
- token refresh mechanism
- credential UI
- multi-user secret-sharing model

Those decisions come later.

This document defines the non-negotiable boundary before those decisions are made.

## Relationship To Other Docs

This document depends on:

- `docs/core/07-permissions-and-audit.md`
- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/14-schema-authority.md`
- `docs/core/schemas/permission-scope.schema.md`
- `docs/core/schemas/human-decision.schema.md`
- `docs/core/schemas/audit-record.schema.md`

This document informs:

- `docs/core/18-external-integration-contract.md`
- future integration schemas
- future runtime implementation
- future operations runbooks
- future emergency stop procedure

## Final Rule

```text
Reference secrets. Never normalize them.
```
