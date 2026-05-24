# Marketplace Keyword & Demand Data Sources for Agent-Powered Commerce (Etsy, POD, Fiverr, Digital Products) — 2026 Reference Report

## TL;DR
- **There is no single source of truth for Etsy demand. Build a layered stack: (1) DataForSEO Labs + Keywords Data + SERP APIs as the programmable foundation; (2) Etsy's own Marketplace Insights tool plus the Open API v3 `/listings/active` endpoint as the only official Etsy buyer-search signal; (3) one Etsy-niche vendor for shop/listing intelligence — eRank for data depth or Sale Samurai for $9.99 Chrome workflow are the strongest 2026 options; (4) Pinterest Trends API and TikTok Creative Center Keyword Insights for cross-platform demand triangulation.**
- **Reddit, Pinterest keyword-level volume, and Etsy autocomplete are now legal hot zones.** Reddit's commercial Data API ($0.24 per 1,000 calls plus required approval) killed GummySearch (announced Nov 6, 2025; signups closed Nov 30, 2025); Etsy's API Terms now explicitly forbid using API data "for purposes of analytics, machine learning, training artificial intelligence models … unless expressly authorized in writing by Etsy"; Pinterest's official Trends API is read-only with no keyword-level volume API. Treat any product depending on scraped autocomplete or undisclosed Reddit/Etsy ingestion as a ToS-fragile dependency.
- **For a pure pay-as-you-go agent stack, DataForSEO at ~$0.0006–$0.002 per SERP query and $0.05–$0.075 per Google Ads keyword call is dramatically cheaper than Semrush ($499.95/mo Business plan plus ~$50/M units, with Adobe having completed the Semrush acquisition on April 28, 2026) and Ahrefs API v3 ($500–$10,000/mo on top of an Advanced subscription).** Combine with SerpApi only when you specifically need its multi-engine coverage and US Legal Shield, and add Helium 10 ($39–$279/mo) for Amazon product/keyword depth that DataForSEO's Amazon Labs API doesn't match on listing analytics.

## Key Findings

### 1. DataForSEO is the cheapest production-grade foundation, but its marketplace coverage is Google-Shopping-and-Amazon-centric — there is no native Etsy endpoint.

DataForSEO confirmed product catalog (per dataforseo.com/apis and docs.dataforseo.com, verified April 2026):

| API | Coverage relevant to this stack | Live mode cost | Standard mode cost |
|---|---|---|---|
| SERP API | 20+ Google endpoints (incl. Autocomplete, Shopping, Images, YouTube), Bing, Yahoo, Baidu, Naver, Seznam | $0.002/query | $0.0006/query (Standard), $0.0012 (Priority) |
| Keywords Data → Google Ads (search_volume) | Google Keyword Planner data, up to 1,000 keywords/request | $0.075/request | $0.05/request |
| Keywords Data → Google Trends | Up to 5 keywords/request; Google Search, News, Images, Shopping, **YouTube** | $0.009/task | $0.00225/task |
| Keywords Data → DataForSEO Trends (proprietary clickstream) | Explore, Subregion, Demography, Merged | n/a | Explore $0.001, Merged $0.005 |
| Keywords Data → Bing Ads | Bing Keyword Planner | $0.075 | $0.05 |
| Keywords Data → Clickstream Data | Refined search volume blended with clickstream | varies | varies |
| DataForSEO Labs Google API | Keyword Ideas $0.01 + $0.0001/kw, Related Keywords, Ranked Keywords, Search Intent ($0.001 + $0.0001/kw), Historical SV, Bulk KD | live only | n/a |
| DataForSEO Labs Amazon API | Bulk Search Volume (1,000 kw), Related Keywords, **Ranked Keywords by ASIN** ($0.011), Product Competitors, Product Keyword Intersections ($0.0105), Product Rank Overview | live only | n/a |
| DataForSEO Labs App Store / Google Play | ASO keyword research | live only | n/a |
| Merchant API → Amazon | Products by keyword, ASIN detail, Sellers (Reviews currently **temporarily unavailable**) | n/a | Standard only |
| Merchant API → Google Shopping | Organic, Paid, Sellers, Product Spec, Product Info, Sellers AD URL | varies | varies |
| Business Data API → Social Media | **Pinterest pin-saves count for a URL**, **Reddit shares for a URL**, **Facebook likes count for a URL** (URL-level only — *not* keyword-level Pinterest or Reddit mining) | live only | n/a |
| Business Data API → Trustpilot / Tripadvisor / GMB Reviews | reviews mining | varies | varies |
| OnPage / Backlinks / Content Analysis / AI Optimization (LLM Mentions, AI Keyword Search Volume, LLM Responses, LLM Scraper) | site audit, link graph, content mentions, LLM brand monitoring | varies | varies |

Critical gaps and confirmations:

- **No Etsy endpoint.** DataForSEO scrapes Etsy URLs only when they appear *inside* a Google SERP (e.g., `etsy.com/market/...` URLs with `etv` and `traffic_cost` from `databases/google/serp_regular`). There is no `merchant/etsy/products` endpoint.
- **No Pinterest keyword volume.** Pinterest endpoint in DataForSEO returns saves count for a target URL only.
- **Reddit support is URL-level only.** Returns subreddit, author, permalink, title, member count for shares of a target URL. No Reddit keyword-mention search.
- **No TikTok or Instagram coverage as of May 2026.**
- **YouTube:** supported via YouTube SERP API (organic, video info, channel info, comments, subtitles) and Google Trends `type=youtube`. No YouTube keyword search-volume endpoint (consistent with Google not publishing one).
- **Rate limit:** 2,000 calls/minute, 30 simultaneous requests (per `dataforseo_labs/amazon/ranked_keywords/live` docs and FAQ).
- **Pricing model:** $50 minimum deposit, $1 free trial credit, no monthly subscription. Balance has no expiry. Sandbox returns synthetic data only.
- **Storage rights:** DataForSEO's ToS says "you can rest assured: using DataForSEO services is absolutely legal … you can't break a search engine's ToS by simply getting data through our APIs." Task results retained 30 days, re-retrievable free. ToS imposes no cache duration limit on customers, but downstream marketplace ToS still attach to stored content.
- **Accuracy:** NextGrowth (Q1 2026 review) cites ~90% accuracy on keyword volume vs Ahrefs/Semrush and a 17-second median support response (2025); G2 reviews echo this. DataForSEO has not published an independent accuracy study.

### 2. Etsy now publishes more first-party demand data than ever — and simultaneously tightened its API Terms against AI/analytics use.

**Marketplace Insights (Beta, GA-rolling 2025–2026):** Etsy unveiled Marketplace Insights at Etsy Up on September 18, 2025; Value Added Resource reported: "Sellers get sneak peek of new Marketplace Insights tool at Etsy Up virtual conference … Seller Growth Expert Maureen Sitterson gave more details about this new tool during her segment at Etsy Up." Built into Shop Manager → Stats → Marketplace Insights. Free tier = **15 keyword searches/week**; Etsy Plus ($10/month) = **unlimited searches** plus 30-day daily search-trend graph and competition-level metric. Results persist 7 days. Data points: searches in last 30 days, listing volume, related keywords, trending searches by category. This is the only source that exposes real Etsy buyer search frequency rather than an estimate. Confirmed by Etsy Help (help.etsy.com/hc/en-us/articles/35122361353239).

**Etsy Open API v3** (developer.etsy.com):

- OAuth 2.0 only since April 3, 2023 (v2 sunset). ~90 endpoints across listings, shops, orders, payments, shipping, reviews, users. Dev MCP Server now available.
- Search endpoint = `GET /v3/application/listings/active` with `keywords`, `sort_on` (created/price/score), `taxonomy_id`, `shop_location`, `min_price`/`max_price`. **Hard offset ceiling of 12,000** (confirmed in URL Syntax doc and GitHub Discussion #1188): "For performance reasons, the offset parameter is limited to a maximum value of 12000. The count property in the response body will provide the total number of records without the limit applied."
- **No autocomplete endpoint.** All third-party Etsy autocomplete data (eRank, EverBee, KeywordTool.io) is scraped from etsy.com HTML, which the API ToS prohibits "unless expressly authorized in writing by Etsy."
- **No Etsy Ads keyword planner.** Etsy Ads exposes bid recommendations only.
- **Rate limits:** Sliding-window algorithm with `x-limit-per-second` and `x-limit-per-day` headers; default-tier QPS/QPD values are app-specific in the Developer Portal (legacy default 10 QPS / 10,000 QPD widely cited). Etsy's API Terms confirm an **Enterprise Tier for apps exceeding 3,000,000 calls/day**. Increases via developer@etsy.com.
- **Caching ToS:** "You will not display listing content more than **six (6) hours** older … any other Etsy content more than **twenty-four (24) hours** older than the content displayed on the Etsy Site … not cache or store [it] longer than is reasonably necessary."
- **Critical 2024–2026 ToS additions:** "Use the Etsy API to collect, scan, or otherwise request Etsy content for purposes of **analytics, machine learning, training artificial intelligence models, licensing, or content removal, unless expressly authorized in writing by Etsy.**" This is the single biggest legal risk for an agent-powered commerce system. Also: prohibition on browser extensions and automated systems scraping the Etsy site, no checkout replication, mandatory trademark disclaimer, perpetual royalty-free license to Etsy on info submitted, no screen-scraping.
- **April 15, 2025 breaking change:** deprecation of certain listing properties; variations migrated to "custom variation"; `getPropertiesByBuyerTaxonomyId`/`getPropertiesByTaxonomyId` no longer return deprecated properties; `updateListingInventory`/`updateListingProperty` 400 on deprecated property_ids.
- **April 9, 2026 deprecation:** legacy listing personalization fields replaced by `personalization_questions` structure / `getListingPersonalization` endpoint.

### 3. Etsy-niche SEO tools: a fragmenting market where eRank leads on data depth, Sale Samurai on Chrome-first UX, EverBee on POD product validation.

| Tool | 2025–2026 pricing | What it gives you | Methodology / risk |
|---|---|---|---|
| **eRank** | Free / Basic $5.99 / Pro $9.99 / Expert $29.99 per month | Keyword Tool (~15-month trend graphs, est. avg CTR, related-keyword exports, country data), Listing Audit, Rank Checker, Bulk Keyword Tool, Trend Buzz, Chrome extension; Etsy OAuth integration | eRank Help explicitly disclaims: they "rely on data from third-party data analytics companies" for SV estimates; realigning against Etsy Marketplace Insights |
| **Sale Samurai** | $9.99/month or $99/year; 3-day free trial | Chrome extension with on-page Etsy SV display, AI listing optimization, long-tail keyword discovery, competitor analysis | Footer: "Uses the Etsy API but is not endorsed or certifed by Etsy, Inc." SV methodology not disclosed |
| **EverBee** | Free Hobby (20 searches/month) / Pro $7.99 / Growth $29.99 per month (per Glenn Broome 2025 review; other 2025 reviews cite $9.99–$29.99) | Chrome extension with product sales estimates, revenue estimates, tag display, 180M+ listing database, POD features, claims 900,000+ users | Sales estimates model-based; strong POD seller mindshare |
| **Marmalead** | ~$19/month after 14-day free trial (no free plan) | Original Etsy SEO tool, engagement scores, seasonal trends, listing optimization, pricing analysis (Bargain/Average/Premium) | Reviewers (Growing Your Craft, Sale Samurai marketing) flag SV accuracy concerns; shop disconnect requires emailing support |
| **Alura** | Free / Starter ~$13.99 / Growth ~$27.99 per month (per reviews) | Keyword Finder, Product Research, Etsy Followup, listing helper, Chrome extension | All-in-one; Etsy OAuth |
| **EtsyHunt** | Free / Pro (~$3.99–$19.99 per reviews) | Largest claimed Etsy product database, Amazon Handmade product search, similar-keyword tool | Budget option; less analytical depth than eRank |
| **Koalanda** | Free / paid tiers | Etsy keyword research, competitor analysis, Listing Editor; claims **89% average accuracy on listing sales history and 100% on shop sales history for past year** | Primary source: official Etsy API plus ML estimation layer; above-average methodology transparency |
| **MakerWords / InsightFactory / Crest / ListingView / InsightAgent / Product Flint** | $4.99–$30+/month; some free | Crest = own-shop analytics; ListingView = 130M+ listings + bulk editing; InsightAgent = market intelligence + AI listing workflows | None disclose Etsy commercial-API approval publicly |

**API availability:** None of these tools publishes a public API or partner program for keyword data. They expose data through their own UI or Chrome extension only — so an agent cannot legitimately ingest their search-volume numbers; you must reimplement keyword research using DataForSEO/Etsy/Pinterest primitives or sign manual data agreements.

### 4. Pinterest: one official trends API, no keyword-volume API, third-party scraping is widely available but ToS-risky.

- **Pinterest API v5 → Trends endpoint** (`/trends/keywords/{region}/top/{trend_type}`): returns top trending keywords by region/trend_type with `pct_growth_wow`, `pct_growth_mom`, `pct_growth_yoy`, and 52-week `time_series` normalized 0–100. Up to 50 results per call. Supports `include_demographics`, `include_predictions`, and `normalize_against_group`. **Not** a search-volume API — values are relative popularity like Google Trends. Access scoped to "agencies, Enterprise clients, and partner platforms."
- **Pinterest Trends consumer site** (trends.pinterest.com) and the annual **Pinterest Predicts** report are richer than the API but human-readable only.
- **Pinterest Ads Manager keyword planner**: provides search-volume estimates inside ad creation flow; requires advertiser account.
- **DataForSEO Pinterest support is URL-level saves only.**
- **Third-party scrapers** (SociaVault, Apify Pinterest Trend Spy / Autocomplete Scraper / Search Scraper, Post2Pin) expose autocomplete and pin metadata for $0.005–$0.05 per call. Violate Pinterest developer ToS; use only with written legal risk assessment.
- **Tailwind** (largest Pinterest-marketing SaaS) provides scheduling/analytics; no public keyword-research API.

### 5. Reddit: post-2023 paid tier, Pushshift gone, and the GummySearch shutdown is the canary in the coal mine.

- **Reddit Data API:** Free tier = 100 QPM per OAuth client, OAuth required, NSFW restricted since July 2023. **Commercial use requires prior Reddit approval and pays $0.24 per 1,000 calls** (per Reddit's 2023 announcement and the Data API Wiki). 1,000-post hard cap on listing endpoints with no date-range filtering and no historical/archive access.
- **Pushshift:** Effectively shut down for public use after Reddit's May 2023 API changes; limited mod-only access remains.
- **GummySearch shutdown:** announced by founder Fed on **November 6, 2025** (per gummysearch.com/final-chapter and solopreneur.global), with new signups and payments closing November 30, 2025; the platform had served **over 135,000 founders, marketers, and investors** (per GummySearch's own farewell page). Founder said he didn't want to "operate in a gray area." Existing paid users retain access through November 30, 2026.
- **Current viable alternatives:**
  - **Subreddit Signals** — explicitly runs on Reddit's official commercial API.
  - **F5Bot** — free email alerts only (Reddit + Hacker News + Lobsters).
  - **Syften** — $19/month, multi-platform monitoring.
  - **RedShip, Reddinbox, ReplyAgent, Trend Seeker, PainOnSocial, StackLead, Prems** — most position around commercial API agreements.
  - **DataForSEO Reddit** support is URL-shares only, not keyword search.
- **Reddit Ads targeting data** is inside Reddit Ads Manager (interest categories, subreddit targeting, contextual keywords) but does not export a keyword-volume table.

### 6. Google / SERP layer: DataForSEO wins on pure $/query, SerpApi wins on engine breadth and legal shield, Semrush/Ahrefs only make sense if you also want the dashboard.

| Provider | Pricing (verified 2026) | Storage / commercial use | Best for |
|---|---|---|---|
| **DataForSEO SERP** | $0.0006/query Standard, $0.0012 Priority, $0.002 Live; AI Summary $0.01; $50 min deposit, $1 free trial | Pay-as-you-go; ToS confirms storage of results is "absolutely legal"; 30-day task replay | Highest-volume programmatic stacks; agent infrastructure |
| **SerpApi** | Developer $75/mo for 5K ($0.015/query); scales to ~$0.005/query at volume; only successful searches billed; cached searches free | $2M U.S. Legal Shield; SOC 2 Type II; **Google sued SerpApi on December 19, 2025 (Case No. 5:25-cv-10826-YGR, N.D. Cal.) alleging DMCA bypass of SearchGuard; SerpApi CEO Julien Khaleghy filed a 31-page motion to dismiss on February 20, 2026; hearing scheduled May 19, 2026 at 2:00 p.m. before Judge Yvonne Gonzalez Rogers** | Multi-engine breadth, legal-compliance-centric apps; **diversify away from sole reliance until lawsuit resolves** |
| **Serper** | $50/mo for 50K (~$0.001/query) | Subscription; less mature support | Cheap LLM/agent grounding |
| **SearchApi** ($2M legal protection) | $0.003–$0.01 range per query | Includes Etsy, Walmart, eBay search engines as named endpoints | Multi-engine ecommerce |
| **Semrush API** | Requires **Business plan $499.95/mo** + units (~$50 per 1M units); $0.00005/unit; 10 units/line live, 50 units/line historical | Cannot resell raw data per Semrush ToS; **Adobe completed its $1.9B Semrush acquisition on April 28, 2026 (Adobe Newsroom)** — pricing/policy stability is now a live risk for existing contracts | Agencies already on Semrush |
| **Ahrefs API v3** | Listed plans start at $500/mo Standard, scaling to $10,000/mo Enterprise; requires ≥ $449/mo Advanced subscription (~ $949/mo all-in entry) | Limited resale rights | Backlink-heavy use cases |
| **Moz Pro API** | Moz Pro plans range $39–$239/mo; API on higher tiers | Per-record commercial caps | Backlinks + branded integrations |
| **Google Ads Keyword Planner (official)** | Free with Google Ads account; bucketed without active spend | Google Ads API ToS — data must support a Google Ads end-user benefit | Internal tooling only |
| **Google Trends API** | Google's official Trends API is in **alpha** (launched 2025); restricted quotas, GCP auth, limited endpoints (interest over time, top trends, related queries) | Alpha terms | Supplemental signal only; most production use goes through DataForSEO Google Trends or DataForSEO Trends |
| **Google Search Console API** | Free; limited to your verified properties | First-party data only | Tracking your own shop's organic queries |
| **KeywordTool.io / AnswerThePublic / AlsoAsked** | $69–$199/mo typical; AnswerThePublic owned by Neil Patel | Scraped autocomplete + cluster outputs | Editorial keyword expansion; **do not rely on for legally-clean storage** |

### 7. YouTube and TikTok: ads-platform creative intelligence, not keyword-volume APIs.

- **YouTube Data API v3:** no search-volume data; video metadata, search results, channel stats, comments. Quota-unit free-tier system. Use Google Trends with `type=youtube` (via DataForSEO at $0.00225/Standard task) for the closest keyword-popularity proxy.
- **vidIQ and TubeBuddy:** browser-extension + dashboard products. Both expose "keyword score," "search volume," "competition" estimates inside their UI; **neither publishes a developer API for keyword data**. Pricing commonly reported as: vidIQ Pro $7.50/mo, Boost $39/mo, Boost+ $79/mo; TubeBuddy Pro $4.99/mo, Legend $19.99/mo — confirm directly with vendor before relying on these numbers. Estimates derived from YouTube autocomplete + suggested queries + clickstream models.
- **YouTube autocomplete:** scrapeable via DataForSEO YouTube SERP API or directly via Google suggestqueries; commercial use carries Google ToS risk.
- **TikTok Creative Center → Keyword Insights** (ads.tiktok.com/business/creativecenter/keyword-insights): free with TikTok Ads Manager / Business account login; returns **Popularity, CTR, CVR, CPA, 6-Second View Rate** for keywords drawn from **TikTok ad campaigns** (not organic posts). Filter by region/industry/objective/keyword-type/time-period. Up to ~500 keywords per view. Updated every 24–48 hours per Stackmatix.
- **TikTok Trends (Trend Discovery, Top Ads, Top Products):** free organic and paid trend signals by region/industry. **Creator Search Insights** surfaces underserved-but-trending search terms for creators.
- **TikTok Symphony / Symphony Assistant / Symphony Creative Studio:** TikTok's 2025 AI ad-creation suite, integrated with Creative Center.
- **TikTok Shop Seller Center analytics:** seller-scoped only.
- **No public TikTok keyword/audience API for third parties.** DataForSEO has no TikTok endpoints.
- **Meta / Instagram:** Audience Insights largely retired in 2021; only first-party Insights and Ads-targeting categories remain. Brand24/Sprout/Talkwalker scrape Instagram via paid social-listening agreements. DataForSEO has no Instagram/Facebook keyword endpoints.

### 8. Marketplace-specific demand tools (Amazon, eBay, Walmart, Etsy-adjacent).

| Marketplace | Best official/native source | Best third-party | Keyword/search-volume data? |
|---|---|---|---|
| Amazon | Amazon Brand Analytics ABA (free to brand-registered sellers); SP-API for advertising data | **Helium 10** ($39 Starter / $99 Platinum / $279 Diamond per month, Jan 2026 update; 7-day full-access trial); **Jungle Scout Catalyst** ($49 Starter / $79 Growth Accelerator / $149 Brand Owner + CI per month); **SmartScout** for market-level intel; **DataForSEO Labs Amazon API** for raw bulk SV ($0.01 + items) and ranked-keywords-by-ASIN ($0.011/call) | Yes — Cerebro / Magnet, JS Keyword Scout, DataForSEO Labs all surface SV; ABA Search Frequency Rank is the gold standard. Jungle Scout exposes a paid public API at $29–$199/mo (4K–10K calls; $0.05 overage) restricted to Growth Accelerator / Brand Owner + CI subscribers; Helium 10 does not publish a public developer API |
| eBay | **Terapeak Product Research** built into Seller Hub (free since April 2021); 3 years of sold-data; Browse API for catalog; Trading API for transactions | ZIK Analytics, Algopix, Putler, MarkSight | Yes — Terapeak gives keyword-level sold-listing data and sell-through rate. **No public Terapeak API**; UI-only with mobile app access added in 2025–2026. The eBay Finding API has been deprecated and decommissioned (Feb 5, 2025) — use Browse API |
| Walmart | Helium 10 supports Walmart at all paid tiers; Walmart Brand Portal analytics | Helium 10; DataForSEO Merchant Google Shopping picks up Walmart in Shopping SERPs | Helium 10 Walmart keyword data is the main third-party source |
| Shopify ecosystem | Shopify Marketplace App data; built-in search analytics for your own store | n/a (each store is private) | First-party only |
| Creative Market / Gumroad / Redbubble / Society6 / Envato / Fiverr | None expose public keyword/search-volume APIs | Scrapers via Apify, ScrapingBee, custom infrastructure | No published demand data. **Fiverr in particular has no keyword tool** — sellers reverse-engineer via gig-search HTML and Google Trends |

### 9. Autocomplete data: a patchwork with substantial legal asymmetry.

| Platform | Official autocomplete API? | Practical 2026 access |
|---|---|---|
| Google | DataForSEO Google Autocomplete SERP API (live $0.002); SerpApi google_autocomplete engine; SearchApi; Serper | Scraped from Google's suggest endpoint; widely tolerated |
| Etsy | **None** | All third-party Etsy autocomplete is scraped — formally a ToS violation. Use Etsy Marketplace Insights instead |
| Pinterest | None (autocomplete not exposed in API v5) | Apify Pinterest Autocomplete Scraper, SociaVault, Post2Pin |
| Amazon | None public; ABA Top Search Terms is the brand-registered substitute | DataForSEO Labs Amazon Related Keywords, Helium 10 Magnet, KeywordTool.io Amazon |
| YouTube | DataForSEO YouTube SERP / Google Trends `type=youtube`; SerpApi YouTube Search | Scraped suggestqueries |
| TikTok | TikTok Creative Center Keyword Insights (ads-only) | Apify scrapers exist; ToS-risky |
| eBay | Terapeak's autocomplete (UI); Browse API has limited keyword suggestions | DataForSEO/SearchApi eBay endpoint provides SERP |

### 10. Data licensing & storage matrix (the questions your legal team will ask).

- **DataForSEO:** scraped public data, customer can store outputs indefinitely; 30-day task replay; no downstream storage cap imposed, but the source-platform ToS (Etsy, Pinterest, Amazon, Reddit) attach to the *content* you store.
- **Etsy Open API:** **6-hour cache on listing content, 24-hour cache on other content**, no AI/ML/analytics training "unless expressly authorized in writing," mandatory trademark disclaimer, perpetual royalty-free license to Etsy on info you submit, no screen-scraping.
- **Amazon SP-API / PA-API:** PA-API requires Associate tag and minimum sales activity; data may not be cached >24 hours; commercial use confined to Amazon affiliate use cases. SP-API data scope is your own seller account.
- **Pinterest:** API data is for "your business' use of the Pinterest API" — third-party redistribution restricted; commercial Trends API access for agencies/enterprise/partner platforms only.
- **Reddit:** commercial use approval required; user-deleted content must be deleted from your store; author identifying info must be deleted when an account is deleted.
- **SerpApi:** $2M US legal shield to customers; cached searches free and reusable; subject to outcome of Google's DMCA suit (motion to dismiss heard May 19, 2026).
- **Semrush:** no resale of raw data; cannot expose Semrush data as raw API to your own customers without partnership; **Adobe acquisition closed April 28, 2026** — policy review expected.
- **Ahrefs:** v3 API (late 2025 launch) replaced v2; storage rights tied to subscription tier.

### 11. Recent (2024–2026) changes that affect this stack.

- **GummySearch shutdown:** announced by founder Fed on **November 6, 2025**; new signups/payments closed **November 30, 2025**; existing paid users retain access through Nov 30, 2026 — the first major Reddit-research tool casualty after Reddit's commercial API policy.
- **Etsy Marketplace Insights** launched at Etsy Up **September 18, 2025**; rolling out through 2026.
- **Etsy AI Writing & Search Tools** (Sept 2025): Listing Title Suggestions, AI Writing Assistant, Smarter Discovery & Search, Review Highlights, Delivery Estimates.
- **Etsy API Terms update** banning analytics/ML/AI-training use of API data "unless expressly authorized in writing."
- **Etsy April 15, 2025 property deprecation** and April 9, 2026 personalization deprecation.
- **Google's official Trends API launched (alpha)** in 2025; restricted quotas.
- **Adobe completed its $1.9B Semrush acquisition on April 28, 2026** (Adobe Newsroom: "Adobe announced the completion of its acquisition of Semrush Holdings, Inc.").
- **Google sued SerpApi** under DMCA on December 19, 2025; motion to dismiss hearing held May 19, 2026 in N.D. Cal.
- **TikTok Symphony AI suite** went GA inside Creative Center, 2025–2026.
- **DataForSEO Trends API and AI Optimization API** (LLM Mentions, AI Keyword Search Volume, LLM Responses, LLM Scraper) launched 2024–2025 to track LLM-driven brand mentions and emerging AI-search volume metrics.
- **Helium 10 added TikTok Shop support** at Diamond tier; **Jungle Scout renamed plans** (Basic→Starter, Suite→Growth Accelerator, Professional→Brand Owner + CI); Helium 10 discontinued its old Starter plan in 2026.
- **eBay Finding API decommissioned February 5, 2025**, replaced by Browse API.

## Details

### Recommended Stacks by Use Case

**Stack A — Pure agent infrastructure (digital products, no human dashboard needed):**
- DataForSEO SERP API (Standard $0.0006/query) for Google + Etsy SERP visibility
- DataForSEO Keywords Data → Google Ads search_volume ($0.05/Standard request for up to 1,000 kw) for baseline volumes
- DataForSEO Labs Amazon (Ranked Keywords by ASIN $0.011) for Amazon depth
- DataForSEO Trends (Merged Data $0.005/task) for seasonality
- Pinterest Trends API (free for approved partners) for visual-search demand
- TikTok Creative Center (free with Business login) for emerging trends
- Etsy Open API `/listings/active` for catalog depth (rate-limited, 12K offset ceiling, 6-hour content cache)
- Etsy Marketplace Insights (human-in-loop or seller-scoped automation) for the only first-party Etsy buyer-search signal

**Stack B — Etsy/POD seller-facing SaaS:**
- Same as Stack A, plus
- eRank or Sale Samurai as a seller-facing UI layer (licensed/resold UI, or build your own atop DataForSEO + Etsy API)
- EverBee for POD validation features
- Helium 10 for cross-marketplace Amazon/Walmart/TikTok Shop expansion

**Stack C — Fiverr / digital services demand:**
- Google Search Console (your own data) + DataForSEO Keywords Data Google Ads
- DataForSEO SERP API to track Fiverr URLs ranking in Google
- DataForSEO Trends + Google Trends for service-keyword seasonality
- Reddit via licensed commercial API or Subreddit Signals for service pain-point discovery
- TikTok Creative Center for service-creator demand signals

### Unknowns / Requires Vendor Confirmation

- Exact default-tier QPS/QPD for Etsy Open API v3 in 2026 (legacy 10 QPS / 10,000 QPD widely cited; current Etsy docs show example values 150/100K)
- Whether Etsy considers a third-party that ingests Etsy API data and exposes AI-driven recommendations to that shop's own owner as "expressly authorized" — legal review recommended
- Reddit commercial-API rate-card beyond the published $0.24/1K (Reddit doesn't publish a rate card; requires direct negotiation)
- Current Pinterest Trends API access criteria for non-agency/non-enterprise developers
- Whether SerpApi's DMCA lawsuit outcome (motion to dismiss heard May 19, 2026) will change SERP-data acceptable use industry-wide
- Whether Adobe will reprice or restrict the Semrush API for builders following the April 28, 2026 acquisition close
- vidIQ and TubeBuddy public API availability — none documented as of writing; pricing figures cited are common but should be re-verified with vendors

## Recommendations

**Stage 1 — Build (week 0–4):** Sign up for DataForSEO ($50 deposit) and Etsy Open API. Implement: (a) DataForSEO Google Ads search_volume + Trends Merged Data for baseline keyword universe; (b) Etsy `/listings/active` ingestion at most every 6 hours per keyword (matching Etsy ToS); (c) cache layer that stores raw API responses but flags Etsy-sourced fields with a 6-hour expiry. **Threshold to scale up:** if you hit 10,000 daily Etsy API calls and aren't yet seeing rate-limit headers near zero, request a tier increase via developer@etsy.com.

**Stage 2 — Validate (week 4–12):** Add Pinterest Trends API (apply via developers.pinterest.com), TikTok Creative Center (free Business login), and one Etsy-niche tool's UI as a sanity check on your DataForSEO-derived numbers. Run eRank or Sale Samurai side-by-side for 50 keywords; if your volume estimates correlate r > 0.7 with Etsy Marketplace Insights numbers, drop the niche tool from the critical path.

**Stage 3 — Differentiate (week 12+):** Layer DataForSEO AI Optimization API (LLM Mentions, AI Keyword Search Volume) if your agent recommends listings optimized for ChatGPT/Perplexity/Gemini commerce queries — this is the most defensible 2026 moat that incumbents don't yet have. **Threshold to add Reddit:** only if you can either (a) afford a licensed commercial Reddit Data API agreement ($0.24/1K + approval) or (b) operate purely on licensed alternatives like Subreddit Signals — do **not** ingest scraped Reddit in any commercial offering.

**Decisions to make now:**
1. **Hard no on scraped Etsy autocomplete in a commercial AI/agent product.** The recent Etsy ToS update makes this an unacceptable legal risk. Replace any autocomplete-driven feature with Marketplace Insights + Etsy taxonomy + DataForSEO Google Autocomplete.
2. **Diversify SERP providers.** Use DataForSEO as primary and either Serper ($50/mo for 50K) or SerpApi as backup, given Google's pending DMCA suit against SerpApi (motion-to-dismiss hearing May 19, 2026).
3. **Budget for Etsy Plus ($10/mo per shop)** for unlimited Marketplace Insights searches if your team manually validates 50+ keywords/week.
4. **Lock in DataForSEO usage now.** Pay-as-you-go means no negotiation leverage, but at $0.0006/SERP you have headroom even at 10× current volume; set a $500/mo alarm and shift traffic from Live to Standard queue at that threshold.
5. **Begin Reddit commercial API approval paperwork now** if Reddit signals matter to your product — approval takes months. Otherwise design the agent so Reddit is enrichment, not core.
6. **Re-quote Semrush contracts at renewal.** With Adobe's acquisition completed April 28, 2026, renewal pricing is in flux; lock multi-year terms in writing if Semrush is in your stack.

## Caveats

- **Pricing volatility.** DataForSEO pricing was verified Q1 2026 but has changed multiple times since 2023. Semrush pricing post-Adobe-close is uncertain. Reddit's stated $0.24/1K dates from 2023 and commercial deals are negotiated individually.
- **EverBee and Marmalead pricing varies across 2025–2026 reviews** — confirm on each vendor's pricing page before relying.
- **vidIQ and TubeBuddy pricing** cited here was not independently re-verified for this report; confirm with vendors.
- **The 90% accuracy claim for DataForSEO** is from a vendor-influenced review (NextGrowth) — not an independent academic study. No published independent accuracy benchmark exists for Etsy-tool search-volume estimates.
- **Etsy Marketplace Insights is still labelled Beta** in the Etsy Seller Handbook; methodology and metric definitions can change. Treat reverse-engineering of its numbers as fragile.
- **The Etsy ToS quotes are sourced via web search excerpts** because etsy.com/legal/api returns HTTP 403 to automated fetchers. Text is consistent across multiple search returns and the original API ToS, but a manual review on Etsy's site is recommended before any production deployment.
- **Google's official Trends API is in alpha** — quotas and endpoints may change without notice.
- **SerpApi's legal status is in flux** pending the Northern District of California's ruling on the motion to dismiss (heard May 19, 2026 — the day before this report). Diversify before relying on SerpApi as sole infrastructure.
- **Pinterest/TikTok/YouTube keyword-research scrapers** (Apify, SociaVault, etc.) are commercially available but put a commercial product in the same position GummySearch was in pre-shutdown. Treat as research-only, not production data sources.