# Design: Migrate Notion MCP to direct API scripts

**Date:** 2026-04-21
**Status:** Approved

## Problem

The Notion MCP tools (`mcp__claude_ai_Notion__notion-search`, `notion-fetch`, etc.) consume significant token context on every agent run due to MCP tool schema loading and verbose raw API responses. This increases cost and reduces context available for actual content work.

## Goal

Replace all Notion MCP usage in agent definitions with lightweight Python scripts that call the Notion REST API directly. Agents call these scripts via Bash and read clean output — same data, far fewer tokens.

## Precedent

`scripts/fetch_notion_subreddits.py` already implements this pattern successfully and is used by `community-monitor`. This migration extends that pattern to all Notion operations.

---

## Script architecture

### Location

```
scripts/notion/
  _client.py          # shared: load_env, notion_request, extract_text_value
  query_database.py   # list/filter pages from any DB
  fetch_page.py       # get page properties + body as clean text
  create_page.py      # create a page with properties + markdown body
  update_page.py      # patch properties on an existing page
```

### Shared client (`_client.py`)

Extracted from `fetch_notion_subreddits.py`. Provides:
- `load_env()` — reads `.env` from repo root
- `notion_request(api_key, version, endpoint, method, body)` — makes authenticated HTTP requests
- `extract_text_value(prop)` — converts Notion property objects to plain Python values

All four scripts import from `_client.py`. No duplication.

### Script contracts

#### `query_database.py`
```bash
python scripts/notion/query_database.py \
  --database-id <id> \
  --filter '{"property": "Status", "select": {"equals": "Ready"}}' \
  --output pipeline/context/result.json
```
- Queries a Notion database with an optional filter
- Outputs an array of pages with clean properties (no raw Notion schema noise)
- Supports `--limit N` to cap results (default: 10)
- Exits non-zero on API error

#### `fetch_page.py`
```bash
python scripts/notion/fetch_page.py \
  --page-id <id> \
  --output pipeline/context/page.json
```
- Fetches page properties and all body blocks
- Outputs `{ "id": "...", "url": "...", "properties": {...}, "body": "plain markdown" }`
- Body is rendered as readable plain text / markdown — not raw block JSON

#### `create_page.py`
```bash
python scripts/notion/create_page.py \
  --database-id <id> \
  --properties '{"Title": "...", "Status": "Ready", "Target Keyword": "..."}' \
  --body "## Section\n\nContent here" \
  --output pipeline/context/created.json
```
- Creates a new page in the specified database
- Accepts properties as a JSON string (script maps to correct Notion property types)
- Accepts body as a markdown string (script converts to Notion blocks)
- Outputs `{ "id": "...", "url": "..." }`

#### `update_page.py`
```bash
python scripts/notion/update_page.py \
  --page-id <id> \
  --properties '{"Status": "Used"}'
```
- Patches properties on an existing page
- Outputs `{ "id": "...", "url": "...", "updated": ["Status"] }`

### Error handling

All scripts:
- Print a clear error message to stderr and exit with code 1 on any API failure
- Include the HTTP status and Notion error message in the output so agents can report it clearly
- Never silently continue on failure

---

## Agent changes

### Affected agents

| Agent | MCP tools removed | Scripts used |
|---|---|---|
| `blog-writer` | `notion-search`, `notion-fetch`, `notion-create-pages`, `notion-update-page` | `query_database.py`, `fetch_page.py`, `create_page.py`, `update_page.py` |
| `short-form-writer` | `notion-search`, `notion-fetch`, `notion-create-pages`, `notion-update-page` | `query_database.py`, `fetch_page.py`, `create_page.py`, `update_page.py` |
| `remotion-renderer` | `notion-fetch`, `notion-search`, `notion-update-page` | `query_database.py`, `fetch_page.py`, `update_page.py` |
| `topic-researcher` | `notion-create-pages` | `create_page.py` |
| `community-monitor` | `notion-search`, `notion-fetch`, `notion-update-page` | existing `fetch_notion_subreddits.py` (unchanged), `update_page.py` |

### Change pattern for each agent

1. **`tools:` frontmatter** — remove all `mcp__claude_ai_Notion__*` entries; ensure `Bash` is listed
2. **Process steps** — replace MCP tool call instructions with equivalent Bash script calls
3. **Output handling** — agents read from `--output` JSON files or stdout instead of MCP responses

### Example: blog-writer Step 1 (before → after)

**Before:**
```
Use `notion-search` to find it, then `notion-fetch` to read the full page content.
```

**After:**
```bash
python scripts/notion/query_database.py \
  --database-id a2e785711fde46e89b3ef30a7ec28c98 \
  --filter '{"property": "Status", "select": {"equals": "Ready"}}' \
  --limit 1 \
  --output pipeline/context/brief.json
```
Then read `pipeline/context/brief.json` for the brief content and page ID.

---

## What does NOT change

- `scripts/fetch_notion_subreddits.py` — already uses direct API, stays as-is
- All database IDs and data source IDs in agent definitions — unchanged
- Agent logic, writing standards, output formats — unchanged
- The Notion databases themselves — no schema changes

---

## Success criteria

- All five agents run without any Notion MCP tools in their `tools:` list
- Each agent can complete its full Notion workflow (read → write → update) using only Bash script calls
- Token usage per agent run is measurably lower (no MCP schema overhead)
