# foodcosting.app - Community Monitor Agent Research

**Date:** April 20, 2026
**Status:** Build-ready research brief
**Scope:** Distribution Team / Community Monitor Agent

---

## Executive Summary

The Community Monitor Agent should start as a Reddit-only daily triage agent.

Its job is not to post, DM, promote, or summarize broad community sentiment. Its first useful job is narrower:

> Find 3-5 fresh Reddit threads each day where Ahmed can give a genuinely useful answer about food costing, menu pricing, recipe costing, margins, supplier price increases, or tool/spreadsheet pain.

Reddit is feasible because public subreddit listings and search can be accessed through OAuth-backed API clients. Facebook Groups should remain manual or semi-manual for now because automated group reading depends on Meta permissions, group/admin approval, and policy constraints.

---

## Platform Findings

### Reddit

Reddit is the best first platform for automation.

Relevant official constraints:

- Reddit requires OAuth for Data API authentication.
- Reddit requires a unique, descriptive `User-Agent`.
- Free API access is rate limited to 100 queries per minute per OAuth client id, averaged over a 10-minute window.
- Clients can be throttled or blocked if unidentified.
- API use must comply with Reddit's Developer Terms and Data API Terms.

Practical implication:

- A daily monitor polling 5-10 subreddits is comfortably within rate limits.
- The agent should store fetched metadata and output links, not build a large permanent mirror of Reddit content.
- The agent should never post automatically.

Sources:

- Reddit Data API Wiki: https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki
- Reddit API docs: https://www.reddit.com/dev/api/
- Reddit Data API Terms: https://redditinc.com/policies/data-api-terms
- PRAW subreddit docs: https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html

### Facebook Groups

Facebook Groups are not a good first automation target.

Automated group content access generally requires app review, permissions, and group/admin context. For this project, Facebook should be handled as:

- Ahmed manually joins and monitors priority groups.
- Agent assists from copied thread text, screenshots, or manually exported notes.
- Later version can add a browser-assisted workflow only if it is compliant with group rules and platform permissions.

Practical implication:

- Do not build Facebook scraping in v1.
- Add a "manual inbox" format later: Ahmed pastes Facebook thread text into `research/inbox/community_threads.md`, then the response drafter can help.

Source:

- Meta Groups API documentation: https://developers.facebook.com/docs/groups-api/

---

## Source Of Truth: Notion Subreddit Database

Ahmed already researched relevant subreddits in Notion. The Community Monitor Agent should use that work as the source of truth instead of hardcoding the subreddit list in the repo.

Canonical database:

`foodcosting / Reddit / Sub-Reddits`

The local config file should be a cache or fallback, not the primary editorial database. This matters because subreddit quality will change over time as Ahmed learns which communities actually produce useful conversations and signups.

### Notion Access Requirements

To read the Notion database, the agent needs:

```text
NOTION_API_KEY=
NOTION_REDDIT_SUBREDDITS_DATABASE_ID=
NOTION_REDDIT_SUBREDDITS_DATA_SOURCE_ID=
NOTION_VERSION=2026-03-11
```

Current Notion API note: Notion split databases and data sources in the newer API model. The agent should retrieve the database first, then query the relevant data source. If the database has only one data source, the script can discover it from the database response and `NOTION_REDDIT_SUBREDDITS_DATA_SOURCE_ID` can be optional.

The database must also be shared with the Notion integration via Notion's `Add connections` menu, otherwise the API may return a `404` even if the database ID is correct.

Sources:

- Notion API intro: https://developers.notion.com/reference/intro
- Retrieve a database: https://developers.notion.com/reference/database-retrieve
- Retrieve a data source: https://developers.notion.com/reference/retrieve-a-data-source
- Query a data source: https://developers.notion.com/reference/query-a-data-source
- Working with databases: https://developers.notion.com/guides/data-apis/working-with-databases

### Recommended Notion Schema

The existing database may already have different property names. If so, map those names in config instead of renaming the database immediately. For a clean v1, the agent needs these fields:

| Property | Type | Required | Purpose |
|---|---:|---:|---|
| `Name` | Title | Yes | Human-readable subreddit name |
| `Subreddit` | Rich text or URL | Yes | `restaurantowners`, `r/restaurantowners`, or full Reddit URL |
| `Status` | Select | Yes | `Active`, `Watch`, `Paused`, `Rejected` |
| `Priority` | Number or Select | Yes | Weight for scoring, e.g. `1.0`, `0.8`, `0.4` |
| `Audience` | Multi-select | No | Restaurant, food truck, catering, bakery, small business |
| `Angle` | Multi-select | No | Pricing, costing, operations, startup, tools |
| `Rules URL` | URL | No | Link to subreddit rules |
| `Promotion Risk` | Select | No | Low, Medium, High |
| `Notes` | Rich text | No | Ahmed's qualitative notes |
| `Last Checked` | Date | No | Optional writeback after successful monitor run |
| `Useful Threads` | Number | No | Optional scorecard |
| `Noise Level` | Select | No | Low, Medium, High |

Minimum viable fields are `Subreddit`, `Status`, and `Priority`.

### Notion Filtering Rules

The monitor should query rows where:

- `Status` is `Active` or `Watch`
- `Subreddit` is not empty
- `Promotion Risk` is not `High`, unless `Priority` is high and Ahmed has explicitly marked it active

The monitor should ignore:

- `Paused`
- `Rejected`
- rows without a subreddit identifier
- linked database views that do not expose the original data source to the integration

### Local Cache

Each run should save the Notion subreddit list to:

`pipeline/out/community-monitor/subreddit-cache.json`

The cache should include:

```json
{
  "fetched_at": "2026-04-20T00:00:00",
  "source": "notion",
  "database": "foodcosting / Reddit / Sub-Reddits",
  "subreddits": []
}
```

If Notion is unavailable, the agent can use this cache for one run and clearly mark the report:

`Warning: using cached subreddit list because Notion fetch failed.`

If there is no cache, the agent should fail gracefully instead of falling back to guesses.

---

## What The Agent Should Monitor

### Starting Subreddits

Use Ahmed's Notion database first. If no Notion access is configured yet, this temporary seed list can be used only for initial testing:

- `r/restaurantowners`
- `r/foodtrucks`
- `r/catering`
- `r/smallbusiness`
- `r/restaurateur`
- `r/KitchenConfidential` with extra selectivity
- `r/Baking` only for home bakery / cottage-food pricing threads

Do not treat all subreddits equally. The `Priority`, `Promotion Risk`, `Audience`, and `Noise Level` properties from Notion should drive scoring. `r/smallbusiness` has broad reach but more noise. `r/restaurantowners`, `r/foodtrucks`, and `r/catering` should score higher for relevance unless Ahmed's Notion notes say otherwise.

### Query Themes

The monitor should search recent posts using theme buckets, not one giant keyword list.

**Food costing fundamentals**

- food cost
- food cost percentage
- COGS
- cost of goods
- margins
- profit margin
- prime cost

**Recipe and menu costing**

- recipe cost
- recipe costing
- menu pricing
- price my menu
- cost per plate
- cost per serving
- ingredient cost

**Pricing and profitability**

- how much should I charge
- pricing strategy
- markup
- margin
- profitable
- losing money
- too expensive

**Operations and control**

- supplier prices
- vendor prices
- invoice prices
- food waste
- portion control
- price increases

**Tool intent**

- spreadsheet
- Excel
- calculator
- software
- app
- tool
- template

---

## Evidence From Reddit

Recent and historical Reddit threads show recurring problems that match foodcosting.app's content pillars:

- Restaurant/cafe owners struggle to allocate fixed costs into menu prices without making items look overpriced.
- Operators ask what software or spreadsheet model to use for cost per plate.
- Food businesses compare rules of thumb like 20%, 25%, or 30% food cost, often without context.
- Owners complain that supplier price increases are hard to track consistently.
- Experienced operators advise starting with high-cost items, top sellers, invoice checks, and "something is better than nothing" measurement.

Example thread types found:

- `r/smallbusiness`: "Pricing items on menu in restaurant business? How to do it?"
- `r/smallbusiness`: "People who run a restaurant, how do calculate the cost per plate..."
- `r/smallbusiness`: "Restaurant owners: How do you manage costing and margins?"
- `r/restaurant`: "Restaurant owners: How bad have food costs gotten lately?"

These are exactly the threads where Ahmed can answer with practical costing advice and optionally save language for future SEO content.

---

## Agent Inputs

The primary input should be the Notion database:

`foodcosting / Reddit / Sub-Reddits`

Use a config file only for defaults, property-name mapping, and fallback behavior:

`pipeline/context/community-monitor-config.json`

Suggested shape:

```json
{
  "source": "notion",
  "notion_database_name": "foodcosting / Reddit / Sub-Reddits",
  "notion_property_map": {
    "name": "Name",
    "subreddit": "Subreddit",
    "status": "Status",
    "priority": "Priority",
    "audience": "Audience",
    "angle": "Angle",
    "promotion_risk": "Promotion Risk",
    "noise_level": "Noise Level",
    "notes": "Notes"
  },
  "max_thread_age_hours": 48,
  "max_comments": 50,
  "daily_limit": 5,
  "exclude_if_locked": true,
  "exclude_if_removed": true,
  "allow_cache_fallback": true
}
```

Environment variables:

```text
NOTION_API_KEY=
NOTION_REDDIT_SUBREDDITS_DATABASE_ID=
NOTION_REDDIT_SUBREDDITS_DATA_SOURCE_ID=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USERNAME=
REDDIT_PASSWORD=
REDDIT_USER_AGENT=windows:foodcosting-community-monitor:v0.1.0 (by /u/<username>)
```

Use a read-only OAuth flow if possible. If using PRAW script auth, keep credentials in `.env` and never commit them.

---

## Agent Output

Write one dated Markdown file per run:

`pipeline/out/community-monitor/YYYY-MM-DD.md`

Suggested output:

```markdown
# Community Monitor - 2026-04-20

## Top Threads

### 1. Pricing items on menu in restaurant business? How to do it?

- Platform: Reddit
- Subreddit: r/smallbusiness
- URL: ...
- Age: 3h
- Comments: 12
- Score: 86
- Match reasons: menu pricing, fixed cost allocation, new cafe/restaurant
- Suggested angle: Explain separating ingredient cost, labor/overhead assumptions, and market price validation. Warn against forcing all fixed costs equally onto every item.
- Product mention: No
- Pain-point language:
  - "product price ridiculously high"
  - "without precise sales data"
  - "operational cost per item"
```

Also write machine-readable JSON for downstream agents:

`pipeline/out/community-monitor/YYYY-MM-DD.json`

The response drafter should consume the JSON, while Ahmed reviews the Markdown.

---

## Scoring Model

Start with a transparent heuristic score. Do not use an LLM for everything in v1.

### Positive Signals

- Thread age under 24 hours: `+25`
- Thread age 24-48 hours: `+10`
- Comments under 10: `+15`
- Comments 10-30: `+8`
- Exact match for high-intent terms: `+20`
- Mentions "tool", "software", "spreadsheet", "calculator", or "Excel": `+15`
- Mentions food business type: restaurant, food truck, catering, bakery, cafe: `+15`
- Question phrasing: `+10`
- Subreddit priority multiplier: `0.3-1.0`

### Negative Signals

- Older than 48 hours: exclude
- More than 50 comments: exclude
- Locked or removed: exclude
- Meme/rant with no actionable question: `-20`
- Job/career/kitchen drama thread with no costing angle: `-25`
- Explicit "no promotion/research" moderation issue: `-25`

### Product Mention Classification

The monitor should pre-classify product mention safety:

- `none`: Answer only; no product mention.
- `soft`: Blog/calculator may be useful if Ahmed already has trust in the thread.
- `direct`: Only when the poster explicitly asks for software, app, calculator, template, or spreadsheet.

Default should be `none`.

---

## Build Recommendation

### V1: Python + PRAW Daily Script

Add:

- `scripts/fetch_notion_subreddits.py`
- `scripts/fetch_reddit_community_threads.py`
- `pipeline/context/community-monitor-config.json`
- `pipeline/out/community-monitor/` output directory

Use the Notion API to load Ahmed's researched subreddit database. Use PRAW because it handles Reddit OAuth, listings, search, and subreddit APIs cleanly.

Core flow:

1. Load `.env`.
2. Load community monitor config.
3. Fetch active/watch subreddits from `foodcosting / Reddit / Sub-Reddits` in Notion.
4. Save a local subreddit cache.
5. For each subreddit:
   - Fetch recent `new` submissions.
   - Search targeted keyword groups with `sort="new"` and `time_filter="week"`.
6. Deduplicate by Reddit submission id.
7. Filter by age, comments, locked/removed status.
8. Score using heuristics and Notion priority/risk fields.
9. Extract title, selftext snippet, URL, subreddit, created time, score, comment count, matched terms.
10. Save top 3-5 to Markdown and JSON.
11. Optionally update `Last Checked` in Notion after a successful run.

### V1.5: Add LLM Triage

After the heuristic list is narrowed to maybe 20 candidate threads, an LLM can classify:

- Is this actually about food costing/pricing?
- What is the best response angle?
- Is product mention appropriate?
- What pain-point language is worth saving?

Keep the LLM downstream of filtering to reduce cost and avoid noisy outputs.

### V2: Pain Point Bank

Append extracted phrases to:

`research/output/pain-point-language-bank.md`

Fields:

- Date found
- Platform/community
- Thread URL
- Exact phrase
- Theme
- Content opportunity

### V3: Facebook Manual Inbox

Add:

- `research/inbox/facebook-community-threads.md`
- A script or prompt that parses pasted Facebook thread text and produces the same JSON schema as Reddit output.

---

## Risks And Guardrails

- **Spam risk:** The agent must never post. Ahmed posts manually.
- **Community ban risk:** Product links should be rare and only when requested.
- **API policy risk:** Use OAuth, real User-Agent, and low request volume.
- **Low relevance risk:** Start with few subreddits and inspect outputs for a week before expanding.
- **Tone risk:** Response drafter must write like a helpful operator/founder, not a marketer.
- **Privacy/copyright risk:** Store snippets, metadata, and links. Do not mirror full threads unnecessarily.

---

## Definition Of Done For V1

The Community Monitor Agent is ready when:

- It reads the subreddit list from Notion's `foodcosting / Reddit / Sub-Reddits` database or clearly reports why it used cache.
- Running one command creates a dated Markdown report and JSON file.
- It surfaces 3-5 relevant Reddit threads from the last 48 hours.
- Each thread includes match reasons and suggested response angle.
- It excludes stale, saturated, locked, or irrelevant threads.
- It runs without posting or writing to Reddit.
- Ahmed can review the report in under 5 minutes.

---

## Recommended Next Step

Build V1 as a local Python script using PRAW and a JSON config file. After 7 daily runs, review:

- How many surfaced threads were worth responding to?
- Which subreddits produced useful opportunities?
- Which keywords created noise?
- Whether response drafting should be automated next or after another week of monitoring data.
