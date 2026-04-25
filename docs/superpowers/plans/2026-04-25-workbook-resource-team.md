# Workbook Resource Team Implementation Plan

> **For agentic workers:** Use this as the starting plan for a recurring spreadsheet/resource department for `Foodcosting.app`. This plan scaffolds the team and its handoffs. It does not require full automation on day one.

**Goal:** Create a reusable agent team that researches, prioritizes, designs, validates, and packages free Excel/Google Sheets resources for restaurant food costing and related workflows.

**Architecture:** A recurring department made of six specialized agents stored in `.claude/agents/`, supported by research artifacts in `research/output/` and a dedicated workbook workspace in `pipeline/workbooks/`. The first version is intentionally lightweight: role definitions, output expectations, folder structure, and handoff order come first; deeper automation can follow later.

**Tech Stack:** Claude agents (markdown), web research, local markdown specs, optional Notion/database integration later, Google Sheets/Excel export workflows later.

---

## File Structure

| Action | Path | Responsibility |
|---|---|---|
| Create | `.claude/agents/workbook-scout.md` | Researches competitor sheets, calculators, and template gaps |
| Create | `.claude/agents/workbook-opportunity-analyst.md` | Scores workbook ideas and recommends what to build next |
| Create | `.claude/agents/workbook-architect.md` | Designs workbook structure, tabs, formulas, and user flow |
| Create | `.claude/agents/workbook-copywriter.md` | Writes workbook instructions, labels, onboarding, and positioning |
| Create | `.claude/agents/workbook-qa.md` | Reviews logic, formulas, usability, and edge cases |
| Create | `.claude/agents/workbook-funnel-strategist.md` | Turns workbooks into lead magnets and app-entry funnels |
| Create | `docs/superpowers/specs/2026-04-25-workbook-agent-team-design.md` | Team design, operating model, and output contract |
| Create | `pipeline/workbooks/README.md` | Working folder guide for workbook artifacts |
| Create | `pipeline/workbooks/intake/` | Early workbook ideas and candidate briefs |
| Create | `pipeline/workbooks/queue/` | Prioritized workbook candidates ready for deeper work |
| Create | `pipeline/workbooks/specs/` | Workbook architecture outputs |
| Create | `pipeline/workbooks/copy/` | Workbook instructional copy and naming outputs |
| Create | `pipeline/workbooks/qa/` | Workbook QA reviews and release decisions |
| Create | `pipeline/workbooks/funnel/` | Packaging and free-to-paid funnel briefs |
| Create | `pipeline/workbooks/releases/` | Final release-ready workbook bundles |
| Create | `pipeline/workbooks/context/` | Temporary workbook-agent run artifacts |
| Reference | `research/output/free-food-costing-sheets-strategy.nmd` | Foundational strategy context for this department |

---

## Phase 1: Scaffold The Team

- [ ] Create the six workbook-team agent files in `.claude/agents/`
- [ ] Create the workbook team design spec in `docs/superpowers/specs/`
- [ ] Make sure each agent has a clearly bounded responsibility
- [ ] Make sure each agent names its expected inputs and outputs
- [ ] Keep the initial version file-based, not dependent on new infrastructure

---

## Phase 2: Define The Operating Loop

The team should operate as a recurring department, not a one-off project.

Recommended loop:

1. `workbook-scout`
2. `workbook-opportunity-analyst`
3. `workbook-architect`
4. `workbook-copywriter`
5. `workbook-qa`
6. `workbook-funnel-strategist`

Associated folder flow:

1. `pipeline/workbooks/intake`
2. `pipeline/workbooks/queue`
3. `pipeline/workbooks/specs`
4. `pipeline/workbooks/copy`
5. `pipeline/workbooks/qa`
6. `pipeline/workbooks/funnel`
7. `pipeline/workbooks/releases`

- [ ] Define the weekly scouting pass
- [ ] Define the scoring/prioritization pass
- [ ] Define the workbook spec and copy handoff
- [ ] Define QA gates before publication
- [ ] Define funnel packaging outputs per workbook

---

## Phase 3: Standardize Inputs And Outputs

Each workbook candidate should eventually have:

- a demand hypothesis
- a competitor snapshot
- a workbook spec
- workbook copy/instructions
- QA notes
- funnel/landing-page recommendations
- a release bundle location

- [ ] Standardize a workbook candidate brief format
- [ ] Standardize workbook spec sections
- [ ] Standardize QA checklist outputs
- [ ] Standardize funnel packaging outputs

---

## Phase 4: Future Automation

These items are intentionally deferred until the team shape is working:

- Google Sheets API creation
- Excel export generation
- Notion or database-backed workbook queue
- performance dashboarding
- automated SERP snapshots

- [ ] Add queue/database support only after the role design is stable
- [ ] Add workbook generation automation only after workbook specs are consistent
- [ ] Add analytics-driven prioritization once enough assets exist

---

## First Recommended Use

Use this team first on the spreadsheet cluster already identified in research:

1. Recipe and Menu Costing Workbook
2. Inventory and COGS Workbook
3. Food Cost Percentage Quick Sheet
4. Par Level and Order Guide Sheet
5. Yield and Edible Portion Sheet

---

## Success Criteria

The scaffold is successful when:

- the team can be run repeatedly without redefining roles each time
- workbook ideas move through a clear handoff sequence
- outputs are consistent enough for downstream building work
- the department can support both flagship sheets and smaller quick-win templates
- workbook files are easy to locate without searching across unrelated pipeline folders
