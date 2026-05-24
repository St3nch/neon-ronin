# r10 — Observatory and Strategy Layer

## Purpose

This document defines how Neon Ronin turns generalized signals from SearchClarity and future business workspaces into research priorities, strategy queues, service improvements, content ideas, and internal product/listing opportunities.

SearchClarity is the first public-facing SEO/GEO service business workspace using Neon Ronin.

Neon Ronin is the internal agent, database, observatory, and strategy engine that can support multiple business workspaces over time.

This document belongs in Neon Ronin because the observatory and strategy layer are not SearchClarity customer-delivery functions. They are internal intelligence functions that can support SearchClarity and future Neon Ronin-backed businesses.

---

## Clean Separation

| System | Owns | Does Not Own |
|---|---|---|
| SearchClarity | Customers, orders, reports, report templates, customer history, paid deliverables, intake, delivery workflow, market signal capture | Cross-project strategy calculations, agent runtime, observatory scoring, internal opportunity queues |
| Neon Ronin | Agents, database, managed runtime, observatory, strategy scoring, market opportunity queues, research prioritization, cross-project intelligence | Customer-facing SEO service promises, report branding, Fiverr gig delivery, client-facing report language |

Short version:

```text
SearchClarity collects the gold dust.
Neon Ronin melts it into bullets.
```

---

## Data Flow

```text
SearchClarity paid order
→ customer report created
→ customer/report history saved
→ market opportunity signals captured
→ generalized signal export prepared
→ Neon Ronin ingests generalized signals
→ Neon Ronin scores and clusters opportunities
→ Neon Ronin produces strategy queues
→ SearchClarity improves services/content/offers
→ future Neon Ronin-backed projects can use validated intelligence
```

SearchClarity should preserve enough customer/report history to serve returning customers well. Neon Ronin should consume generalized, non-customer-identifying signals for higher-level strategy.

---

## Inputs From SearchClarity

Neon Ronin may consume these generalized or de-identified inputs from SearchClarity:

| Input | Description | Notes |
|---|---|---|
| Market Opportunity Signals | Niche/product/keyword/category gaps flagged during paid research | No customer name, no shop URL, no exact client strategy |
| Keyword Observations | Keyword, cluster, intent, source, date, niche | Source report type is allowed; customer identity is not needed |
| Pattern Tags | Normalized recommendation/problem categories | Bridge from report findings to generalized market learning |
| Generalized Observations | Abstracted insights observed across reports | No single-client identifying detail |
| Outcome Labels | Aggregated recommendation outcome signals | Use confidence levels; do not treat single outcomes as proof |
| Service Demand Signals | Repeat customer paths, add-on requests, revision themes | Supports SearchClarity service roadmap |
| Content Opportunity Signals | Common buyer questions and knowledge gaps | Supports SearchClarity.co authority content |

Neon Ronin should not need raw customer files, payment data, platform credentials, private screenshots, or client-specific confidential strategy to do its job.

---

## Strategy Layer Jobs

The strategy layer answers:

```text
Which niches look promising?
Which keyword clusters deserve deeper research?
Which recommendation patterns are common enough to become default checks?
Which services should SearchClarity build next?
Which content should SearchClarity.co publish?
Which internal listing/product opportunities deserve investigation?
Which signals need more data before action?
```

It produces decisions, not customer reports.

---

## Core Scoring Models

### 1. Market Opportunity Score

Purpose: rank niches, product clusters, or marketplace gaps for deeper research.

SearchClarity r05 captures the signal during paid report work. Neon Ronin applies the same 12-factor scoring model so capture and strategy stay aligned.

Starting formula:

```text
Buyer intent clarity
+ Keyword depth
+ Demand signal
+ Competition weakness
+ Differentiation room
+ Product variation potential
+ Seasonality
+ Content expansion potential
+ Marketplace fit
+ Operational difficulty
+ Risk / IP exposure
+ Strategic value
= Market Opportunity Score
```

Each factor is scored 1–5. Higher is better. For Risk / IP exposure, lower risk receives the higher score.

| Factor | Score | Meaning |
|---|---:|---|
| Buyer intent clarity | 1–5 | Buyers appear to search with purchase intent |
| Keyword depth | 1–5 | Enough long-tail and cluster terms exist to support research/content/listings |
| Demand signal | 1–5 | Search, marketplace, or trend demand appears meaningful |
| Competition weakness | 1–5 | Existing supply is weak, sloppy, thin, generic, or poorly optimized |
| Differentiation room | 1–5 | There is room to create a distinct angle instead of copying the market |
| Product variation potential | 1–5 | The niche supports recipient, occasion, style, material, format, or bundle variants |
| Seasonality | 1–5 | Evergreen demand, seasonal demand, or both create useful timing opportunities |
| Content expansion potential | 1–5 | SearchClarity/Neon Ronin can build SEO, Pinterest, site, or educational content around it |
| Marketplace fit | 1–5 | Fits Etsy, Shopify, Pinterest, Fiverr, Google, or another useful channel |
| Operational difficulty | 1–5 | Realistic to execute without excessive tooling, fulfillment, policy, or workflow pain |
| Risk / IP exposure | 1–5 | Trademark, copyright, policy, and reputation risks are low enough to proceed |
| Strategic value | 1–5 | Helps SearchClarity or Neon Ronin learn, expand, package services, or build assets |

Maximum score: 60.

Score interpretation:

| Score | Meaning | Action |
|---:|---|---|
| 0–25 | Ignore | Not worth time now; retain only if useful as historical noise |
| 26–35 | Watch | Interesting but weak; see if it appears again |
| 36–45 | Research Later | Worth researching when capacity opens |
| 46–55 | Research Next | Strong signal; prioritize public-data research |
| 56–60 | Serious Opportunity | Research promptly and consider action if validated |

### 2. Recommendation Pattern Confidence

Purpose: decide which recurring report findings should become default checks, template sections, or analyst training points.

Inputs:

- frequency across reports
- frequency across niches
- customer outcome signals, if available
- revision/dispute rate
- analyst confidence
- evidence source quality

Output:

```text
Emerging
Confirmed
Default Check
Deprecated
Needs More Evidence
```

### 3. Niche Strength Score

Purpose: evaluate whether a niche deserves a dedicated SearchClarity content page, gig variant, or internal opportunity research.

Inputs:

- number of signals in the niche
- keyword depth
- buyer intent clarity
- weak-competition observations
- content/Pinterest/Shopify expansion potential
- repeat customer demand
- operational fit

Output:

```text
Ignore
Watch
Research
Build Content
Build Service Variant
Investigate Internal Listing/Product Opportunity
```

### 4. Service Expansion Score

Purpose: avoid launching every possible gig too early.

Inputs:

- customer requests
- attach-rate from existing services
- delivery complexity
- pricing potential
- template readiness
- fit with SearchClarity brand
- repeat-order potential

Output:

```text
Do Not Build Yet
Watch
Draft Template
Test Manually
Launch Service
```

---

## Strategy Queues

Neon Ronin should maintain these queues:

| Queue | Purpose | Example |
|---|---|---|
| Market Research Queue | Niches/clusters requiring public-data research | Profession-specific retirement gifts |
| Niche Opportunity Queue | Validated niches worth future action | Teacher appreciation printable bundles |
| Service Expansion Queue | Potential new SearchClarity services | Pinterest SEO Plan, Shopify Product Page Audit |
| Template Improvement Queue | Report sections or checks to update | Add identical-tag-set warning to audits |
| Content Opportunity Queue | SearchClarity.co articles/pages to create | Etsy title structure guide for gift sellers |
| Internal Listing/Product Opportunity Queue | Validated opportunities for future internal products/listings | Adjacent gift niche with weak competition |
| Data Quality Queue | Signals that need more evidence or better source data | Niche has strong anecdotal signal but weak tool confirmation |

---

## Agent Roles Later

Neon Ronin agents may eventually support:

- signal ingestion from SearchClarity trackers
- keyword cluster normalization
- opportunity scoring suggestions
- public research collection
- competitor pattern extraction from public data
- content brief drafting
- report template improvement suggestions
- strategy queue maintenance
- periodic observatory summaries

Agents should assist. They should not make unsupervised money decisions, publish content, contact customers, or alter customer-facing deliverables without human review.

---

## Relationship to SearchClarity r05

SearchClarity r05 defines:

```text
what customer/report history SearchClarity keeps
what market signals SearchClarity captures during paid work
what should not be stored
how returning customers benefit
```

This Neon Ronin r10 defines:

```text
how generalized SearchClarity signals become strategy calculations
how opportunity queues are maintained
how Neon Ronin supports SearchClarity and future businesses
```

SearchClarity r05 is the capture layer.

Neon Ronin r10 is the strategy layer.

---

## First Practical Build

Do not build a complex software system first.

Start with SearchClarity's minimal tracker system and a Neon Ronin strategy workbook / table set:

```text
SearchClarity tracker:
- Customers
- Shops
- Orders
- Reports
- Audited Items
- Recommendations
- Action Plan Items
- Keyword Observations
- Market Opportunity Signals
- Generalized Observations
- Outcomes
- Consent Records

Neon Ronin strategy workbook:
- Signal Inbox
- Market Opportunity Scores
- Niche Scores
- Recommendation Pattern Scores
- Service Expansion Scores
- Strategy Queues
- Research Backlog
```

Once SearchClarity reaches enough paid volume that manual review becomes painful, Neon Ronin can move the strategy layer into a real database and agent-supported workflow.

---

## Final Summary

SearchClarity is the storefront and service business.

Neon Ronin is the engine room and strategy brain.

SearchClarity captures customer history and market signals from real paid work.

Neon Ronin turns generalized signals into decisions about what to research, build, sell, improve, or ignore next.

That separation keeps SearchClarity clean for customers and gives Neon Ronin room to become the broader observatory for future gig businesses.
---

## Appendix A. Migrated Reference Material From SearchClarity r05

**Migration note:** The following material originally lived in SearchClarity 05-client-report-history-and-market-signal-capture.md. It was moved here because generalized market learning models, opportunity scoring, research workflows, observability metrics, and future platform data models belong to Neon Ronin's observatory and strategy layer, not to the customer-facing SearchClarity service docs.

### A.1 Original SearchClarity r05 Section 5

#### Original Section 5: Generalized Market Learning Model

Generalized learning is what makes SearchClarity smarter over time without compromising any individual client. The transformation flow is:

```
Client-specific observation
    → normalized issue pattern
    → aggregated market pattern
    → reusable SearchClarity insight
    → improved report / template / service / product / listing strategy
```

Three things make this safe:

1. **Abstraction strips identity.** Once a pattern is observed in 5+ unrelated clients, it loses its connection to any one of them.
2. **Generalized observations are stored separately.** Different operational layer; different access pattern; the link back to "originally observed in Client X's audit" exists for internal traceability but is never used in any output.
3. **Public sharing requires a higher bar than internal use.** Internal template improvements can use generalized patterns freely. Public content (blog posts, case studies, marketing) requires patterns to be either observed in 10+ unrelated clients *or* corroborated by independent public research.

##### Original Section 5.1: Worked examples

**Example 1 — Etsy titles**

| Stage | Content |
|---|---|
| Client-specific observation | Client A's listing title is "Smells Like Retirement Candle Funny Retirement Gift for Coworker Retirement Party Decor Gag Gift" — leads with cute phrase, buries the buyer-intent term in position 5–7 |
| Normalized issue pattern | "Title leads with cute or theme phrase; buyer-intent recipient/occasion term buried mid-title" |
| Aggregated market pattern | Observed across 12 unrelated gift-niche Etsy audits over 6 months |
| Reusable SearchClarity insight | For gift listings, lead titles with recipient + occasion + product type; cute phrases work better as secondary positioning |
| Application | Updated standard recommendation pattern in r04 Section 4 template; added as a default check in the Title Structure Analysis section of Report 1 |

**Example 2 — Etsy tags**

| Stage | Content |
|---|---|
| Client-specific observation | Client B uses the same 13 tags across 47 listings |
| Normalized issue pattern | "Identical tag set across all listings — low-signal pattern" |
| Aggregated market pattern | Observed in 18 of 24 audited shops where listing count exceeds 20 |
| Reusable SearchClarity insight | Identical tag sets are the modal failure pattern for established Etsy shops, not the exception. Make it a standard finding in shop-level audits |
| Application | Now a default check in Report 5 (Shop Visibility); also surfaced in Report 1 cross-listing patterns chapter |

**Example 3 — Keyword clusters**

| Stage | Content |
|---|---|
| Client-specific observation | Client C's research surfaced "personalized 2026 retirement gift" with low competition and high specificity |
| Normalized issue pattern | "Year-specific personalization terms underserved" |
| Aggregated market pattern | Observed across retirement, wedding, graduation, and birthday niches in 8 separate keyword research packs |
| Reusable SearchClarity insight | Year-specific personalization is a recurring underserved sub-niche across occasion-driven gift categories; recommend as a rotating annual term |
| Application | Added as a standard cluster check in r04 Section 6.6; surfaces in Keyword Research Pack methodology |

**Example 4 — Competitor observations**

| Stage | Content |
|---|---|
| Client-specific observation | For Client D's term "personalized retirement gift for coworker", top results lean functional (mugs, plaques) over decorative (candles, ornaments) at ~11:4 |
| Normalized issue pattern | "Buyer intent for [recipient]+[occasion]+[personalization] queries skews functional over decorative" |
| Aggregated market pattern | Observed in 7 of 9 gift-niche Competitor Observation reports across different recipient/occasion combinations |
| Reusable SearchClarity insight | When a decorative product targets a recipient-specific gift query and underperforms, the pattern is more likely buyer-intent mismatch than listing weakness. Diagnostic question added to analyst training |
| Application | New row in Report 4 standard analysis framework; warning added to Report 1 when audit identifies decorative products targeting functional-skew queries |

**Example 5 — Shop structure**

| Stage | Content |
|---|---|
| Client-specific observation | Client E runs a shop split across three unrelated niches (retirement gifts, wedding gifts, funny coworker candles); each group competes independently |
| Normalized issue pattern | "Niche fragmentation across active listings dilutes shop-level signal" |
| Aggregated market pattern | Observed in roughly half of Shop Visibility Reports for shops over 40 listings |
| Reusable SearchClarity insight | Niche fragmentation is the dominant shop-level visibility problem at 40+ listings — more impactful than any individual listing fix |
| Application | Added as a top-priority diagnostic in r04 Section 8; informs the recommended path section of Report 5 |

**Example 6 — Pinterest**

| Stage | Content |
|---|---|
| Client-specific observation | Client F (established Etsy seller, 18 months in) asks for a Pinterest plan after Audit and Keyword Pack |
| Normalized issue pattern | "Pinterest requests cluster among sellers with existing Etsy traction, not pre-launch sellers" |
| Aggregated market pattern | 8 of 10 Pinterest Plan orders come from sellers with 12+ months Etsy history |
| Reusable SearchClarity insight | Position Pinterest Plan as a *traction-stage* product, not a launch-stage product. Sell sequencing: Audit → Keyword Pack → Pinterest |
| Application | Updated r04 Section 9.1 "When to sell"; informed the Channel Priority table in Report 10 |

**Example 7 — Shopify product pages**

| Stage | Content |
|---|---|
| Client-specific observation | Client G's Shopify meta titles include the brand name in position 1, consuming 13 characters before any buyer-intent term |
| Normalized issue pattern | "Brand-first meta titles waste high-value early characters" |
| Aggregated market pattern | Observed in 14 of 18 Shopify audits |
| Reusable SearchClarity insight | Brand-first meta titles are the default in most Shopify themes; sellers don't realise this is configurable. Make it a top finding |
| Application | Now a default check in Report 7; added to analyst training |

**Example 8 — Schema readiness**

| Stage | Content |
|---|---|
| Client-specific observation | Client H's Shopify product pages have basic Product schema (auto-generated) but lack Brand, AggregateRating, and MerchantReturnPolicy fields |
| Normalized issue pattern | "Auto-generated Shopify Product schema is incomplete relative to current Google Rich Results requirements" |
| Aggregated market pattern | Observed in 11 of 12 Shopify schema audits regardless of theme |
| Reusable SearchClarity insight | The auto-generated baseline is universally incomplete; assume incomplete and check for the three specific missing fields by default |
| Application | Standard table in Report 8 expanded to highlight these three fields explicitly |

**Example 9 — AI search readiness**

| Stage | Content |
|---|---|
| Client-specific observation | Client I's AI search readiness audit found that prompts for the brand return partial information — assistant knows category but not founder, products, or positioning |
| Normalized issue pattern | "Brand entity ambiguity to AI search systems — partial recognition without specificity" |
| Aggregated market pattern | Observed in 6 of 7 AI readiness audits to date |
| Reusable SearchClarity insight | Partial recognition is the modal state for small brands; the readiness gap is consistently in FAQ/About content depth and third-party mention sparsity, not in schema |
| Application | Reordered Report 9 priority recommendations to lead with entity content depth before schema |

**Example 10 — Cross-channel concentration**

| Stage | Content |
|---|---|
| Client-specific observation | Client J generates 92% of revenue from Etsy despite 14-month-old Shopify store |
| Normalized issue pattern | "Single-channel revenue concentration with inactive owned-asset channel" |
| Aggregated market pattern | Common pattern in established Etsy sellers who have launched but not invested in Shopify |
| Reusable SearchClarity insight | The default Strategy Report Channel Priority table should flag Shopify-inactive-but-launched as a top diversification readiness opportunity, not as a "build a Shopify store" recommendation |
| Application | Updated Report 10 Channel Priority table in r04 Section 13.5 |

**Example 11 — Revision patterns**

| Stage | Content |
|---|---|
| Client-specific observation | Client K asks for revision because they expected specific tags, not "tag directions" |
| Normalized issue pattern | "Buyers conflate audit and rewrite reports" |
| Aggregated market pattern | This revision reason appears in ~15% of Audit orders |
| Reusable SearchClarity insight | Audit description must clarify "diagnosis, not implementation" more aggressively at the point of sale and in delivery messages |
| Application | Updated Audit gig copy and Report 1 delivery message in r04 Section 16.3 |

**Example 12 — Returning-customer attach**

| Stage | Content |
|---|---|
| Client-specific observation | Client L purchases Audit then asks immediately about title/tag rewrites |
| Normalized issue pattern | "Audit→Rewrite attach within 7 days of delivery" |
| Aggregated market pattern | This sequence describes ~40% of second orders |
| Reusable SearchClarity insight | Audit delivery message should always close with the Rewrite as the recommended next step (already in r04 Section 16.3); offer a returning-customer discount |
| Application | Standardised in r04 Section 16.3 delivery template |

---

### A.2 Original SearchClarity r05 Section 7.2

#### Original Section 7.2: Opportunity Signal Scoring

Every Market Opportunity Signal gets scored across 12 factors. Each factor receives a score from 1 to 5.

- 1 = weak / bad / unclear
- 3 = decent but not proven
- 5 = strong / obvious / attractive

Higher is better. For Risk / IP exposure, lower risk gets the higher score.

| Factor | Score 1–5 | What To Look For |
|---|---:|---|
| Buyer intent clarity |  | Are people searching with purchase intent? |
| Keyword depth |  | Are there enough long-tail and cluster terms? |
| Demand signal |  | Does the niche appear to have meaningful search/market demand? |
| Competition weakness |  | Are competitors sloppy, generic, poorly optimized, or thin? |
| Differentiation room |  | Can we create a distinct angle? |
| Product variation potential |  | Are there many recipient/occasion/style/material variants? |
| Seasonality |  | Is there evergreen demand, seasonal demand, or both? |
| Content expansion potential |  | Can we build SEO/Pinterest/site content around it? |
| Marketplace fit |  | Does it fit Etsy, Shopify, Pinterest, Fiverr, or other channels? |
| Operational difficulty |  | Is it realistic to execute without a nightmare? |
| Risk / IP exposure |  | Are there trademark, copyright, or policy risks? Lower risk scores higher. |
| Strategic value |  | Does this help SearchClarity/Neon Ronin learn or expand? |

Maximum score: 60.

| Total Score | Classification | Meaning |
|---:|---|---|
| 0–25 | Ignore | Not worth time now. Keep only if the note may matter later. |
| 26–35 | Watch | Interesting but weak. See if it appears again. |
| 36–45 | Research Later | Worth researching when time opens up. |
| 46–55 | Research Next | Strong signal. Put it near the top of the research queue. |
| 56–60 | Serious Opportunity | Very strong. Research promptly and consider action if validated. |

This scoring is intentionally simple. If analysts need a spreadsheet formula, use:

```text
opportunity_score = sum(all 12 factor scores)
```

Do not over-engineer it yet.

### A.3 Original SearchClarity r05 Section 7.5

#### Original Section 7.5: Research Workflow For Strong Signals

Signals classified as **Research Later**, **Research Next**, or **Serious Opportunity** should eventually get independent research.

Research should use public or properly licensed sources such as:

- Etsy search observation
- eRank or comparable Etsy tools
- Google Trends
- Pinterest Trends
- Google SERPs
- Shopify/site observations
- Fiverr/Upwork marketplace observations
- public competitor listings
- public content gaps

The research workflow:

1. Pull the signal record.
2. Confirm the score still looks reasonable.
3. Run public-data research.
4. Update the evidence summary.
5. Decide whether the signal is Rejected, Watch, Research Next, Validated, or Converted.
6. If converted, label the conversion type: content, service improvement, internal project, or listing/product idea.

### A.4 Original SearchClarity r05 Section 7.7

#### Original Section 7.7: Review Cadence

Market Opportunity Signals are reviewed monthly.

The review asks:

- What new signals were logged?
- Which signals scored 46+?
- Which Watch signals appeared repeatedly and deserve a higher score?
- Which signals should move to Research Later or Research Next?
- Which validated signals should become content, service improvements, internal projects, or listing/product ideas?
- Which signals are weak enough to ignore?

At low volume, this is a 30-minute monthly spreadsheet review. Do not turn it into ceremony.

---

### A.5 Original SearchClarity r05 Section 14

#### Original Section 14: Observability / Intelligence Metrics

Internal metrics SearchClarity should watch over time. These are not customer-facing; they're operational and strategic.

| Metric | Why It Matters | How To Use It |
|---|---|---|
| Most common listing issues identified | Tells us what the template needs to address best | Strengthen the most-common-issue section in Report 1 template; train analysts on the modal failure patterns |
| Most common title problems | Sharpens Title Structure Analysis section | Add default checks; refine recommendation patterns |
| Most common tag problems | Sharpens Tag Coverage section | Same |
| Niches frequently audited | Tells us where our market is concentrated | Inform gig positioning, marketing focus, and which adjacent niches to consider (per Section 7) |
| Niches with repeat demand (multiple orders, same niche) | Higher value than single-order niches | Justifies developing niche-specific methodology cheat sheets for analysts; could justify niche-specific gig variants |
| Keyword clusters appearing across clients | Shows market-wide demand patterns | Generalized layer; informs r04 Section 6.6 cluster definitions; informs methodology content |
| Recommendations most often reused (pattern tag frequency) | The patterns that recur are the patterns that matter most | Promote to default checks in the relevant report; consider for blog/methodology content |
| Recommendations with positive follow-up signals | Validates which patterns actually move the needle | Strengthen confidence in those recommendation patterns; reflect cautiously in methodology content |
| Recommendations with negative or mixed signals | Tells us which patterns are weaker than thought | Revise; potentially deprecate; warn analysts |
| Report types with most repeat orders | Identifies the highest-LTV report types | Prioritise quality investment; identify natural attach-rate opportunities |
| Revision reasons (categorised) | Operational learning | Spot patterns; fix in gig copy, intake, or report template |
| Average turnaround time per report type | Operational health | Detect drift; flag training needs; inform pricing |
| Customer questions after delivery (categorised) | What our reports are not explaining well enough | Update report template; update gig copy |
| Add-on conversion rates (Audit → Rewrite, Audit → Keyword Pack, etc.) | Revenue per customer; bundle-design signal | Inform delivery message templates (per r04 Section 16); inform bundle pricing |
| First-order to second-order conversion rate | The whole point of returning-customer focus | If low, returning-customer experience is broken; investigate |
| Time between first and second order | Tells us how aggressively to nudge | Inform timing of follow-up review-request messages |
| Outcome label distribution per recommendation pattern | Empirical methodology quality | Direct input to template refinement |
| Market Opportunity Signals logged per month | Measures analyst engagement with the intelligence layer | If low, add flagging as an explicit step in the post-research analyst checklist |
| Composite score distribution across signals | Tells us whether the scoring system is being applied or just all checked as high | Recalibrate scoring guidance if distribution is skewed; flag if most signals cluster at extreme scores |
| Signals per niche | Which niches keep surfacing as interesting | Strongest indicator of where independent research time should go |
| Signals progressed to Validated | Measures the funnel from observation to confirmed opportunity | If low relative to signals logged, the research step has a bottleneck |
| Validated signals actioned (into content / listings / gigs) | Measures conversion from intelligence to strategy | The terminal metric — the whole system exists to produce this |

These metrics are watched at quarterly intervals minimum. None of them are individually published; aggregated insights from them can inform public content per Section 11.

---

### A.6 Original SearchClarity r05 Section 15

#### Original Section 15: Future Database Implications

Not a software design. A list of what the future data model must support, so that whoever builds it knows the requirements up front.

| Future Entity | Purpose | Notes |
|---|---|---|
| Customer | Person paying for work; returning-customer recognition | Email is the natural unique identifier; minimize fields |
| Shop / Website | The unit of work; every report links here | Multiple shops per customer possible; one shop per report typical |
| Platform Account | Source channel + platform-side order tracking | Multiple platform accounts per customer possible (Fiverr now, direct later) |
| Order | Transactional record | Foreign keys to customer, shop, platform account |
| Report | Deliverable; metadata + file references | Foreign key to order; one report per order typical, but allow multiple (for bundles) |
| Audited Listing / Page | Snapshot at audit time | Foreign key to report; multiple per report; capture text content, reference URLs to media |
| Keyword Observation | Atomic keyword research unit | Foreign keys to report and niche; keyword text indexable for cross-client reuse; source + source date critical |
| Recommendation | Five-line recommendation block | Foreign keys to report, listing/page (optional), pattern tag (optional); priority enum |
| Action Plan Item | Subset of Recommendation tracked for outcome | Foreign keys to report and recommendation; status enum; outcome link |
| Outcome | Empirical layer | Foreign keys to action plan item; outcome label enum; confidence enum; consent flag |
| Revision / Support Note | Operational log | Foreign keys to order/report; summary text, not raw transcripts |
| Generalized Observation | The intelligence layer | No foreign keys to specific clients (by design); links to source observations counted, not retained as identifiers |
| Market Signal / Opportunity | Scored, researched opportunities flagged during paid work | **No client identifiers**; source field records engagement type, not client name; the signal exists independently of any one client; scores and research status evolve over time |
| Pattern Tag | Bridge entity between Recommendation and Generalized Observation | Many-to-many; allows abstracting a specific recommendation into a generalized pattern category |
| Niche | Categorisation for shops and keyword observations | Free-text descriptor + normalized cluster; allows cross-shop pattern aggregation |
| Consent Record | For testimonials, case studies, public examples | Foreign key to customer; specifies scope and revocability |
| Retention Schedule | Configurable retention policy applied automatically | Per data type; per Section 10 |
| Anonymization Status | Flag indicating whether a record has been anonymized for public use | Per record where applicable |

**Architectural notes for the future build:**

- **Client-specific data and generalized observations must be cleanly separable.** Either separate schemas, separate databases, or rigorously enforced access controls — but the boundary needs to be operationally real, not just notional.
- **Retention rules must be applied automatically.** Manual deletion will not happen on schedule. The database should know its own retention rules and act on them.
- **Consent records are mandatory before publication.** Building the consent record system before the public case study system is the correct order.
- **Pattern tags need to be a controlled vocabulary, not free-text.** A free-text "what kind of recommendation is this" field will drift into uselessness within months.
- **The customer's portal view (if we ever build one) shows the customer their own data — only.** No cross-customer visibility, no generalized layer exposed, no leakage between accounts.
- **Audit logs.** Internal access to client-specific data should be logged. Not for surveillance — for accountability if a customer ever asks "who saw my data".

This is enough specification to inform a future build. The current state is "spreadsheets and folders"; that's fine for the first 20–50 orders. Moving to a real database becomes important once volume exceeds what a single analyst can hold in their head.

---


