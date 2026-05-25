# 19 - Hammer Testing Doctrine

## Purpose

This document defines Neon Ronin's hammer testing doctrine.

Hammer testing is the future verification layer that proves Neon Ronin's declared invariants, boundaries, persistence assumptions, review gates, audit behavior, and failure behavior hold under real execution.

This doctrine exists before implementation so Neon Ronin does not grow a database, API, agent runtime, or integration layer without knowing what must eventually be tortured, verified, and refused.

## Schema Status

```text
Phase 5B planning doctrine
```

This is not executable test code.

This is not a test runner selection.

This is not a database implementation decision.

This is the doctrine that future hammer tests must follow.

## Core Rule

```text
Declared invariants must eventually be hammered, not merely trusted.
```

If Neon Ronin claims a boundary, lifecycle rule, permission rule, audit rule, review gate, or ownership rule, future implementation must be able to prove it under real execution.

## What Hammer Testing Is

Hammer testing is boundary-torture verification.

Hammer tests answer questions like:

- does workspace isolation actually hold?
- does raw workspace data actually fail to enter the Observatory?
- does review-gated work actually block without human decision?
- does a failed multi-write operation actually roll back?
- does read-only really mean read-only?
- does a denied permission leave the database clean?
- does a score remain decision support instead of action authority?
- does emergency stop actually block consequential work?

Hammer tests are proof attempts against Neon Ronin's laws.

## What Hammer Testing Is Not

Hammer testing is not:

- ordinary unit testing
- helper-function testing
- snapshot testing theater
- route smoke testing only
- happy-path demo validation
- mock-heavy confidence theater
- UI click-through testing alone
- a substitute for schema authority
- a substitute for human review
- a license to implement before doctrine is clear

A hammer test that mocks the boundary it claims to verify is not a hammer.

## Hammer Failure Meaning

```text
Hammer failure means the system is not safe for the claimed capability.
```

A hammer failure is not a minor CI annoyance.

It means a declared invariant failed under pressure.

Correct response:

1. stop
2. understand the invariant failure
3. fix behavior or correct doctrine if doctrine was wrong
4. rerun hammer verification
5. do not promote the capability until the hammer passes

Suppressing hammer failures to keep moving is a governance failure.

## Required Hammer Categories

Neon Ronin's future hammer suite must include at least these categories.

## 1. Persistence Hammer

Verifies database and storage assumptions under real execution.

Must eventually verify:

- migrations apply cleanly
- expected tables/columns/constraints exist
- required fields are enforced
- valid status transitions persist correctly
- invalid status transitions are rejected
- multi-write operations are atomic
- failed transactions roll back fully
- audit records are not written for rolled-back actions unless explicitly modeled as failed attempts
- read-only paths do not write hidden state
- timestamps and system-owned fields are controlled by the system

## 2. Contract Hammer

Verifies API/service/tool contracts match documented behavior.

Must eventually verify:

- valid requests return exact expected response shape
- invalid requests return exact documented error shape
- missing records produce safe not-found behavior
- list endpoints are deterministic
- filters/sorting/pagination behave as documented
- forbidden fields are rejected
- server-owned fields cannot be forged
- unknown fields are rejected where schema authority requires it
- zero-state behavior is explicit and stable

## 3. Boundary Hammer

Verifies ownership and system boundaries hold under pressure.

Must eventually verify:

- workspace-private data does not leak across workspaces
- workspace-specific business logic does not enter core records
- integration-owned provider details remain external references or integration records
- Observatory query surfaces do not expose private source details
- score outputs do not become approval/action authority
- raw signals do not enter Observatory tables
- credentials never appear in normal records
- external provider capability is not treated as Neon Ronin permission

## 4. Workspace Isolation Hammer

Verifies one workspace cannot read, write, infer, mutate, or receive private data from another workspace.

Must eventually verify:

- Workspace A private artifact is unavailable to Workspace B
- Workspace B cannot infer Workspace A record existence through descriptive errors
- cross-workspace mutation attempts fail without side effects
- cross-workspace references fail unless explicitly governed
- shared Observatory intelligence remains generalized and privacy-safe

Preferred posture for cross-workspace violation probes:

```text
return unavailable/not found without existence leakage
```

## 5. Observatory Boundary Hammer

Verifies Observatory intake, query, scoring, and derived intelligence boundaries.

Must eventually verify:

- raw signal submission is rejected
- signal candidate requires sanitization review
- sanitized signal requires human decision before intake
- rejected/parked signals do not enter Observatory
- score output includes provenance/confidence/data quality notes
- score output cannot trigger external action
- Observatory query does not expose raw source workspace data
- derived intelligence remains derived, not canonical workspace truth

## 6. Review Gate Hammer

Verifies review gates are real blockers.

Must eventually verify:

- customer-facing artifacts cannot become delivery-ready without review
- public publishing cannot occur without review
- paid actions cannot proceed without human decision
- destructive actions cannot proceed without human decision
- credential/permission changes cannot proceed without human decision
- agents cannot approve their own work
- review item creation is not approval
- human decision scope is bounded

## 7. Audit Hammer

Verifies meaningful actions leave durable trace.

Must eventually verify:

- state changes create audit records
- blocked consequential actions create audit records where required
- failed operations create safe audit summaries
- human decisions link to audit records
- audit records do not contain raw secrets or private payload dumps
- audit failure blocks consequential actions
- audit records are append-friendly and not silently rewritten

## 8. Permission Hammer

Verifies permissions are deny-first and subordinate to all other boundaries.

Must eventually verify:

- unlisted action classes are denied
- denied action classes win over allowed action classes
- permissions cannot bypass lifecycle
- permissions cannot bypass runtime mode
- permissions cannot bypass review gates
- permissions cannot bypass emergency stop
- permission denial leaves state clean
- agents cannot expand their own permissions

## 9. Agent Run Hammer

Verifies agent runs stay bounded.

Must eventually verify:

- agent run action classes are subset of agent definition and permission scope
- agent run cannot perform external write without review/human decision
- agent run cannot approve its own outputs
- agent run cannot submit raw data to Observatory
- blocked/failed/cancelled/expired/skipped runs are auditable
- agent run outputs remain references, not payload dumps
- agent run cannot forge system-owned fields

## 10. Artifact Ownership Hammer

Verifies artifacts are tracked without stealing ownership.

Must eventually verify:

- artifact metadata can be core-tracked
- artifact content remains workspace-owned unless explicitly public/generalized
- public-use flag requires consent or fictional/sample classification
- delivery-ready status requires review
- contaminated artifacts are blocked
- storage references do not contain credentials

## 11. Signal Sanitization Hammer

Verifies raw-to-sanitized signal flow.

Must eventually verify:

- raw signals remain workspace-owned
- signal candidates are distinct from accepted Observatory signals
- private/customer details are removed before intake
- missing provenance blocks signal candidate approval
- rejected candidate remains auditable but not ingested
- sanitized signal intake requires human decision and audit

## 12. Failure And Rollback Hammer

Verifies failure handling is explicit and safe.

Must eventually verify:

- mid-transaction failure rolls back all related writes
- partial state does not masquerade as success
- unknown external outcome blocks retry until review
- failed review does not promote artifact/signal/workflow
- audit logging failure blocks consequential action
- recovery creates correction/superseding records instead of rewriting history

## 13. Schema Drift Hammer

Verifies schemas do not casually mutate into data swamps.

Must eventually verify:

- unknown fields are rejected where required
- forbidden fields are rejected
- provider-specific fields do not appear in generic core records
- unbounded metadata is not used as semantic truth
- schema changes require ownership/purpose/provenance review
- deprecated/retired fields do not silently regain authority

## 14. External Integration Hammer

Verifies integrations remain subordinate to Neon Ronin authority.

Must eventually verify:

- provider capability does not equal permission
- credential references are used instead of secret values
- live writes require human decision
- destructive actions require human decision
- unknown provider outcome blocks retry
- imported data is classified before durable storage
- raw provider payload does not become core semantic truth

## 15. Emergency Stop Hammer

Verifies emergency stop actually stops meaningful work.

Must eventually verify:

- emergency stop blocks new agent runs
- emergency stop blocks new workflows
- emergency stop blocks external actions
- emergency stop blocks credential-backed actions
- emergency stop blocks Observatory intake if relevant
- emergency stop cannot be bypassed by permission scope
- lifting emergency stop requires human decision

## Real Execution Principle

Future hammer tests should use real execution surfaces wherever possible.

Preferred:

```text
API/service call -> real validation -> real persistence -> real response -> real audit check
```

Avoid:

```text
mock permission check -> fake repository -> assert true
```

Where real execution is not possible, the gap must be documented and not counted as full hammer coverage.

## Exact Assertion Principle

Hammer assertions must be precise.

Good assertions:

- exact status value
- exact error class
- exact allowed response fields
- exact absent private fields
- exact audit record count/relationship
- exact database cleanliness after failure
- exact deterministic ordering

Bad assertions:

- response is not empty
- status code is 2xx
- object exists somewhere
- no exception thrown
- seems fine

## Negative Path Principle

Every important valid path needs a corresponding invalid-path probe.

Example:

```text
Valid: sanitized signal with human approval enters Observatory.
Invalid: raw signal tries to enter Observatory and is blocked with no write.
```

Invalid-path tests are not extra.

They prove the boundary.

## No Fake Coverage Rule

A planned hammer module is not coverage.

A route smoke test is not hammer coverage.

A mocked check is not hammer coverage.

A happy-path-only test is not hammer coverage.

A coverage map entry is not coverage until it links to implemented checks or clearly says planned/manual/deferred.

## Coverage Map Rule

Neon Ronin should eventually maintain:

```text
docs/operations/hammer-coverage-map.md
```

The coverage map should connect:

```text
Invariant -> Hammer module -> Check(s) -> Status -> Gaps
```

Possible coverage statuses:

```text
planned
manual_only
implemented
blocked
deferred
retired
```

A stale coverage map is a false confidence claim.

## Future First Module Set

When Neon Ronin reaches implementation/DB readiness, first hammer modules should likely include:

1. `hammer-workspace-isolation`
2. `hammer-observatory-boundary`
3. `hammer-review-gates`
4. `hammer-audit-trail`
5. `hammer-agent-run-boundaries`
6. `hammer-signal-sanitization`
7. `hammer-artifact-ownership`
8. `hammer-permission-denial`
9. `hammer-emergency-stop`
10. `hammer-schema-drift`

These names are planning names, not implementation commitments.

## Future DB Reliability Probes

When a real database exists, the first DB hammer probes should include:

- workspace-scoped records require `workspace_id`
- cross-workspace private reads fail without existence leakage
- raw signal cannot be inserted into Observatory-owned records
- sanitized signal requires human decision before intake
- agent run cannot approve itself
- review approval creates human decision and audit trail
- multi-write workflow failure rolls back all writes
- audit logging failure blocks consequential write
- credential reference cannot contain secret value
- unknown external outcome cannot be retried automatically
- forbidden fields are rejected
- system-owned fields cannot be forged

## Database Posture Influence

Neon Ronin has not yet chosen a final database architecture.

This doctrine does not choose:

- PostgreSQL vs SQLite vs hybrid local-first
- single database vs multiple databases
- schema layout
- ORM/query library
- migration tool
- API framework

However, this doctrine does require future database design to support:

- strong ownership boundaries
- reliable transactions
- auditable state changes
- deterministic queries
- controlled migrations
- workspace isolation
- credential isolation
- rollback verification
- schema discipline

## JSON Discipline

JSON may be used only where justified.

Acceptable future uses may include:

- bounded provider payload storage inside integration-owned records
- controlled configuration payloads
- bounded metadata with documented allowed keys

Forbidden use:

```text
custom_data as hidden schema
metadata as unresolved modeling
provider payload as core truth
workspace-private data copied into generic JSON
```

No data swamp.

## Polymorphic Reference Caution

Neon Ronin schemas use many thin references, such as:

```text
record_type
record_id
relationship
```

Future implementation must not handle these references with scattered route-local guesswork.

If polymorphic references become implementation reality, Neon Ronin should use a central resolver that:

1. validates allowed record types
2. verifies target record exists
3. verifies workspace scope where applicable
4. avoids cross-workspace existence leakage
5. fails deterministically
6. is hammered directly

## API/Service Boundary Preference

Future implementation should strongly prefer governed API/service entry points over direct database access by agents, tools, UI, scripts, or operator surfaces.

Reason:

```text
One enforcement surface is hammerable.
Many direct database shortcuts are drift factories.
```

This is not yet a final implementation ADR, but it should be treated as the default planning posture.

## Relationship To Manual Testing

Manual tests come before hammer tests.

Manual testing answers:

```text
Can humans execute and inspect the workflow safely on paper/in docs?
```

Hammer testing later answers:

```text
Does the implemented system enforce the workflow truth under pressure?
```

Both are needed.

Manual proof does not replace hammer proof.

Hammer proof does not replace human review.

## Relationship To Concrete Workspace Scenarios

Concrete workspaces may later provide excellent hammer scenarios, such as:

- artifact ownership
- customer delivery review
- raw market signal capture
- sanitized signal handoff
- public sample and consent checks
- external service-platform boundaries

Specific-business details must not define hammer doctrine.

Hammer doctrine protects Neon Ronin generally.

Concrete workspaces later supply realistic scenarios.

## Relationship To VEDA Lessons

This doctrine borrows the discipline of the VEDA/Project V/V Forge hammer posture:

- invariants first
- real execution over mock theater
- exact contracts over vibes
- negative paths are required
- rollback must be forced and verified
- boundary violation probes are required
- coverage maps must stay honest
- hammer failure means unsafe capability

Neon Ronin adapts these lessons to its own workspace, Observatory, review, agent, artifact, and integration model.

## Anti-Drift Rules

Hammer doctrine must not drift.

Rules:

1. Do not add hammer checks that cannot trace to invariant, schema, contract, operation doc, or ADR.
2. Do not count planned checks as implemented coverage.
3. Do not allow workspace-specific scenarios to become core hammer doctrine without abstraction.
4. Do not allow provider-specific behavior to define generic integration hammers.
5. Do not allow happy-path-only modules.
6. Do not allow tests to mock away the boundary being verified.
7. Do not allow hammer coverage to outrun schema authority.
8. Do not allow stale coverage maps to claim safety.

## When To Add Hammer Coverage

Future hammer coverage must grow when:

- a new invariant is added
- a schema gains implementation authority
- a workflow becomes executable
- a workspace reaches active implementation
- an agent gains a new action class
- an integration is promoted
- an Observatory capability is implemented
- a bug violates a declared invariant
- an incident reveals an untested boundary
- a new DB migration changes persistence rules

## Non-Goals

This document does not define:

- test framework
- language/runtime
- CI setup
- database implementation
- API framework
- migration tool
- exact test fixtures
- seed data format
- executable hammer modules
- production deployment gate

Those come later.

## Relationship To Other Docs

This document depends on:

- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/14-schema-authority.md`
- `docs/core/16-error-and-failure-handling.md`
- `docs/core/18-external-integration-contract.md`
- `docs/core/20-transaction-boundaries.md`
- `docs/operations/manual-test-template.md`
- `docs/operations/schema-change-checklist.md`
- `docs/operations/emergency-stop-procedure.md`

This document informs:

- future DB posture docs
- future API/service design
- future migration doctrine
- future hammer readiness plan
- future hammer coverage map
- future implementation quality gates

## Final Rule

```text
Do not trust the boundary until the hammer has tried to break it.
```
