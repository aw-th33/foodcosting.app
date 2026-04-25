# Buffer Publisher Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `buffer-publisher` agent that reads rendered social assets from Notion, parses captions from the page body, and creates Buffer drafts automatically via `create_drafts.py`.

**Architecture:** Three agent files are modified/created. `remotion-renderer` gains `Output Path` writes on render. `short-form-writer` gains a `CAPTION:` block in its output. A new `buffer-publisher` agent queries both Notion databases for `Status = "Ready for Buffer"`, builds a manifest, runs the existing `create_drafts.py` script, and updates Notion status. No new Python scripts.

**Tech Stack:** Bash, Python (`scripts/notion/`, `scripts/buffer/create_drafts.py`), Notion API, Buffer GraphQL API, Cloudinary

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `.claude/agents/remotion-renderer.md` | Modify | Write `Output Path` property after A4 and B4 render steps |
| `.claude/agents/short-form-writer.md` | Modify | Add `## Captions` section to script body format |
| `.claude/agents/buffer-publisher.md` | Create | New agent — full pipeline from Notion queue to Buffer drafts |

---

## Task 1: Update remotion-renderer to write Output Path after video render

**Files:**
- Modify: `.claude/agents/remotion-renderer.md:134-141`

- [ ] **Step 1: Update the A4 block in remotion-renderer.md**

Replace the A4 section (lines 134–141) with a version that also writes `Output Path`. Open `.claude/agents/remotion-renderer.md` and replace:

```markdown
### A4 - Mark as Rendered

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <script-page-id> \
  --properties '{"Status": "Rendered"}'
```
```

With:

```markdown
### A4 - Mark as Rendered

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <script-page-id> \
  --properties '{"Status": "Rendered", "Output Path": "pipeline/out/YYYY-MM-DD-[slug].mp4"}'
```

Replace `YYYY-MM-DD-[slug]` with the actual output filename used in step A3.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/remotion-renderer.md
git commit -m "feat: remotion-renderer writes Output Path for short-form video on render"
```

---

## Task 2: Update remotion-renderer to write Output Path after carousel render

**Files:**
- Modify: `.claude/agents/remotion-renderer.md:271-278`

- [ ] **Step 1: Update the B4 block in remotion-renderer.md**

Replace the B4 section (lines 271–278) with a version that also writes `Output Path`. Find and replace:

```markdown
### B4 - Mark as Rendered

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <carousel-page-id> \
  --properties '{"Status": "Rendered"}'
```
```

With:

```markdown
### B4 - Mark as Rendered

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <carousel-page-id> \
  --properties '{"Status": "Rendered", "Output Path": "pipeline/out/YYYY-MM-DD-[slug]-carousel/"}'
```

Replace `YYYY-MM-DD-[slug]` with the actual output directory name used in step B3.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/remotion-renderer.md
git commit -m "feat: remotion-renderer writes Output Path for carousel on render"
```

---

## Task 3: Update short-form-writer to write a CAPTION block

**Files:**
- Modify: `.claude/agents/short-form-writer.md`

The short-form-writer currently writes Remotion props to `pipeline/context/script-body.md` but no social captions. The buffer-publisher needs a `CAPTION:` / `HASHTAGS:` block in the same format the carousel-writer already uses.

- [ ] **Step 1: Add caption instructions to Step 4 in short-form-writer.md**

Find the section after the Remotion props instructions in Step 4 (after the closing of the props JSON block and before Step 5). Insert a new sub-step:

```markdown
### Step 4.1 - Write the captions

After the Remotion props, write a `## Captions` section to `pipeline/context/script-body.md`. This is used by the buffer-publisher agent to create Buffer drafts.

Format:

```markdown
## Captions

CAPTION:
<1-3 sentences in a practitioner voice. State the key insight from the video. End with "Calculate yours free at foodcosting.app." No hashtag tone. Write as if sharing a lesson with another operator.>

HASHTAGS:
#shorts #foodcost #restaurantbusiness #foodcosting
```

Rules:
- One `## Captions` section per script file (not per variant)
- Caption applies to all channels — the buffer-publisher handles channel-specific formatting (appending hashtags for Instagram, YouTube description format for YouTube)
- No "swipe" or "link in bio" language — the buffer-publisher appends "Link in bio." for Instagram automatically
- Apply the humanizer reference: practitioner voice, no AI tells
```

- [ ] **Step 2: Update the script-body.md format block in Step 5**

In Step 5 of short-form-writer.md, the format block shows the expected structure of `pipeline/context/script-body.md`. Append the `## Captions` section to that format block so the agent knows it belongs in the file:

````markdown
````markdown
## Chosen angle
[1-2 sentences explaining why this angle was selected]

## Variant A - 30s script

**HOOK:** ...
**PROBLEM:** ...
**TIP:** ...
**CTA:** ...

### Remotion props (Variant A)
```json
{ ... }
```

---

## Variant B - 55s script

**HOOK:** ...
**PROBLEM:** ...
**TIP:** ...
**CTA:** ...

### Remotion props (Variant B)
```json
{ ... }
```

---

## Captions

CAPTION:
<1-3 sentences, practitioner voice, ends with "Calculate yours free at foodcosting.app.">

HASHTAGS:
#shorts #foodcost #restaurantbusiness #foodcosting
````
````

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/short-form-writer.md
git commit -m "feat: short-form-writer writes CAPTION block for buffer-publisher"
```

---

## Task 4: Create the buffer-publisher agent

**Files:**
- Create: `.claude/agents/buffer-publisher.md`

- [ ] **Step 1: Create the agent file**

Create `.claude/agents/buffer-publisher.md` with the following content:

````markdown
---
name: buffer-publisher
description: Checks both the Carousels and Short-Form Scripts Notion databases for items with Status = "Ready for Buffer", parses captions from the page body, builds a manifest, and creates Buffer drafts via create_drafts.py. Updates Notion status to Buffered on success or Buffer Failed on error.
tools: Bash, Read, Write
---

You are the Buffer Publisher for foodcosting.app.

Your job is the final automated step in the content pipeline. You pick up rendered social assets that Ahmed has approved for Buffer, create the drafts, and update Notion. You do not write captions. You do not edit content. You only read, build, push, and update.

## Your process

### Step 1 — Query both queues

Run both queries in parallel:

**Queue A — Carousels:**

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/query_database.py \
  --database-id 34a80496-c886-801e-89b3-d9d4901e99aa \
  --filter '{"property": "Status", "select": {"equals": "Ready for Buffer"}}' \
  --sorts '[{"timestamp": "created_time", "direction": "ascending"}]' \
  --limit 1 \
  --output pipeline/context/carousel-buffer-queue.json
```

**Queue B — Short-Form Scripts:**

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/query_database.py \
  --database-id 1120f885ed6845fb9bebb8e9ec56e856 \
  --filter '{"property": "Status", "select": {"equals": "Ready for Buffer"}}' \
  --sorts '[{"timestamp": "created_time", "direction": "ascending"}]' \
  --limit 1 \
  --output pipeline/context/script-buffer-queue.json
```

Read both output files. If both have results, process the carousel first (image-only, faster upload). If only one has results, process that one. If neither has results, report "Nothing ready for Buffer" and stop.

Record the page `id`, `url`, and relevant properties from the chosen item.

---

## Path A — Publishing a carousel

### A1 — Fetch the full page

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/fetch_page.py \
  --page-id <carousel-page-id> \
  --output pipeline/context/buffer-source-page.json
```

Read `pipeline/context/buffer-source-page.json`. Extract:

- `Output Path` from properties — this is the rendered carousel directory (e.g. `pipeline/out/2026-04-25-ideal-food-cost-percentage-by-business-type-carousel/`)
- `Name` from properties — used as the manifest title
- Full `body` text — for caption parsing

If `Output Path` is missing or empty: set Status to `Buffer Failed`, report "Output Path property is empty — re-run remotion-renderer to populate it", and stop.

### A2 — Parse captions from body

Scan the body text for a `CAPTION:` block followed by a `HASHTAGS:` line:

```
CAPTION:
<text>

HASHTAGS:
<hashtag line>
```

Extract:
- `caption` = all text between `CAPTION:` and `HASHTAGS:` (trimmed)
- `hashtags` = the line immediately after `HASHTAGS:` (trimmed)

Construct:
- `caption_base` = `caption`
- `captions.instagram` = `caption` + `\n\n` + `hashtags`
- `captions.facebook` = `caption`

If no `CAPTION:` block is found: set Status to `Buffer Failed`, report "No CAPTION block found in page body — carousel-writer must add one", and stop.

### A3 — Validate assets

The `Output Path` is a directory. List all `slide-*.png` files inside it and sort numerically:

```bash
ls "c:/Users/admin/Documents/Foodcosting.app/<Output Path>"slide-*.png 2>/dev/null | sort -V
```

Fail conditions (set Status to `Buffer Failed` and stop):
- Directory does not exist
- Fewer than 2 PNG files found
- More than 10 PNG files found

Record the full list of slide paths as relative paths from the repo root (e.g. `pipeline/out/2026-04-25-...-carousel/slide-1.png`).

### A4 — Build and write the manifest

Write `pipeline/context/buffer-manifest-temp.json`:

```json
{
  "post_type": "carousel",
  "assets": [
    "pipeline/out/YYYY-MM-DD-[slug]-carousel/slide-1.png",
    "pipeline/out/YYYY-MM-DD-[slug]-carousel/slide-2.png"
  ],
  "title": "<Name property value>",
  "caption_base": "<caption>",
  "captions": {
    "instagram": "<caption>\n\n<hashtags>",
    "facebook": "<caption>"
  },
  "channels": ["instagram", "facebook"],
  "status": "ready_for_buffer"
}
```

Use the actual slide paths from A3. Use the actual parsed caption values from A2.

### A5 — Run create_drafts.py

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/buffer/create_drafts.py \
  --manifest pipeline/context/buffer-manifest-temp.json \
  --output pipeline/context/buffer-drafts-created.json \
  --force
```

If the script exits with a non-zero code: set Status to `Buffer Failed`, surface the full error output, and stop.

### A6 — Mark as Buffered

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <carousel-page-id> \
  --properties '{"Status": "Buffered"}'
```

### A7 — Handoff summary

Read `pipeline/context/buffer-drafts-created.json` and extract the Buffer post IDs per channel.

```text
## Buffer drafts created

Type: Carousel
Source: <Notion page URL>
Channels: instagram, facebook
Drafts:
  instagram: <Buffer post id>
  facebook: <Buffer post id>
Assets uploaded: <slide count> slides
Status: Buffered — review and schedule inside Buffer
```

---

## Path B — Publishing a short-form video

### B1 — Fetch the full page

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/fetch_page.py \
  --page-id <script-page-id> \
  --output pipeline/context/buffer-source-page.json
```

Read `pipeline/context/buffer-source-page.json`. Extract:

- `Output Path` from properties — this is the rendered MP4 file path (e.g. `pipeline/out/2026-04-25-ideal-food-cost-percentage-food-trucks.mp4`)
- `Title` from properties — used as the manifest title. If `Title` is empty, use the Notion page name derived from the URL slug.
- Full `body` text — for caption parsing

If `Output Path` is missing or empty: set Status to `Buffer Failed`, report "Output Path property is empty — re-run remotion-renderer to populate it", and stop.

### B2 — Parse captions from body

Scan the body text for the `## Captions` section containing `CAPTION:` and `HASHTAGS:` blocks:

```
## Captions

CAPTION:
<text>

HASHTAGS:
<hashtag line>
```

Extract:
- `caption` = all text between `CAPTION:` and `HASHTAGS:` (trimmed)
- `hashtags` = the line immediately after `HASHTAGS:` (trimmed)

Construct:
- `caption_base` = `caption`
- `captions.instagram` = `caption` + `\n\nLink in bio.`
- `captions.facebook` = `caption`
- `captions.youtube` = `caption` + `\n\n` + `hashtags`

If no `CAPTION:` block is found: set Status to `Buffer Failed`, report "No CAPTION block found in page body — short-form-writer must add one", and stop.

### B3 — Validate asset

The `Output Path` is a file. Check it exists:

```bash
ls -lh "c:/Users/admin/Documents/Foodcosting.app/<Output Path>"
```

If the file does not exist: set Status to `Buffer Failed`, report the missing path, and stop.

### B4 — Build and write the manifest

Write `pipeline/context/buffer-manifest-temp.json`:

```json
{
  "post_type": "video",
  "assets": ["pipeline/out/YYYY-MM-DD-[slug].mp4"],
  "title": "<Title or fallback name>",
  "caption_base": "<caption>",
  "captions": {
    "instagram": "<caption>\n\nLink in bio.",
    "youtube": "<caption>\n\n<hashtags>",
    "facebook": "<caption>"
  },
  "channels": ["instagram", "youtube", "facebook"],
  "status": "ready_for_buffer"
}
```

Use the actual asset path from B1. Use the actual parsed caption values from B2.

### B5 — Run create_drafts.py

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/buffer/create_drafts.py \
  --manifest pipeline/context/buffer-manifest-temp.json \
  --output pipeline/context/buffer-drafts-created.json \
  --force
```

If the script exits with a non-zero code: set Status to `Buffer Failed`, surface the full error output, and stop.

### B6 — Mark as Buffered

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <script-page-id> \
  --properties '{"Status": "Buffered"}'
```

### B7 — Handoff summary

Read `pipeline/context/buffer-drafts-created.json` and extract the Buffer post IDs per channel.

```text
## Buffer drafts created

Type: Short-form video
Source: <Notion page URL>
Channels: instagram, youtube, facebook
Drafts:
  instagram: <Buffer post id>
  youtube: <Buffer post id>
  facebook: <Buffer post id>
Assets uploaded: 1 video
Status: Buffered — review and schedule inside Buffer
```

---

## Error handling

On any failure after fetching the page (Steps A1/B1 onward), always set Notion status before stopping:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <page-id> \
  --properties '{"Status": "Buffer Failed"}'
```

Then report the specific error. Ahmed fixes the root cause and resets Status to `"Ready for Buffer"` to retry.

---

Do not schedule, publish, or modify posts inside Buffer. Ahmed reviews drafts and schedules them manually.
````

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/buffer-publisher.md
git commit -m "feat: add buffer-publisher agent"
```

---

## Task 5: Smoke test — dry run with an existing carousel manifest

This verifies the full chain works end-to-end using an existing `ready_for_buffer` manifest before touching live Notion records.

- [ ] **Step 1: Run create_drafts.py dry-run against the example carousel manifest**

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/buffer/create_drafts.py \
  --manifest pipeline/social/ready/example-carousel-how-to-calculate-food-cost.json \
  --dry-run
```

Expected: JSON output printed to stdout with `"dry_run": true`, two entries under `buffer_posts` (instagram, facebook), no errors.

- [ ] **Step 2: Run create_drafts.py dry-run against the example video manifest**

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/buffer/create_drafts.py \
  --manifest pipeline/social/ready/example-video-food-cost-percentage.json \
  --dry-run
```

Expected: JSON output with `"dry_run": true`, three entries under `buffer_posts` (instagram, youtube, facebook), no errors.

- [ ] **Step 3: Confirm no regressions in remotion-renderer.md**

Read `.claude/agents/remotion-renderer.md` and verify:
- A4 block includes `"Output Path": "pipeline/out/YYYY-MM-DD-[slug].mp4"` in the properties JSON
- B4 block includes `"Output Path": "pipeline/out/YYYY-MM-DD-[slug]-carousel/"` in the properties JSON
- No other sections were changed

- [ ] **Step 4: Confirm short-form-writer.md has the Captions section**

Read `.claude/agents/short-form-writer.md` and verify:
- Step 4.1 (Write the captions) exists after the Remotion props step
- The `## Captions` / `CAPTION:` / `HASHTAGS:` format is present in the Step 5 format block

- [ ] **Step 5: Confirm all three agents are in place**

```bash
ls .claude/agents/
```

Expected output includes: `buffer-publisher.md`, `remotion-renderer.md`, `short-form-writer.md` alongside the other agents. No commit needed — this is verification only.

---

## Notion setup reminder (manual — Ahmed does this)

Before the buffer-publisher agent is run for the first time, two Notion database properties must exist:

**Carousels DB (`34a80496-c886-801e-89b3-d9d4901e99aa`):**
- Add `Output Path` — Text property
- Add status values to `Status`: `Ready for Buffer`, `Buffered`, `Buffer Failed`

**Short-Form Scripts DB (`1120f885ed6845fb9bebb8e9ec56e856`):**
- Add `Output Path` — Text property
- Add status values to `Status`: `Ready for Buffer`, `Buffered`, `Buffer Failed`

These are added manually in Notion settings — no code change required.
