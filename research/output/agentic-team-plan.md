# foodcosting.app — Agentic Team Plan

**Last updated:** April 18, 2026
**Owner:** Ahmed
**Status:** Active working document

---

## Philosophy

Ahmed has ~5–7 hours/week. An agentic team multiplies that into 30+ hours of output. The agents do the volume work. Ahmed does the judgment work. Nothing goes public without Ahmed's review.

**Rule: Agents draft. Ahmed decides. Agents execute approved actions. Agents never publish.**

---

## Team Structure

```
Ahmed (Founder / Editor-in-Chief / Final Approver)
│
├── Content Production Team
│   ├── Topic Researcher Agent
│   ├── Blog Writer Agent
│   ├── Short-Form Script Writer Agent
│   └── Remotion Video Renderer Agent
│
├── Distribution Team
│   ├── Community Monitor Agent
│   ├── Community Response Drafter Agent
│   └── Social Media Scheduler Agent (planned)
│
├── Intelligence Team
│   ├── SEO Tracker Agent (planned)
│   ├── Competitor Monitor Agent (planned)
│   └── Pain Point Analyst Agent (planned)
│
└── Operations Team
    ├── Weekly Report Agent (planned)
    └── Notion/Database Maintenance Agent (planned)
```

---

## Active Agents (Built & Scheduled)

### 1. Topic Researcher Agent

**Purpose:** Analyze GSC data to identify the highest-opportunity content topic for the next blog post.

**Trigger:** Scheduled (2x/week, before blog writer)
**Input:** Google Search Console data, existing blog post inventory
**Output:** Structured content brief with target keyword, search intent, outline, and competitor analysis
**Handoff:** Brief is saved for Blog Writer Agent to pick up

**What "good" looks like:**
- Identifies keywords with rising impressions but low click-through (opportunity gap)
- Avoids topics already covered unless the existing post is underperforming
- Prioritizes Tier 1 (money) keywords over Tier 2 (problem) keywords
- Brief includes: primary keyword, secondary keywords, search intent, suggested H2s, competitor URLs to beat, target word count

---

### 2. Blog Writer Agent

**Purpose:** Write a full SEO-optimized blog post from the topic researcher's brief.

**Trigger:** Scheduled (2x/week, after topic researcher)
**Input:** Content brief from Topic Researcher
**Output:** Complete markdown blog post ready for review
**Handoff:** Post saved for Ahmed to review → publish to site and Notion

**What "good" looks like:**
- Hits target word count (1,200–2,000 words typically)
- Includes primary keyword in title, H1, first paragraph, and 2–3 H2s
- Natural internal links to other blog posts and free tools
- CTA to sign up woven into the content (not a hard sell)
- Reads like advice from a food business expert, not a software company
- No fluff, no filler, no generic business advice

---

### 3. Short-Form Script Writer Agent

**Purpose:** Repurpose blog posts into short-form video scripts for YouTube Shorts and Facebook Reels.

**Trigger:** Scheduled (after blog posts are published)
**Input:** Published blog post + handoff notes
**Output:** Structured video script with hook, body, CTA, and recommended Remotion props
**Handoff:** Script saved for Remotion Renderer Agent

**What "good" looks like:**
- Hook in first 2 seconds (question or surprising stat)
- 30–60 seconds total
- One clear takeaway per video
- CTA: "Link in bio" or "Search foodcosting.app"
- Script includes visual direction (text overlays, transitions)

---

### 4. Remotion Video Renderer Agent

**Purpose:** Render short-form video scripts into final MP4 files.

**Trigger:** After short-form script is approved
**Input:** Script with Remotion props
**Output:** MP4 file in `pipeline/out/`
**Handoff:** Video ready for Ahmed to review → upload to platforms

**What "good" looks like:**
- Clean captions, readable on mobile
- Brand-consistent colors and fonts
- Under 60 seconds
- Renders without errors

---

### 5. Community Monitor Agent (needs building)

**Purpose:** Scan target communities daily for threads where food costing knowledge is relevant.

**Trigger:** Daily (morning)
**Input:** List of target communities + qualifying criteria
**Output:** Top 3–5 threads worth responding to, with context and suggested angle
**Handoff:** Threads surfaced for Community Response Drafter

**Qualifying criteria:**
- Someone asking about food cost calculation, menu pricing, or recipe costing
- Someone complaining about margins, pricing confusion, or cost tracking
- Someone asking for tool recommendations in the food business space
- Avoid: threads older than 48 hours, threads with 50+ comments (already saturated)

**Implementation approach:**
- Reddit: Use Reddit API or web scraping for target subreddits
- Facebook: Harder to automate — may need manual monitoring with agent-assisted summarization
- Start with Reddit only, add Facebook monitoring when feasible

---

### 6. Community Response Drafter Agent (needs building)

**Purpose:** Draft helpful, authentic responses to community threads surfaced by the Monitor.

**Trigger:** After Community Monitor surfaces threads
**Input:** Thread context, community rules, engagement rules from distribution playbook
**Output:** Draft response for Ahmed to review, edit, and post manually
**Handoff:** Draft → Ahmed reviews → Ahmed posts

**What "good" looks like:**
- Answers the question completely (no link-bait half-answers)
- Sounds like a knowledgeable food business person, not a bot
- No product mention unless the thread explicitly asks for tools
- Matches the tone of the community (casual in Reddit, professional in Facebook groups)
- Under 200 words typically (concise, not essays)

---

## Planned Agents (Not Yet Built)

### 7. Social Media Scheduler Agent

**Purpose:** Take approved videos and schedule them across YouTube, Facebook, and Instagram.
**Status:** Planned for Phase 2
**Dependency:** Need platform API access or a scheduling tool (Buffer, Later, or direct API)
**Ahmed's role:** Approves content, agent handles scheduling

---

### 8. SEO Tracker Agent

**Purpose:** Weekly automated pull of GSC data — keyword positions, traffic, top pages, CTR.
**Status:** Planned for Phase 1 (Month 2)
**Output:** Weekly SEO summary saved to a tracking file or Notion
**Why:** Ahmed shouldn't manually check GSC. This feeds the Topic Researcher with fresh data.

---

### 9. Competitor Monitor Agent

**Purpose:** Monthly scan of competitor websites, pricing pages, and feature announcements.
**Status:** Planned for Phase 2
**Output:** Summary of changes — new features, pricing changes, new content
**Why:** Catch competitive moves early. Feed comparison page content.

---

### 10. Pain Point Analyst Agent

**Purpose:** Aggregate pain-point language from community monitoring and search queries into themes.
**Status:** Planned for Phase 2
**Output:** Monthly report of top pain points, language patterns, and content/feature opportunities
**Why:** Closes the loop between community listening and content production.

---

### 11. Weekly Report Agent

**Purpose:** Compile weekly metrics into a single summary for Ahmed.
**Status:** Planned for Phase 1 (Month 2)
**Output:** One-page summary: signups, MRR, traffic, top content, community engagement, agent output
**Why:** Ahmed needs a 5-minute weekly review, not a dashboard to explore.

---

### 12. Notion/Database Maintenance Agent

**Purpose:** Keep the Notion blog database accurate — sync published status, update metrics, flag stale content.
**Status:** Planned for Phase 2
**Output:** Notion updates, flagged issues for Ahmed
**Why:** Database drift (as we just cleaned up) wastes time and causes confusion.

---

## Agent Build Priority

| Priority | Agent | Phase | Effort | Impact |
|---|---|---|---|---|
| 1 | SEO Tracker | Phase 1, Month 2 | Low | Feeds topic research with fresh data |
| 2 | Weekly Report | Phase 1, Month 2 | Low | Saves Ahmed 30+ min/week |
| 3 | Community Monitor (Reddit) | Phase 1, Month 3 | Medium | Unlocks daily community engagement |
| 4 | Community Response Drafter | Phase 1, Month 3 | Medium | Reduces response drafting to review-only |
| 5 | Pain Point Analyst | Phase 2 | Low | Closes community → content loop |
| 6 | Social Media Scheduler | Phase 2 | Medium | Removes manual posting |
| 7 | Competitor Monitor | Phase 2 | Low | Monthly intel on competitive moves |
| 8 | Notion Maintenance | Phase 2 | Low | Prevents database drift |

---

## Agent Pipeline Flows

### Content Pipeline (Active)

```
GSC Data
  ↓
Topic Researcher → Content Brief
  ↓
Blog Writer → Draft Blog Post
  ↓
Ahmed Reviews → Approved Post
  ↓
Published to Site + Notion
  ↓
Short-Form Writer → Video Script
  ↓
Ahmed Reviews → Approved Script
  ↓
Remotion Renderer → MP4 Video
  ↓
Ahmed Reviews → Upload to Platforms
```

### Community Pipeline (To Build)

```
Reddit API / Facebook Groups
  ↓
Community Monitor → Top 3-5 Threads
  ↓
Community Response Drafter → Draft Responses
  ↓
Ahmed Reviews + Edits → Posts Manually
  ↓
Pain Point Analyst → Language Bank
  ↓
Feeds back into → Topic Researcher
```

### Intelligence Pipeline (To Build)

```
GSC Data + Community Data + Competitor Data
  ↓
SEO Tracker (weekly) + Competitor Monitor (monthly) + Pain Point Analyst (monthly)
  ↓
Weekly Report Agent → One-Page Summary for Ahmed
  ↓
Ahmed makes decisions → Adjusts priorities
```

---

## Scheduled Triggers (Current)

7 remote triggers are configured for content production:

| Trigger | Schedule | Agent | Status |
|---|---|---|---|
| Blog Post (Tue) | Tuesday 8am ET | Topic Researcher → Blog Writer | Active |
| Blog Post (Sat) | Saturday 8am ET | Topic Researcher → Blog Writer | Active (re-enabled) |
| Social (Mon) | Monday 9am ET | Short-Form Writer | Active |
| Social (Tue) | Tuesday 9am ET | Short-Form Writer | Active |
| Social (Wed) | Wednesday 9am ET | Short-Form Writer | Active |
| Social (Thu) | Thursday 9am ET | Short-Form Writer | Active |
| Social (Fri) | Friday 9am ET | Short-Form Writer | Active |

---

## Infrastructure Needs

| Need | Status | Action |
|---|---|---|
| GitHub repo access for agents | Fixed (reconnected) | Monitor for auto-disable |
| GSC API access | Needed | Set up for SEO Tracker agent |
| Reddit API access | Needed | Set up for Community Monitor |
| Email platform (Mailchimp/Loops) | Not started | Set up in Phase 1 |
| Video hosting / upload API | Not started | Needed for Social Scheduler |
| Cloudinary access | Active (`dcqba0rmb`) | Available for image hosting |

---

## Agent Development Principles

1. **Start simple, iterate.** First version of any agent should take <2 hours to build. Optimize later based on output quality.
2. **Every agent has a clear handoff.** Input → Processing → Output → Next step. No ambiguous "figure it out" agents.
3. **Human review is non-negotiable for public content.** Agents that produce draft content always route through Ahmed before publishing.
4. **Agents log their work.** Every agent run should produce an artifact (file, Notion update, or log entry) so Ahmed can audit what happened.
5. **Fail gracefully.** If an agent can't complete its task (API down, bad data), it should save what it has and flag the issue — not retry silently or produce garbage.
6. **Agents feed each other.** The goal is a compounding system where community insights improve content, content drives SEO, SEO drives traffic, traffic produces signups. Design agents to pass data downstream.

---

## Monthly Agent Team Review

Every month, Ahmed should spend 30 minutes answering:

1. Which agents produced useful output this month?
2. Which agents produced output I always had to heavily edit or discard?
3. Are there manual tasks I did repeatedly that an agent could handle?
4. Are any agents running but producing no value? (Turn them off.)
5. What's the next agent to build based on where I'm spending the most time?

---

*This plan evolves as agents are built and tested. Add new agents only when there's a clear, repeated task they'd handle. Don't build agents for one-off tasks — that's what ad-hoc Claude Code sessions are for.*
