# Workbook Agent Team Design

**Date:** 2026-04-25
**Status:** Initial scaffold
**Approach:** Recurring department, file-based first

---

## Overview

This design defines a standing agent team for `Foodcosting.app` focused on free workbook and template products for restaurant food costing.

The team exists to create a repeatable resource engine:

- research what operators already use
- identify the best workbook opportunities
- design workbook logic and structure
- make the workbook understandable and branded
- validate quality
- package the workbook as a lead magnet and product entry point

This is a recurring department, not a one-time setup.

---

## Department Charter

The Workbook Resource Team creates free spreadsheet-based products that:

- attract relevant organic traffic
- build trust with restaurant operators
- solve real food-costing workflows
- create a natural upgrade path into `Foodcosting.app`

---

## Agent Roster

### 1. Workbook Scout

Purpose:
Research existing sheets, calculators, and template hubs. Capture what competitors offer, how they package it, and what gaps exist.

Primary output:
Competitor teardowns and workbook idea inputs.

### 2. Workbook Opportunity Analyst

Purpose:
Score workbook ideas by demand, product fit, differentiation potential, and upsell potential.

Primary output:
A prioritized recommendation for what to build next.

### 3. Workbook Architect

Purpose:
Design workbook structure, tabs, formulas, data flow, user path, and logic assumptions.

Primary output:
A workbook specification detailed enough for production.

### 4. Workbook Copywriter

Purpose:
Write the workbook's instructional text, onboarding tab content, labels, positioning copy, and user-facing guidance.

Primary output:
Workbook-ready copy plus packaging guidance.

### 5. Workbook QA

Purpose:
Review formulas, flows, usability, missing cases, and breakage risk.

Primary output:
A ship/no-ship QA note with required fixes or approval.

### 6. Workbook Funnel Strategist

Purpose:
Connect each workbook to landing-page positioning, lead capture, app entry, and upgrade motions.

Primary output:
A funnel packaging brief for the workbook.

---

## Operating Loop

The team should normally run in this order:

1. Scout
2. Opportunity Analyst
3. Architect
4. Copywriter
5. QA
6. Funnel Strategist

Some loops may skip or combine roles early on, but the full system should keep these functions distinct.

---

## Storage Layout

Workbook-team artifacts should live in a dedicated workspace:

- `pipeline/workbooks/intake`
- `pipeline/workbooks/queue`
- `pipeline/workbooks/specs`
- `pipeline/workbooks/copy`
- `pipeline/workbooks/qa`
- `pipeline/workbooks/funnel`
- `pipeline/workbooks/releases`
- `pipeline/workbooks/context`

This keeps workbook operations separate from the general content pipeline and avoids dumping workbook artifacts into the shared `pipeline/context` directory.

### Folder Responsibilities

`intake`
Candidate briefs, scouting notes, and early workbook idea inputs.

`queue`
Prioritized workbook opportunities that are approved for deeper work.

`specs`
Workbook architecture and structure outputs.

`copy`
Workbook instructional copy and in-sheet text.

`qa`
Quality reviews, findings, and release recommendations.

`funnel`
Landing-page angle, CTA, and upgrade-path briefs.

`releases`
Final release-ready workbook bundles.

`context`
Temporary or run-specific workbook agent artifacts.

---

## Output Contract

Each workbook candidate should be able to produce these six artifacts:

1. Research note
2. Opportunity score
3. Workbook spec
4. Workbook copy pack
5. QA review
6. Funnel brief

---

## Scope Boundaries

This team is responsible for:

- spreadsheet and workbook concepts
- free template strategy
- workbook UX and logic
- landing-page and funnel packaging guidance

This team is not directly responsible for:

- app feature development
- payment or billing systems
- final web implementation of marketing pages
- enterprise sales workflows

---

## Recommended Initial Cadence

- Weekly: scouting and idea intake
- Biweekly: one workbook spec or one workbook release candidate
- Monthly: review traction and reprioritize backlog
- Quarterly: refresh cluster strategy and retire weak concepts

---

## Prioritization Heuristic

Workbook ideas should be judged using:

- search/demand signal
- prevalence among competitors
- clarity of user pain
- build effort
- differentiation potential
- fit with `Foodcosting.app`
- natural free-to-paid upgrade path

---

## Design Principles

- Google Sheets first, Excel compatible where practical
- Real operator workflows over generic spreadsheet aesthetics
- Clear onboarding tab or start-here layer
- Protected formulas and guided inputs where possible
- Free version must be genuinely useful
- Upsell only where spreadsheet pain naturally appears

---

## Initial Backlog Focus

The first workbook cluster should likely include:

1. Recipe and Menu Costing Workbook
2. Inventory and COGS Workbook
3. Food Cost Percentage Quick Sheet
4. Par Level and Order Guide Sheet
5. Yield and Edible Portion Sheet

---

## Shared Context

Foundational research currently lives here:

- `research/output/free-food-costing-sheets-strategy.nmd`

That note should be treated as a required context artifact for this team until a fuller workbook knowledge base exists.
