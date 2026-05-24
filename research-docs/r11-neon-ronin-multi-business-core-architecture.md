# r11 — Neon Ronin Multi-Business Core Architecture

## Purpose

This document defines Neon Ronin as a multi-business internal operating system.

SearchClarity is only one small business that Neon Ronin needs to manage. It is the first real workspace, not the whole system.

Neon Ronin must also support future small businesses, service offers, marketplace projects, digital product lines, and internal ventures. One likely future business is a T-shirt design business called Super T Shirts that sells on Etsy and uses Neon Ronin agents to research, draft, organize, review, and operate the business.

Core rule:

```text
Neon Ronin is the operating system.
Each small business is a workspace.
SearchClarity is one workspace.
Super T Shirts could be another workspace.
The Observatory is shared intelligence.
The human remains the final decision-maker.
```

---

## 1. Executive Verdict

The correct model is not:

```text
Neon Ronin = SearchClarity backend
```

The correct model is:

```text
Neon Ronin = internal multi-business command center
SearchClarity = first business workspace
Super T Shirts = possible future business workspace
Other future businesses = additional workspaces
Observatory = shared market intelligence layer
Data Core = shared system of record
Orchestrator = routes work across all workspaces
```

This distinction matters because SearchClarity should not distort the platform architecture.

SearchClarity sells SEO/GEO/visibility services.

Super T Shirts might sell T-shirt designs on Etsy.

A future KDP workspace might sell books.

A future Gumroad workspace might sell templates.

A future Fiverr workspace might sell productized services.

All of these businesses need different workflows, agents, outputs, quality gates, and marketplace rules. Neon Ronin should provide the shared operating layer that lets each workspace run without hardcoding the whole app around one business.

---

## 2. Neon Ronin Mental Model

Think of Neon Ronin as an agent office building.

```text
Neon Ronin HQ
│
├── SearchClarity Workspace
│   ├── Customer Intake Agent
│   ├── Keyword Research Agent
│   ├── Report Drafting Agent
│   ├── QA Agent
│   └── Signal Capture Agent
│
├── Super T Shirts Workspace
│   ├── Trend Research Agent
│   ├── Design Brief Agent
│   ├── IP Risk Packet Agent
│   ├── Listing Copy Agent
│   ├── Mockup Prep Agent
│   └── Publishing Prep Agent
│
├── Future KDP Workspace
│   ├── Niche Research Agent
│   ├── Outline Agent
│   ├── Content Draft Agent
│   ├── Cover Brief Agent
│   └── Publishing Prep Agent
│
└── Observatory Workspace
    ├── Signal Intake Agent
    ├── Keyword Cluster Agent
    ├── Trend Agent
    ├── Competitor Pattern Agent
    ├── Opportunity Scoring Agent
    └── Data Quality Agent
```

The building is Neon Ronin.

The businesses are departments.

The agents are workers.

The Observatory is the shared research and intelligence floor.

The human is the owner/operator and final approver.

---

## 3. Core Architecture

| Component | Role | Applies To |
|---|---|---|
| Orchestrator | Routes jobs, chooses workflows, assigns agents, enforces gates | All workspaces |
| Workspace Registry | Defines each small business workspace and its rules | All workspaces |
| Agents | Perform narrow tasks inside workflows | Workspace-specific and shared |
| Observatory | Shared market intelligence, signals, scoring, research queues | All workspaces |
| Data Core | Shared storage for jobs, outputs, signals, scores, reviews, logs | All workspaces |
| Strategy Layer | Converts scored signals into recommended actions | All workspaces |
| Human Review Gates | Blocks risky or public actions until approved | All workspaces |
| Audit Logs | Records what agents did, what data they used, and what humans approved | All workspaces |
| Permission System | Controls what agents can access and do | All workspaces |
| Runtime Manager | Controls schedules, budgets, modes, and kill switches | All workspaces |

---

## 4. Workspace Definition

A workspace is a business/project operating area inside Neon Ronin.

Each workspace should define:

- workspace name
- business purpose
- business type
- supported channels
- workflows
- agents
- inputs
- outputs
- data access permissions
- marketplace/platform rules
- Observatory query permissions
- signal feedback rules
- human approval gates
- storage rules
- audit requirements

Reusable schema:

```yaml
workspace_id: string
workspace_name: string
business_name: string
business_type: service | marketplace_store | digital_products | content | internal_research | other
purpose: string
channels:
  - etsy
  - fiverr
  - shopify
  - gumroad
  - pinterest
  - other

inputs:
  - name: string
    source: human | customer | marketplace | observatory | external_api | manual
    required: boolean

outputs:
  - name: string
    format: markdown | pdf | spreadsheet | image | listing_draft | research_packet | task
    public_facing: boolean
    requires_human_review: boolean

agents:
  - agent_name: string
    role: string
    allowed_actions:
      - read
      - analyze
      - draft
      - queue
    forbidden_actions:
      - publish_without_approval
      - spend_without_budget
      - use_unapproved_sources

workflows:
  - workflow_name: string
    trigger: string
    steps:
      - step_name: string
        agent: string
        review_required: boolean

observatory:
  can_query: true
  can_submit_signals: true
  allowed_query_types:
    - keyword_cluster
    - trend_profile
    - competitor_pattern
    - opportunity_score
    - prior_signal_check

human_review_gates:
  - idea_gate
  - ip_common_sense_gate
  - quality_gate
  - publish_gate
  - paid_action_gate

storage_rules:
  customer_data: workspace_private
  business_data: workspace_private
  generalized_signals: observatory_allowed_after_sanitization
  public_outputs: human_review_required
```

---

## 5. SearchClarity Workspace

SearchClarity is the first service-business workspace.

Purpose:

```text
Produce SEO/GEO/marketplace visibility services and reports for customers.
```

SearchClarity owns:

- customer intake
- customer orders
- paid reports
- report templates
- delivery workflow
- customer/report history
- raw market signal capture during paid work

SearchClarity does not own:

- Neon Ronin orchestration
- Observatory scoring
- cross-business strategy
- future workspace architecture
- opportunity queues for all businesses

Example SearchClarity workflow:

```text
Customer order received
→ Intake Agent normalizes request
→ Research Agent gathers marketplace/keyword context
→ Report Drafting Agent drafts customer deliverable
→ QA Agent reviews draft
→ Human approves final report
→ Report delivered
→ Signal Capture Agent submits sanitized raw signals to Observatory
→ Neon Ronin scores signals for future strategy
```

SearchClarity's key output to Neon Ronin:

```text
generalized raw market signals
```

Not customer secrets.

Not client-specific confidential strategy.

---

## 6. Super T Shirts Workspace

Super T Shirts is a possible future marketplace-store workspace.

Purpose:

```text
Create, review, list, and manage original T-shirt design ideas for Etsy or other marketplaces using Neon Ronin agents, with human approval before publishing.
```

Super T Shirts would own:

- brand direction
- product ideas
- T-shirt design concepts
- design briefs
- mockup drafts
- Etsy listing drafts
- product/listing status
- shop-specific records
- sales/order notes if integrated later

Neon Ronin would provide:

- agent orchestration
- trend research workflow
- Observatory data
- opportunity scoring
- IP/common-sense review packet generation
- managed runtime
- human review gates
- audit logs
- shared data model

Possible agents:

| Agent | Role |
|---|---|
| Trend Research Agent | Finds trend, keyword, and niche demand signals from approved sources |
| Niche Scoring Agent | Scores potential T-shirt niches using Observatory criteria |
| Design Brief Agent | Turns approved ideas into design briefs |
| IP Risk Packet Agent | Surfaces obvious brand, celebrity, quote, lyrics, sports, university, or franchise risks for human review |
| Listing Copy Agent | Drafts Etsy titles, tags, descriptions, and disclosure notes |
| Mockup Prep Agent | Prepares mockup requirements or draft asset checklist |
| QA Agent | Checks listing draft quality, policy concerns, and completeness |
| Publishing Prep Agent | Prepares final packet for human approval; does not publish by itself |
| Signal Capture Agent | Sends generalized market/product signals back to the Observatory |

Possible workflow:

```text
Human enters idea or agent finds trend
→ Observatory checks keyword/trend/market context
→ Super T Shirts agents prepare idea packet
→ Human reviews idea
→ IP/common-sense gate
→ Design brief drafted
→ Human approves design direction
→ Listing copy drafted
→ QA review
→ Human publish gate
→ Listing is manually published or approved for assisted publishing
→ Results/signals saved back to workspace and Observatory
```

Important rule:

```text
Super T Shirts agents may draft and prepare.
They may not publish listings without human approval.
```

---

## 7. Shared Observatory Across Businesses

The Observatory should not belong to SearchClarity or Super T Shirts.

It belongs to Neon Ronin.

It receives signals from all workspaces:

```text
SearchClarity paid report signals
Super T Shirts product/niche signals
Future KDP topic signals
Future Gumroad template signals
Future Fiverr service demand signals
```

It returns:

- keyword clusters
- trend profiles
- competitor patterns
- opportunity scores
- data quality notes
- research recommendations
- queue assignments
- generalized observations

Example shared loop:

```text
SearchClarity sees a repeated Etsy visibility problem in a niche
→ submits sanitized signal to Observatory
→ Observatory scores it
→ score suggests it may be useful for Super T Shirts
→ Super T Shirts receives a research queue item
→ human reviews before action
```

This is the compounding value of Neon Ronin.

One business learns something.

The Observatory generalizes it.

Other businesses may benefit.

---

## 8. Data Separation Rules

Neon Ronin must separate business-specific data from generalized intelligence.

| Data | Stored Where | Shared? |
|---|---|---|
| SearchClarity customer info | SearchClarity workspace | No |
| SearchClarity reports | SearchClarity workspace | No, except generalized signals |
| Super T Shirts product drafts | Super T Shirts workspace | No, except generalized signals |
| Etsy shop credentials | Workspace/private secure storage | No |
| Raw market signals | Workspace first, then Observatory if sanitized | Yes, after sanitization |
| Opportunity scores | Observatory | Yes, according to permission rules |
| Agent run logs | Data Core | Limited by workspace permissions |
| Human approvals | Data Core/workspace | Limited by workspace permissions |
| Generalized observations | Observatory | Yes |

Rule:

```text
Private business/customer data stays in the workspace.
Generalized market intelligence can flow to the Observatory.
```

---

## 9. Agent Permissions Across Workspaces

Agents should not automatically see all businesses.

Example:

| Agent | Can Access SearchClarity? | Can Access Super T Shirts? | Can Access Observatory? |
|---|---:|---:|---:|
| SearchClarity Report Drafting Agent | Yes | No | Read selected data |
| SearchClarity Signal Capture Agent | Yes | No | Submit sanitized signals |
| Super T Shirts Design Brief Agent | No | Yes | Read selected data |
| Super T Shirts Listing Copy Agent | No | Yes | Read selected data |
| Observatory Scoring Agent | Sanitized signals only | Sanitized signals only | Yes |
| Orchestrator | Metadata and routing state | Metadata and routing state | Yes |
| Audit Logger | Event metadata | Event metadata | Event metadata |

No agent should cross workspace boundaries unless explicitly granted access.

---

## 10. Human Review Gates Across Workspaces

Every workspace should have strict review gates.

Universal gates:

| Gate | Required Before |
|---|---|
| Idea Gate | Turning an idea into a project |
| IP/Common-Sense Gate | Creating product/design/listing work from risky concepts |
| Quality Gate | Marking a draft as ready for delivery or publishing |
| Customer Delivery Gate | Sending customer-facing reports/messages |
| Publish Gate | Publishing marketplace listings or public content |
| Paid Action Gate | Spending money or launching ads |
| Credential/Permission Gate | Changing connected accounts, tools, or agent permissions |

For SearchClarity:

```text
No customer report is delivered without human review.
```

For Super T Shirts:

```text
No listing is published without human review.
No IP-sensitive idea proceeds without human review.
```

---

## 11. MVP Build Implication

The MVP should not hardcode SearchClarity as the whole app.

Instead, build the minimum multi-workspace system:

1. Workspace registry
2. Job/workflow records
3. Agent registry
4. Review queue
5. Raw signal inbox
6. Observatory scorecard
7. Human approval gates
8. Audit log

Then implement SearchClarity as Workspace 1.

Later implement Super T Shirts as Workspace 2.

This proves Neon Ronin is actually reusable.

---

## 12. Suggested First Workspaces

| Order | Workspace | Why |
|---:|---|---|
| 1 | SearchClarity | First real service business; produces paid-work signals |
| 2 | Super T Shirts | Tests marketplace/product workflow and IP gates |
| 3 | Observatory | Shared intelligence layer should grow alongside both |
| 4 | Future Gumroad/Templates Workspace | Tests digital product workflows |
| 5 | Future Fiverr Services Workspace | Tests productized service workflows |

Observatory is listed third here as a build milestone, but conceptually it exists from the beginning. The practical version can start simple.

---

## 13. What This Changes

This architecture means:

- SearchClarity should not define the whole data model.
- SearchClarity should be configured as a workspace.
- Super T Shirts should be able to plug in later without rewriting the platform.
- Agents should be workspace-scoped.
- The Observatory should be business-agnostic.
- Strategy queues should allow source and target workspace fields.
- Opportunity signals should include source workspace and possible destination workspace.
- Human review gates should be reusable across workspaces.

Important fields to add to future schemas:

```text
workspace_id
business_id
source_workspace_id
target_workspace_id
signal_type
signal_visibility
data_sensitivity
review_gate_required
approval_status
```

---

## 14. Final Principle

Neon Ronin should be designed as a small-business operating system from the start.

Not a SearchClarity backend.

Not an Etsy bot.

Not a single-purpose agent swarm.

It should be:

```text
A human-controlled, multi-workspace agent command center
for running and learning from multiple small businesses.
```

SearchClarity is the first tenant.

Super T Shirts may be the second tenant.

The Observatory is the shared intelligence layer.

The Data Core remembers.

The Orchestrator routes.

Agents assist.

Humans decide.
