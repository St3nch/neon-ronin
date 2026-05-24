# r07 — Managed Agent Runtime

## TL;DR

Neon Ronin should not treat "always-on agents" as uncontrolled background autonomy.

Instead, it should use a **managed agent runtime**:

> Agents can run in the background, but only within schedules, budgets, permissions, logs, and human-controlled modes.

The goal is not to create agents that wander forever. The goal is to create controlled research/drafting workers that operate when allowed, stop when told, and never perform marketplace-changing actions without approval.

Core principle:

> **Always-on capability. Human-controlled operation.**

Or, more Neon Ronin:

> **The agents patrol when scheduled. They do not wander.**

---

## 1. Why This Matters

Earlier research showed a tension:

- We want agents that can continuously help with research, drafting, monitoring, and opportunity discovery.
- But we do not want uncontrolled autonomy.
- We do not want auto-publishing.
- We do not want agents hammering APIs, burning tokens, generating junk, or quietly making marketplace changes.

The answer is not "always on" in the reckless sense.

The answer is:

```text
managed background work
+ explicit schedules
+ on/off controls
+ budget caps
+ task limits
+ human approval gates
```

This makes agent work useful without turning the system into a caffeinated raccoon with an API key.

---

## 2. Core Runtime Modes

Neon Ronin should support clear runtime modes.

| Mode | Meaning | Use Case |
|---|---|---|
| **Off** | No background agent work runs. | Full manual control, safe default. |
| **On-Demand** | Agents run only when the user clicks "Run." | Research a niche, generate ideas, draft listings. |
| **Scheduled** | Agents run on fixed schedules. | Daily keyword refresh, weekly opportunity scan. |
| **Watch Mode** | Agents monitor approved sources within strict limits. | Watch selected keywords, competitors, trends. |
| **Paused** | Existing state is saved, but no new work starts. | Stop work temporarily without losing context. |
| **Emergency Stop** | Kill active runs and block new ones. | Runaway task, cost spike, bad behavior. |

Default should be:

```text
Off or On-Demand
```

Scheduled/watch behavior should be opt-in.

---

## 3. What Agents May Do Autonomously

Agents can run unattended only for safe, reversible, non-marketplace-changing work.

Allowed autonomous work:

- pull approved keyword data
- refresh DataForSEO results
- monitor saved keywords
- summarize marketplace changes
- identify trend shifts
- generate product/service ideas
- draft listing copy
- draft design prompts
- summarize competitor patterns
- organize review packets
- detect stale review items
- prepare weekly opportunity summaries
- queue items for human review

The output of autonomous work should usually be:

```text
review queue item
research note
draft
recommendation
summary
```

Not:

```text
live marketplace action
```

---

## 4. What Agents Must Never Do Without Approval

Agents must not perform risky or irreversible actions without explicit human approval.

Blocked without approval:

- publish Etsy listings
- activate listings
- delete listings
- change live listing content
- change prices on live products
- change inventory on live products
- submit products to production
- send customer messages
- issue refunds
- cancel orders
- change shop settings
- change account settings
- change API credentials
- modify production partner settings
- make paid marketplace actions unless budget-approved

This should be enforced by design, not just by prompt instructions.

---

## 5. Action Classes

Actions should be classified by permission level.

| Class | Description | Autonomous? | Examples |
|---|---|---:|---|
| **Read** | Fetch or inspect data. | Yes, within limits. | Keyword lookups, trend checks, listing observations. |
| **Analyze** | Transform or summarize data. | Yes. | Opportunity scoring, competitor summaries. |
| **Draft** | Create internal text/assets. | Yes, within budgets. | Product ideas, listing drafts, prompt drafts. |
| **Queue** | Add something for human review. | Yes. | New idea packet, stale listing suggestion. |
| **External Draft** | Create a draft in an external system. | Gated early. | Printify draft product, Etsy draft listing. |
| **Live Write** | Change marketplace-visible state. | No, human approval required. | Publish, activate, edit live title, change price. |
| **Destructive** | Delete, cancel, refund, revoke, remove. | No, explicit approval required. | Delete listing, refund order, revoke token. |

Early versions should keep even **External Draft** actions gated until trust is proven.

---

## 6. Scheduling Model

Schedules should be explicit, visible, and editable by the human operator.

Example schedules:

```text
Daily 7:00 AM
→ Pull DataForSEO keyword trends for approved niches

Monday 9:00 AM
→ Generate 20 new product ideas from saved demand signals

Wednesday 9:00 AM
→ Refresh competitor snapshots for parked ideas

Friday 4:00 PM
→ Summarize weekly opportunities and stale review items
```

Each scheduled job should define:

- name
- purpose
- source permissions
- run frequency
- max runtime
- max spend
- max output items
- whether it can use LLMs
- whether it can generate images
- whether it can create external drafts
- who/what receives the output

---

## 7. Budget and Cost Controls

Every managed agent job should have budget limits.

Required controls:

| Control | Purpose |
|---|---|
| **Daily spend cap** | Prevent runaway API cost. |
| **Per-job spend cap** | Prevent one workflow from consuming the budget. |
| **Per-agent token cap** | Stop infinite reasoning loops. |
| **Data API request cap** | Prevent DataForSEO or similar overuse. |
| **Image generation cap** | Prevent expensive creative loops. |
| **Max runtime** | Stop stuck jobs. |
| **Max output count** | Prevent huge review queues. |
| **Cooldowns** | Avoid hammering APIs or marketplaces. |
| **Kill switch** | Stop everything immediately. |

Budget status should be visible in the app.

Example:

```text
Daily Budget: $10.00
Used Today: $2.17
Remaining: $7.83
Active Jobs: 1
Queued Review Items: 14
```

---

## 8. Source Permissions

Agents should not have free access to every source.

Each source should have permissions and limits.

| Source | Recommended Permission Model |
|---|---|
| **DataForSEO** | Allowed within budget and rate limits. |
| **Google Trends / SERP data** | Allowed through approved APIs. |
| **Pinterest Trends** | Allowed if official/approved access exists. |
| **TikTok Creative Center** | Manual or approved workflow only until terms are clear. |
| **Etsy Open API** | Highly restricted; read/write actions separated. |
| **Etsy Marketplace Insights** | Human/manual unless official automation is allowed. |
| **Etsy autocomplete scraping** | Avoid / block unless legal review approves. |
| **Reddit** | Avoid scraping; use commercial API or licensed vendors only. |
| **eRank / Sale Samurai / EverBee** | Manual/export/licensed only unless vendor permission exists. |
| **Printify** | Restricted; product creation/publish actions require gates. |

No source should be added to autonomous jobs without a permission profile.

---

## 9. Review Queue Output

Managed agents should produce review items, not final actions.

A review item should include:

- title
- type: idea, listing draft, design prompt, competitor note, trend alert, etc.
- source job
- source data
- reasoning summary
- proposed next action
- cost spent generating it
- created timestamp
- expiration/staleness date
- human decision field: approve, edit, reject, park
- human notes

Example:

```text
Review Item: Personalized retirement candle for nurses
Type: Product idea
Source Job: Monday Opportunity Scan
Evidence: DataForSEO + Etsy listing observation + Pinterest trend note
Suggested Next Step: Approve for design prompt drafting
Human Decision: Pending
```

---

## 10. Human Control Surface

The desktop app should expose simple controls.

Minimum controls:

- global agent system: on/off
- pause all
- emergency stop
- run selected job now
- enable/disable schedule
- edit schedule
- set daily budget
- set per-job budget
- view active jobs
- view completed jobs
- view failed jobs
- view cost log
- view queued review items
- clear or archive stale outputs

The human should always know:

```text
what is running
why it is running
what it can access
what it has spent
what it produced
what needs review
```

---

## 11. Desktop Lifecycle

For the initial desktop-first version, the safest behavior is:

```text
App open → scheduled/on-demand jobs may run
App closed → jobs pause by default
App reopened → jobs resume or ask for confirmation
```

Possible later modes:

| Mode | Description | Complexity |
|---|---|---:|
| **Tray Mode** | App keeps running in background after window closes. | Medium |
| **Local Daemon** | Separate background process runs schedules. | High |
| **Remote Scheduler** | Server/VPS runs research jobs and desktop app reviews output. | Medium-High |
| **Hybrid** | Local desktop review + optional remote research worker. | High |

Do not assume true 24/7 operation in the first version.

Start with:

```text
On-demand + scheduled while app is open
```

Then test whether more is actually needed.

---

## 12. Logging and Audit Trail

Every job run should be logged.

Logs should include:

- job name
- start time
- end time
- status: completed, failed, paused, killed
- mode: on-demand, scheduled, watch
- sources accessed
- API calls made
- LLM/model calls made
- estimated cost
- output count
- errors
- generated review items
- human actions taken later

This matters for:

- debugging
- cost control
- marketplace compliance
- repeatability
- trust
- understanding what agents are actually doing

The goal is to avoid mystery-agent behavior.

---

## 13. Failure Handling

Managed agents should fail safely.

Failure states:

| Failure | Safe Behavior |
|---|---|
| API rate limit | Stop job, log, retry later only if allowed. |
| Budget exceeded | Stop job immediately. |
| LLM/tool error | Save partial state, mark failed. |
| Suspicious output | Queue for review or reject internally. |
| Source permission conflict | Stop and ask human. |
| External API write attempted without approval | Block action and log violation. |
| Long-running loop | Kill after max runtime. |

No failure should cause an agent to improvise around restrictions.

---

## 14. Relationship to LangGraph / Hermes / OpenClaw / Custom Workers

This document does not decide which runtime framework to use.

Instead, it defines what any runtime must support.

### LangGraph

Useful for:

- stateful workflows
- human approval gates
- pause/resume
- durable workflow state
- structured review flows

Potential role:

```text
workflow orchestrator and approval engine
```

### Hermes / OpenClaw

Potentially useful for:

- background agent workers
- persistent research agents
- scheduled drafting tasks
- exploratory work

Potential role:

```text
worker layer, not final authority
```

### Custom Workers

Potentially useful for:

- scheduled jobs
- deterministic data pulls
- cost-controlled API workflows
- simple research tasks

Potential role:

```text
boring, reliable execution layer
```

Important:

No worker layer should bypass the managed runtime rules.

---

## 15. Open Questions

Research still needed:

1. Should scheduled work run only when the desktop app is open?
2. Is tray/background mode necessary?
3. Should there be a small remote scheduler for nightly research?
4. Should LangGraph own schedules, or should a separate scheduler invoke workflows?
5. Should Hermes/OpenClaw be used at all, or are custom workers enough?
6. How should job budgets be calculated and enforced?
7. What observability/logging tool should be used?
8. What should happen if a scheduled job creates too many review items?
9. Should low-risk jobs run automatically while high-risk jobs require manual start?
10. How should stale review items expire?

---

## 16. Recommended Next Research

The next research should focus on:

```text
r08 — First Channel Selection / Manual Validation Plan
```

Main question:

> Which first business channel should Neon Ronin manually test before building deeper automation?

Candidate channels:

- Etsy POD
- Etsy digital downloads
- Gumroad templates
- Creative Market templates
- Fiverr Etsy SEO services
- Fiverr creative services
- Shopify/direct
- TikTok Shop
- Amazon Merch
- Redbubble / Society6 / TeePublic
- Payhip / Lemon Squeezy / Stan / Beacons

The managed runtime can support any of these later. But first, the business workflow needs to prove it is worth automating.

---

## 17. Final Principle

```text
Agents can patrol.
Agents can scout.
Agents can draft.
Agents can queue.

Agents cannot decide the business.
Agents cannot approve themselves.
Agents cannot publish.
Agents cannot spend without limits.
Agents cannot wander.
```

Short version:

> **Neon Ronin is not an autonomous shop bot. It is a managed agent command center.**
