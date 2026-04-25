# Workbook Pipeline

This folder is the working area for the Workbook Resource Team.

Unlike the broader content pipeline, workbook artifacts should stay grouped by function so research, specs, QA, and packaging do not end up mixed into the global `pipeline/context` directory.

## Folder Layout

### intake

Early-stage workbook ideas and candidate briefs.

Typical contents:

- raw workbook candidate notes
- scout outputs
- early opportunity inputs

### queue

Prioritized workbook candidates that are approved for deeper work.

Typical contents:

- scored opportunities
- queued workbook candidates
- simple status handoff files

### specs

Workbook architecture outputs.

Typical contents:

- workbook specifications
- tab structures
- formula notes
- assumptions

### copy

Workbook-facing copy and instructional assets.

Typical contents:

- start-here copy
- tab instructions
- labels and warnings
- workbook naming drafts

### qa

Review outputs before release.

Typical contents:

- QA checklists
- risk notes
- release recommendations

### funnel

Packaging and growth materials for each workbook.

Typical contents:

- landing-page angle briefs
- CTA recommendations
- free-to-paid ladder notes

### releases

Final workbook packages and release-ready bundles.

Typical contents:

- final workbook package folders
- release summaries
- associated metadata

### context

Temporary or intermediate machine-readable files used during workbook-agent runs.

Typical contents:

- transient JSON
- temporary fetched source files
- run-specific artifacts that should not live at the root pipeline level

## Naming Guidance

- Keep names workbook-first, not agent-first.
- Prefer stable slugs such as `recipe-menu-costing-workbook`.
- Use dated folders only for release bundles or snapshots where timing matters.

## Intended Flow

1. `intake`
2. `queue`
3. `specs`
4. `copy`
5. `qa`
6. `funnel`
7. `releases`

