# Internal Research Persistence Proof 001 Evidence

## Status

```text
passed
```

This evidence record closes the first local SQLite-backed persistence proof.

It records the result of the approved implementation-start decision for `workspace_config_create` and audit-first persistence behavior.

## Evidence Metadata

```yaml
proof_evidence_id: evidence_internal_research_persistence_001
implementation_start_decision_id: decision_internal_research_implementation_start_persistence_001
implementation_plan_id: impl_plan_internal_research_persistence_001
first_proof_parameter_record_id: first_proof_params_internal_research_persistence_001
workspace_id: ws_internal_research_001
proof_status: passed
created_at: 2026-05-26T00:00:00Z
updated_at: 2026-05-26T00:00:00Z
schema_version: persistence_proof_evidence_v1
record_revision: 1
```

## Proof Implemented

Implemented files:

```text
packages/neon-core/src/neon_ronin_core/persistence/sqlite_store.py
fixtures/internal-research/workspace_config_fixture.py
packages/neon-core/tests/test_workspace_config_create.py
```

The implementation remains inside the approved areas:

```text
packages/neon-core/
fixtures/internal-research/
```

No desktop app, local service, UI, agent runtime, integration, scheduled job, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation was added.

## Invariant Proven

```text
no audit record means no workspace config record
```

## Hammer Executed

```text
python -m unittest discover -s packages/neon-core/tests -v
```

Result:

```text
Ran 10 tests
OK
```

## Hammer Coverage

| Check | Result |
|---|---|
| valid workspace config creation creates exactly one workspace config and one audit record | passed |
| forced audit creation failure blocks or rolls back workspace config creation | passed |
| no partial workspace config remains after forced audit failure | passed |
| caller cannot forge system-owned fields | passed |
| unknown fields are rejected | passed |
| forbidden fields such as unbounded `metadata` or `custom_data` are rejected | passed |
| timestamps are UTC ISO 8601 with `Z` suffix | passed |
| `schema_version` and `record_revision` are present and correctly owned | passed |
| result is deterministic and not mock-only | passed |
| duplicate workspace id does not create a second audit record | passed |
| missing required fields are rejected before persistence | passed |
| non-empty `allowed_agents` is rejected for the first proof | passed |
| non-empty `external_references` is rejected for the first proof | passed |
| scheduled or watch runtime flags are rejected for the first proof | passed |

## Implementation Notes

- SQLite is used through Python stdlib `sqlite3`.
- The proof uses direct module/service calls only.`n- Expanded hammer coverage now includes duplicate-create, required-field, runtime, agent, and external-reference guard checks.
- The schema has only the two approved tables: `workspace_configs` and `audit_records`.
- The audit failure strategy is injectable audit write failure.
- Failed-attempt audit logging remains deferred.
- Human-decision persistence remains out of scope.

## Scope Confirmed Not Added

Still absent:

- `apps/desktop` implementation
- `services/local` implementation
- Tauri config
- frontend code
- HTTP API
- CLI contract
- MCP tool surface
- agent runtime
- integrations
- scheduled jobs
- watch mode
- live Observatory ingestion
- customer-facing workspace onboarding
- SearchClarity onboarding
- automation

## Next Recommended Step

Do not expand into agents, UI, integrations, or customer-facing workspace work.

Recommended next implementation step:

```text
Add a tiny developer hammer runner or test command wrapper so the first proof can be rerun consistently without manual PYTHONPATH setup.
```

Alternative next step:

```text
Pause and audit the first implementation slice before adding any new code.
```
