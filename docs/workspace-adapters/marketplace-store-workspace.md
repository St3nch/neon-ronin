# Marketplace Store Workspace Adapter

## Purpose

This adapter defines the generic pattern for a marketplace store workspace.

It should not name a specific store brand.

## Typical Needs

- trend research
- product idea intake
- niche validation
- design/product briefs
- IP/common-sense review packets
- listing drafts
- mockup or asset prep
- publish gates
- sales/order notes if integrated later
- signal capture

## Typical Agents

| Agent | Role |
|---|---|
| Trend Research Agent | Finds trend, keyword, and niche demand signals from approved sources |
| Niche Scoring Agent | Scores potential niches using Observatory criteria |
| Product Brief Agent | Turns approved ideas into product/design briefs |
| IP Risk Packet Agent | Surfaces obvious brand, celebrity, quote, lyrics, sports, university, or franchise risks for human review |
| Listing Copy Agent | Drafts titles, tags, descriptions, and disclosure notes |
| Asset Prep Agent | Prepares mockup or asset requirements |
| QA Agent | Checks listing draft quality, policy concerns, and completeness |
| Publishing Prep Agent | Prepares final packet for human approval; does not publish by itself |
| Signal Capture Agent | Sends generalized market/product signals back to the Observatory |

## Generic Workflow

```text
Human enters idea or agent finds trend
-> Observatory checks keyword/trend/market context
-> Workspace agents prepare idea packet
-> Human reviews idea
-> IP/common-sense gate
-> Product/design brief drafted
-> Human approves direction
-> Listing copy drafted
-> QA review
-> Human publish gate
-> Listing is manually published or approved for assisted publishing
-> Results/signals saved back to workspace and Observatory
```

## Review Gates

- idea gate
- IP/common-sense gate
- quality gate
- publish gate
- paid action gate

## Rule

```text
Marketplace store agents may draft and prepare.
They may not publish listings or change live marketplace state without human approval.
```
