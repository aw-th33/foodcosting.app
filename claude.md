# foodcosting.app — Project Context & Objectives

This file provides full business context for working on foodcosting.app. Read it before taking any action. Every task — whether coding, content, marketing, or strategy — should be evaluated against the north star metric and the core principles defined here.

---

## What This Is

foodcosting.app is a lightweight menu pricing and food cost calculation tool built for SMB food business owners in the US: restaurants, caterers, home bakers, and food truck operators.

The key differentiator is simplicity. This is not a full inventory management system. It is a focused, affordable tool for businesses that cannot justify the cost or complexity of enterprise platforms. The product should always feel light and easy — that is a core product principle, not just a marketing claim.

The app is built on Lovable (React-based), delivered as a PWA optimized for mobile.

---

## Competitive Landscape

| Competitor | Why Owners Leave or Avoid |
|---|---|
| MarketMan | Expensive, complex, built for large operations |
| Reciprofity | Feature-heavy, steep learning curve |
| Supy | Enterprise-focused, not SMB-friendly |
| Meez | Strong on recipe costing but broader in scope |

**Our position:** The lightest, most affordable option for owners who just need food costing done — not a platform to run their entire operation.

---

## Pricing

| Plan | Price |
|---|---|
| Monthly | $15 / month |
| Limited Lifetime deal | $99 / year |
| Annual (alt) | $149 / year |

There is no lifetime deal currently active. Long-term plan is to optimize pricing tiers once there is sufficient conversion data.

---

## North Star Metric (Current Focus)

**Signups.** Every decision should be evaluated against whether it moves signups. Product polish, new features, and scope creep are explicitly deprioritized unless they directly unblock conversion. The MVP is built. The bottleneck is marketing and growth.

---

## Distribution Strategy

### SEO

SEO is building traction. Keywords started at 40+ positions on Google and are now trending toward 20+. This is a signal worth compounding — not a reason to switch channels.

The approach is niche-specific, low-competition terms rather than broad food cost keywords dominated by established players. Free tools (calculators) and blog content are the primary SEO levers. Google Search Console and occasional Ahrefs use are the tracking tools.

Priority keyword clusters:

- Niche calculator terms (e.g. cake pricing calculator, food truck cost sheet)
- Long-tail recipe costing and menu pricing terms
- Competitor comparison terms

### Community Engagement

Facebook group engagement has produced real signups and is the most proven channel so far. Reddit has been underutilized and should be expanded. The approach in both channels is to position as a food business expert — not a founder — and provide genuine value before ever mentioning the product.

Target communities: food business Facebook groups, r/foodtrucks, r/smallbusiness, r/restaurantowners, r/catering, r/MealPrepSunday.

The goal is to become the person people associate with food costing knowledge. Trust is the asset. Aggressive link dropping kills it.

### Social Media (Building From Zero)

A brand social media presence is a planned channel. The cold start problem is acknowledged. The approach is to use agentic workflows to automate content production and scheduling so this channel does not compete with Ahmed's limited time. Content should mirror the community positioning: practical, useful, food-business focused. Not founder content.

Platforms to build: Facebook, Instagram, YouTube Shorts. TikTok is deprioritized due to algorithm geo-weighting.

---

## Agent Workflows

Claude Code agents replace Opeclaw as the primary automation layer. All pipelines should be designed with human review preserved at trust-sensitive touchpoints — community posting and content publishing always require sign-off before going live.

### Community Monitoring Pipeline

Monitor relevant communities > qualify threads with genuine pain points > draft responses > Ahmed reviews and posts manually.

### SEO Content Pipeline

Keyword research > brief approval > draft content > human review > publish > rank tracking via Google Search Console.

### Short-Form Video Pipeline

Repurpose blog content into YouTube Shorts and Facebook Reels via FFmpeg. ElevenLabs for AI voiceover where needed.

### Social Media Pipeline

Content generation > scheduling > performance tracking. Automate as much as possible given the cold-start constraint.

The community monitoring pipeline feeds real pain-point language into SEO keyword research. This compounding loop is intentional and should be preserved as pipelines are built.

---

## Tooling

| Area | Tool |
|---|---|
| App builder | Lovable |
| Agent workflows | Claude Code agents |
| Analytics | PostHog |
| SEO tracking | Google Search Console, Ahrefs (occasional) |
| Video production | FFmpeg, CapCut / DaVinci Resolve, ElevenLabs |
| Competitors tracked | MarketMan, Reciprofity, Supy, Meez |

---

## Core Principles

**Distribution beats product.** The MVP is done. A mediocre product with great distribution wins over a polished product no one finds. Do not let product work crowd out distribution work.

**One channel, one metric.** Chasing multiple strategies in parallel causes paralysis and stalls. Stay focused on signups. Evaluate new channels only when the current ones are saturated or failing.

**Community trust is the asset.** Being genuinely helpful in communities — before the product is ever mentioned — is the strategy. This takes time and cannot be shortcut.

**Systematize everything.** Ahmed works on this as a side project with constrained weekly hours. Leverage through agentic workflows and repeatable systems is the primary way to compete with larger teams.

**Human review at trust-sensitive touchpoints.** Even as automation increases, community posts and published content require Ahmed's sign-off. Automating these without review creates reputational risk.

**Simplicity is the product.** Every feature decision should ask: does this make the tool feel lighter or heavier? If heavier, the bar for inclusion is high.

---

## How to Work in This Project

Before executing any task:

1. Ask whether it moves **signups**. If not, it is low priority unless explicitly requested.
2. If it is a product task, ask whether it **unblocks conversion** or is polish.
3. If it is a content or agent task, ask whether it **feeds the distribution engine**.
4. Flag clearly if a proposed direction conflicts with the principles above.
5. When in doubt, default to **distribution over product**, **automation over manual**, and **niche over broad**.
