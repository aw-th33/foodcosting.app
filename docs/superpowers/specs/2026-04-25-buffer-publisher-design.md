# Buffer Publisher Agent — Design Spec

Date: 2026-04-25  
Status: Approved

---

## Overview

A new `buffer-publisher` Claude agent that bridges rendered social assets to Buffer drafts. Ahmed sets `Status = "Ready for Buffer"` on a Notion Carousel or Short-Form Script page after reviewing the rendered output. The agent picks it up, parses captions from the page body, builds a manifest, runs `create_drafts.py`, and marks the record as `"Buffered"`.

This is the final automated step in the content pipeline before Ahmed schedules posts inside Buffer.

---

## Pipeline position

```
short-form-writer / carousel-writer
        ↓
remotion-renderer  (marks Rendered, writes Output Path)
        ↓
Ahmed reviews rendered output
        ↓
Ahmed sets Status = "Ready for Buffer"
        ↓
buffer-publisher   (creates Buffer drafts, marks Buffered)
        ↓
Ahmed schedules inside Buffer
```

---

## Trigger

Ahmed manually sets `Status = "Ready for Buffer"` on a Carousel or Short-Form Script Notion page. The agent is run on demand — it does not poll automatically.

---

## Queues

The agent queries both databases in parallel:

- **Carousels** DB (`34a80496-c886-801e-89b3-d9d4901e99aa`) — filter `Status = "Ready for Buffer"`
- **Short-Form Scripts** DB (`1120f885ed6845fb9bebb8e9ec56e856`) — filter `Status = "Ready for Buffer"`

One item processed per run. If both queues have items, carousel is processed first (faster, image-only). If neither queue has items, agent reports "Nothing ready for Buffer" and stops.

---

## Status flow

```
Draft → Ready to Render → Rendered → Ready for Buffer → Buffered
                                                       → Buffer Failed
```

`Buffer Failed` is set on any error. Ahmed fixes the issue and resets to `"Ready for Buffer"` to retry.

---

## Notion schema changes

### Carousels database — new properties
| Property | Type | Written by |
|---|---|---|
| `Output Path` | Text | remotion-renderer |

New status values: `Ready for Buffer`, `Buffered`, `Buffer Failed`

### Short-Form Scripts database — new properties
| Property | Type | Written by |
|---|---|---|
| `Output Path` | Text | remotion-renderer |

New status values: `Ready for Buffer`, `Buffered`, `Buffer Failed`

---

## Agent changes to existing agents

### remotion-renderer — two additions

After rendering and marking `Status = "Rendered"`, also write `Output Path`:

- **Carousel:** `pipeline/out/YYYY-MM-DD-<slug>-carousel/` (the directory)
- **Short-form video:** `pipeline/out/YYYY-MM-DD-<slug>.mp4` (the file)

```bash
python scripts/notion/update_page.py \
  --page-id <page-id> \
  --properties '{"Status": "Rendered", "Output Path": "<path>"}'
```

### short-form-writer — add caption block to script body

After the Remotion props for each variant, append a `CAPTION:` section to `pipeline/context/script-body.md`:

```markdown
## Captions

CAPTION:
<instagram/facebook caption — 1-3 sentences, practitioner voice, ends with foodcosting.app CTA>

HASHTAGS:
#shorts #foodcost #restaurantbusiness
```

This makes the caption format identical to the carousel body, so the buffer-publisher can use the same parsing logic for both content types.

---

## buffer-publisher agent

### Step 1 — Query both queues in parallel

```bash
python scripts/notion/query_database.py \
  --database-id 34a80496-c886-801e-89b3-d9d4901e99aa \
  --filter '{"property": "Status", "select": {"equals": "Ready for Buffer"}}' \
  --sorts '[{"timestamp": "created_time", "direction": "ascending"}]' \
  --limit 1 \
  --output pipeline/context/carousel-buffer-queue.json

python scripts/notion/query_database.py \
  --database-id 1120f885ed6845fb9bebb8e9ec56e856 \
  --filter '{"property": "Status", "select": {"equals": "Ready for Buffer"}}' \
  --sorts '[{"timestamp": "created_time", "direction": "ascending"}]' \
  --limit 1 \
  --output pipeline/context/script-buffer-queue.json
```

Process carousel first if both have results. Stop if neither has results.

### Step 2 — Fetch the full page body

```bash
python scripts/notion/fetch_page.py \
  --page-id <page-id> \
  --output pipeline/context/buffer-source-page.json
```

Read `pipeline/context/buffer-source-page.json`. Extract:
- `Output Path` from properties — fail immediately if missing or empty
- Full `body` text for caption parsing

### Step 3 — Parse captions from body

Scan the body for the `CAPTION:` block:

```
CAPTION:
<text until next heading or HASHTAGS:>

HASHTAGS:
<hashtag line>
```

Rules:
- The caption text becomes `caption_base` and also `captions.facebook`
- For Instagram: append hashtags on a new line after the caption
- For YouTube (video only): append `\n\n` + hashtags after the caption
- If no `CAPTION:` block is found, set `Status = "Buffer Failed"`, report "No CAPTION block found in page body", and stop

### Step 4 — Validate Output Path and assets

For **carousels**: `Output Path` is a directory. Glob for `slide-*.png` files inside it. Fail if directory does not exist or contains no PNGs. Sort slides numerically (`slide-1.png`, `slide-2.png`, ...). Fail if fewer than 2 or more than 10 slides found.

For **short-form videos**: `Output Path` is a file path ending in `.mp4`. Fail if the file does not exist.

On any failure: set `Status = "Buffer Failed"` with a clear error message and stop.

### Step 5 — Build the manifest

Construct the manifest dict in memory, write to a temp file at `pipeline/context/buffer-manifest-temp.json`:

**Carousel manifest:**
```json
{
  "post_type": "carousel",
  "assets": ["pipeline/out/.../slide-1.png", "..."],
  "title": "<Notion page Name property>",
  "caption_base": "<parsed caption>",
  "captions": {
    "instagram": "<caption + hashtags>",
    "facebook": "<caption>"
  },
  "channels": ["instagram", "facebook"],
  "status": "ready_for_buffer"
}
```

**Video manifest:**
```json
{
  "post_type": "video",
  "assets": ["pipeline/out/.../<slug>.mp4"],
  "title": "<Notion page Title property — fall back to Name if Title is empty>",
  "caption_base": "<parsed caption>",
  "captions": {
    "instagram": "<caption> Link in bio.",
    "youtube": "<caption>\n\n<hashtags>",
    "facebook": "<caption>"
  },
  "channels": ["instagram", "youtube", "facebook"],
  "status": "ready_for_buffer"
}
```

### Step 6 — Run create_drafts.py

```bash
python scripts/buffer/create_drafts.py \
  --manifest pipeline/context/buffer-manifest-temp.json \
  --output pipeline/context/buffer-drafts-created.json \
  --force
```

`--force` is required because the temp manifest path is reused across runs.

If the script exits non-zero: set `Status = "Buffer Failed"`, surface the stderr output, and stop.

### Step 7 — Update Notion status

On success:
```bash
python scripts/notion/update_page.py \
  --page-id <page-id> \
  --properties '{"Status": "Buffered"}'
```

On failure (any step after Step 2):
```bash
python scripts/notion/update_page.py \
  --page-id <page-id> \
  --properties '{"Status": "Buffer Failed"}'
```

### Step 8 — Handoff summary

```text
## Buffer drafts created

Type: Carousel | Short-form video
Source: <Notion page URL>
Channels: instagram, facebook | instagram, youtube, facebook
Drafts: <list of Buffer draft IDs per channel>
Assets uploaded: <count>
Status: Buffered — Ahmed reviews and schedules inside Buffer
```

---

## Files created or modified

| File | Change |
|---|---|
| `.claude/agents/buffer-publisher.md` | New agent |
| `.claude/agents/remotion-renderer.md` | Write `Output Path` on render |
| `.claude/agents/short-form-writer.md` | Add `CAPTION:` block to script body |
| `pipeline/context/buffer-manifest-temp.json` | Temp file, reused per run |
| `pipeline/context/buffer-drafts-created.json` | Existing output file, reused |

No new Python scripts needed — `create_drafts.py` is used as-is.

---

## Out of scope

- Fully automated triggering (future — once system is stable)
- LinkedIn support (not in current channel setup)
- Scheduling posts inside Buffer (Ahmed does this manually)
- Writing or editing captions (caption quality is owned by the content writers)
