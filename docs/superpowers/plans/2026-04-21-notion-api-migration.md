# Notion API Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all Notion MCP tool usage across 5 agent definitions with direct Notion REST API calls via Python scripts, reducing token consumption per agent run.

**Architecture:** A shared `_client.py` module provides auth and HTTP helpers; four focused scripts (`query_database.py`, `fetch_page.py`, `create_page.py`, `update_page.py`) handle all Notion operations. Agents call these via Bash and read clean JSON output. Five agent `.md` files are updated to remove MCP tools and use the new scripts.

**Tech Stack:** Python 3 stdlib only (urllib, json, argparse, pathlib) — no new dependencies. Notion REST API v2026-03-11.

---

## File map

**Create:**
- `scripts/notion/_client.py` — shared auth, HTTP, property parsing
- `scripts/notion/query_database.py` — filter pages from a DB
- `scripts/notion/fetch_page.py` — get page properties + body as markdown
- `scripts/notion/create_page.py` — create page with properties + body
- `scripts/notion/update_page.py` — patch page properties

**Modify:**
- `.claude/agents/blog-writer.md`
- `.claude/agents/short-form-writer.md`
- `.claude/agents/remotion-renderer.md`
- `.claude/agents/topic-researcher.md`
- `.claude/agents/community-monitor.md`

---

### Task 1: Create `scripts/notion/_client.py`

**Files:**
- Create: `scripts/notion/_client.py`

- [ ] **Step 1: Create the file**

```python
"""
Shared Notion API client utilities.
Extracted from scripts/fetch_notion_subreddits.py — same pattern, reusable.

Environment variables required:
    NOTION_API_KEY      - required
    NOTION_VERSION      - optional, default 2026-03-11
"""

import os
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def load_env():
    """Load .env from repo root into os.environ (skip already-set vars)."""
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key and value and key not in os.environ:
                os.environ[key] = value


def get_auth():
    """Return (api_key, api_version) from environment. Exits on missing key."""
    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        print("ERROR: NOTION_API_KEY is not set", file=sys.stderr)
        sys.exit(1)
    api_version = os.environ.get("NOTION_VERSION", "2026-03-11")
    return api_key, api_version


def notion_request(api_key, api_version, endpoint, method="GET", body=None):
    """Make an authenticated Notion API request. Raises RuntimeError on HTTP error."""
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": api_version,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"Notion API {method} /{endpoint}: HTTP {e.code} — {error_body}") from e


def extract_property(prop):
    """Convert a Notion property object to a plain Python value."""
    if not prop:
        return None
    ptype = prop.get("type", "")
    if ptype == "title":
        items = prop.get("title", [])
        return "".join(item.get("plain_text", "") for item in items)
    elif ptype == "rich_text":
        items = prop.get("rich_text", [])
        return "".join(item.get("plain_text", "") for item in items)
    elif ptype == "select":
        sel = prop.get("select")
        return sel.get("name") if sel else None
    elif ptype == "multi_select":
        return [item.get("name") for item in prop.get("multi_select", [])]
    elif ptype == "number":
        return prop.get("number")
    elif ptype == "url":
        return prop.get("url")
    elif ptype == "date":
        d = prop.get("date")
        return d.get("start") if d else None
    elif ptype == "checkbox":
        return prop.get("checkbox")
    elif ptype == "files":
        files = prop.get("files", [])
        urls = []
        for f in files:
            if f.get("type") == "external":
                urls.append(f["external"]["url"])
            elif f.get("type") == "file":
                urls.append(f["file"]["url"])
        return urls[0] if len(urls) == 1 else urls
    return None


def clean_properties(raw_props):
    """Convert all raw Notion properties to a plain dict."""
    return {key: extract_property(val) for key, val in raw_props.items()}


def blocks_to_markdown(blocks):
    """Convert a list of Notion block objects to readable markdown text."""
    lines = []
    for block in blocks:
        btype = block.get("type", "")
        content = block.get(btype, {})
        rich = content.get("rich_text", [])
        text = "".join(r.get("plain_text", "") for r in rich)

        if btype == "heading_1":
            lines.append(f"# {text}")
        elif btype == "heading_2":
            lines.append(f"## {text}")
        elif btype == "heading_3":
            lines.append(f"### {text}")
        elif btype == "paragraph":
            lines.append(text if text else "")
        elif btype == "bulleted_list_item":
            lines.append(f"- {text}")
        elif btype == "numbered_list_item":
            lines.append(f"1. {text}")
        elif btype == "code":
            lang = content.get("language", "")
            lines.append(f"```{lang}\n{text}\n```")
        elif btype == "quote":
            lines.append(f"> {text}")
        elif btype == "divider":
            lines.append("---")
        elif btype == "callout":
            emoji = content.get("icon", {}).get("emoji", "💡")
            lines.append(f"> {emoji} {text}")
        elif btype == "toggle":
            lines.append(f"<details><summary>{text}</summary></details>")
        # unsupported block types are skipped silently
    return "\n\n".join(line for line in lines if line is not None)


def write_output(data, output_path=None):
    """Write JSON to a file or print to stdout."""
    serialized = json.dumps(data, indent=2, ensure_ascii=False)
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(serialized, encoding="utf-8")
        print(f"Written to {output_path}", file=sys.stderr)
    else:
        print(serialized)
```

- [ ] **Step 2: Verify the file exists**

```bash
python -c "import sys; sys.path.insert(0, 'scripts/notion'); import _client; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add scripts/notion/_client.py
git commit -m "feat: add shared Notion API client module"
```

---

### Task 2: Create `scripts/notion/query_database.py`

**Files:**
- Create: `scripts/notion/query_database.py`

- [ ] **Step 1: Create the file**

```python
"""
Query a Notion database and output clean page summaries.

Usage:
    python scripts/notion/query_database.py \\
        --database-id <id> \\
        --filter '{"property": "Status", "select": {"equals": "Ready"}}' \\
        --limit 10 \\
        --output pipeline/context/result.json

Output (stdout or file):
    [
      {
        "id": "page-id",
        "url": "https://notion.so/...",
        "properties": { "Title": "...", "Status": "Ready", ... }
      },
      ...
    ]
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _client import load_env, get_auth, notion_request, clean_properties, write_output


def query_database(api_key, api_version, database_id, filter_body=None, limit=10):
    body = {"page_size": min(limit, 100)}
    if filter_body:
        body["filter"] = filter_body

    try:
        result = notion_request(api_key, api_version, f"databases/{database_id}/query", method="POST", body=body)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    pages = result.get("results", [])[:limit]
    output = []
    for page in pages:
        output.append({
            "id": page["id"],
            "url": page.get("url", ""),
            "properties": clean_properties(page.get("properties", {})),
        })
    return output


def main():
    parser = argparse.ArgumentParser(description="Query a Notion database")
    parser.add_argument("--database-id", required=True, help="Notion database ID")
    parser.add_argument("--filter", dest="filter_json", default=None, help="Filter as JSON string")
    parser.add_argument("--limit", type=int, default=10, help="Max pages to return (default 10)")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    load_env()
    api_key, api_version = get_auth()

    filter_body = None
    if args.filter_json:
        try:
            filter_body = json.loads(args.filter_json)
        except json.JSONDecodeError as e:
            print(f"ERROR: invalid --filter JSON: {e}", file=sys.stderr)
            sys.exit(1)

    pages = query_database(api_key, api_version, args.database_id, filter_body, args.limit)
    write_output(pages, args.output)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-test the import**

```bash
python -c "import sys; sys.path.insert(0, 'scripts/notion'); import query_database; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add scripts/notion/query_database.py
git commit -m "feat: add notion query_database script"
```

---

### Task 3: Create `scripts/notion/fetch_page.py`

**Files:**
- Create: `scripts/notion/fetch_page.py`

- [ ] **Step 1: Create the file**

```python
"""
Fetch a Notion page's properties and body blocks as clean markdown.

Usage:
    python scripts/notion/fetch_page.py \\
        --page-id <id> \\
        --output pipeline/context/page.json

Output (stdout or file):
    {
      "id": "page-id",
      "url": "https://notion.so/...",
      "properties": { "Title": "...", "Status": "...", ... },
      "body": "## Heading\\n\\nParagraph text..."
    }
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _client import load_env, get_auth, notion_request, clean_properties, blocks_to_markdown, write_output


def fetch_page(api_key, api_version, page_id):
    try:
        page = notion_request(api_key, api_version, f"pages/{page_id}")
    except RuntimeError as e:
        print(f"ERROR fetching page: {e}", file=sys.stderr)
        sys.exit(1)

    # Fetch all body blocks (handles pagination)
    blocks = []
    cursor = None
    while True:
        endpoint = f"blocks/{page_id}/children"
        if cursor:
            endpoint += f"?start_cursor={cursor}"
        try:
            result = notion_request(api_key, api_version, endpoint)
        except RuntimeError as e:
            print(f"ERROR fetching blocks: {e}", file=sys.stderr)
            sys.exit(1)
        blocks.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")

    return {
        "id": page["id"],
        "url": page.get("url", ""),
        "properties": clean_properties(page.get("properties", {})),
        "body": blocks_to_markdown(blocks),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch a Notion page as clean JSON")
    parser.add_argument("--page-id", required=True, help="Notion page ID")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    load_env()
    api_key, api_version = get_auth()

    page = fetch_page(api_key, api_version, args.page_id)
    write_output(page, args.output)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-test the import**

```bash
python -c "import sys; sys.path.insert(0, 'scripts/notion'); import fetch_page; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add scripts/notion/fetch_page.py
git commit -m "feat: add notion fetch_page script"
```

---

### Task 4: Create `scripts/notion/create_page.py`

**Files:**
- Create: `scripts/notion/create_page.py`

- [ ] **Step 1: Create the file**

```python
"""
Create a new Notion page in a database with properties and a markdown body.

Usage:
    python scripts/notion/create_page.py \\
        --database-id <id> \\
        --properties '{"Title": "My Post", "Status": "Ready"}' \\
        --body "## Intro\\n\\nContent here." \\
        --output pipeline/context/created.json

Output (stdout or file):
    { "id": "new-page-id", "url": "https://notion.so/..." }

Supported property types (auto-detected by name convention in the DB):
    Title field     -> title
    All others      -> rich_text, select, number, url, date, checkbox
    The script fetches the DB schema first to map property types correctly.
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _client import load_env, get_auth, notion_request, write_output


def get_db_schema(api_key, api_version, database_id):
    """Fetch DB schema to know each property's type."""
    try:
        db = notion_request(api_key, api_version, f"databases/{database_id}")
    except RuntimeError as e:
        print(f"ERROR fetching database schema: {e}", file=sys.stderr)
        sys.exit(1)
    return db.get("properties", {})


def build_property_value(name, value, schema):
    """Convert a plain Python value to a Notion property payload using the DB schema."""
    prop_schema = schema.get(name, {})
    ptype = prop_schema.get("type", "rich_text")

    if ptype == "title":
        return {"title": [{"text": {"content": str(value)}}]}
    elif ptype == "rich_text":
        return {"rich_text": [{"text": {"content": str(value)}}]}
    elif ptype == "select":
        return {"select": {"name": str(value)}}
    elif ptype == "multi_select":
        items = value if isinstance(value, list) else [value]
        return {"multi_select": [{"name": str(v)} for v in items]}
    elif ptype == "number":
        return {"number": float(value) if value is not None else None}
    elif ptype == "url":
        return {"url": str(value)}
    elif ptype == "date":
        return {"date": {"start": str(value)}}
    elif ptype == "checkbox":
        return {"checkbox": bool(value)}
    elif ptype == "files":
        url = str(value)
        return {"files": [{"name": url.split("/")[-1], "type": "external", "external": {"url": url}}]}
    else:
        # fallback: rich_text
        return {"rich_text": [{"text": {"content": str(value)}}]}


def markdown_to_blocks(markdown_text):
    """Convert a markdown string to Notion block objects (subset of block types)."""
    blocks = []
    lines = markdown_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # Code fences
        if line.startswith("```"):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": "\n".join(code_lines)}}],
                    "language": lang or "plain text",
                },
            })
        elif line.startswith("### "):
            blocks.append({"object": "block", "type": "heading_3",
                           "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}})
        elif line.startswith("## "):
            blocks.append({"object": "block", "type": "heading_2",
                           "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}})
        elif line.startswith("# "):
            blocks.append({"object": "block", "type": "heading_1",
                           "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}})
        elif line.startswith("- "):
            blocks.append({"object": "block", "type": "bulleted_list_item",
                           "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}})
        elif line.startswith("1. ") or (len(line) > 2 and line[0].isdigit() and line[1] == "."):
            text = line.split(". ", 1)[1] if ". " in line else line
            blocks.append({"object": "block", "type": "numbered_list_item",
                           "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}})
        elif line.startswith("> "):
            blocks.append({"object": "block", "type": "quote",
                           "quote": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}})
        elif line.strip() == "---":
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        elif line.strip() == "":
            pass  # skip blank lines
        else:
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}})
        i += 1

    return blocks


def create_page(api_key, api_version, database_id, properties_dict, body_markdown=None):
    schema = get_db_schema(api_key, api_version, database_id)

    notion_properties = {}
    for name, value in properties_dict.items():
        if value is None:
            continue
        notion_properties[name] = build_property_value(name, value, schema)

    payload = {
        "parent": {"database_id": database_id},
        "properties": notion_properties,
    }

    if body_markdown:
        payload["children"] = markdown_to_blocks(body_markdown)

    try:
        result = notion_request(api_key, api_version, "pages", method="POST", body=payload)
    except RuntimeError as e:
        print(f"ERROR creating page: {e}", file=sys.stderr)
        sys.exit(1)

    return {"id": result["id"], "url": result.get("url", "")}


def main():
    parser = argparse.ArgumentParser(description="Create a Notion page in a database")
    parser.add_argument("--database-id", required=True)
    parser.add_argument("--properties", required=True, help="Properties as JSON string")
    parser.add_argument("--body", default=None, help="Page body as markdown string")
    parser.add_argument("--body-file", default=None, help="Read body from a file instead of --body")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    load_env()
    api_key, api_version = get_auth()

    try:
        properties_dict = json.loads(args.properties)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid --properties JSON: {e}", file=sys.stderr)
        sys.exit(1)

    body = args.body
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    if body:
        body = body.replace("\\n", "\n")

    result = create_page(api_key, api_version, args.database_id, properties_dict, body)
    write_output(result, args.output)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-test the import**

```bash
python -c "import sys; sys.path.insert(0, 'scripts/notion'); import create_page; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add scripts/notion/create_page.py
git commit -m "feat: add notion create_page script"
```

---

### Task 5: Create `scripts/notion/update_page.py`

**Files:**
- Create: `scripts/notion/update_page.py`

- [ ] **Step 1: Create the file**

```python
"""
Update properties on an existing Notion page.

Usage:
    python scripts/notion/update_page.py \\
        --page-id <id> \\
        --properties '{"Status": "Used"}'

Output (stdout):
    { "id": "...", "url": "...", "updated": ["Status"] }

The script fetches the page's parent database schema to map property types correctly.
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _client import load_env, get_auth, notion_request, write_output
from create_page import get_db_schema, build_property_value


def get_page_db_id(api_key, api_version, page_id):
    """Fetch the page to find its parent database ID."""
    try:
        page = notion_request(api_key, api_version, f"pages/{page_id}")
    except RuntimeError as e:
        print(f"ERROR fetching page: {e}", file=sys.stderr)
        sys.exit(1)
    parent = page.get("parent", {})
    if parent.get("type") != "database_id":
        print("ERROR: page is not in a database — cannot resolve property types", file=sys.stderr)
        sys.exit(1)
    return parent["database_id"]


def update_page(api_key, api_version, page_id, properties_dict):
    db_id = get_page_db_id(api_key, api_version, page_id)
    schema = get_db_schema(api_key, api_version, db_id)

    notion_properties = {}
    for name, value in properties_dict.items():
        notion_properties[name] = build_property_value(name, value, schema)

    try:
        result = notion_request(api_key, api_version, f"pages/{page_id}", method="PATCH",
                                body={"properties": notion_properties})
    except RuntimeError as e:
        print(f"ERROR updating page: {e}", file=sys.stderr)
        sys.exit(1)

    return {
        "id": result["id"],
        "url": result.get("url", ""),
        "updated": list(properties_dict.keys()),
    }


def main():
    parser = argparse.ArgumentParser(description="Update properties on a Notion page")
    parser.add_argument("--page-id", required=True)
    parser.add_argument("--properties", required=True, help="Properties to update as JSON string")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    load_env()
    api_key, api_version = get_auth()

    try:
        properties_dict = json.loads(args.properties)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid --properties JSON: {e}", file=sys.stderr)
        sys.exit(1)

    result = update_page(api_key, api_version, args.page_id, properties_dict)
    write_output(result, args.output)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-test the import**

```bash
python -c "import sys; sys.path.insert(0, 'scripts/notion'); import update_page; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add scripts/notion/update_page.py
git commit -m "feat: add notion update_page script"
```

---

### Task 6: Update `blog-writer` agent

**Files:**
- Modify: `.claude/agents/blog-writer.md`

The blog-writer uses Notion for: (1) find latest Ready brief, (2) create blog page, (3) mark brief as Used.

- [ ] **Step 1: Update the `tools:` frontmatter**

Change line 4 from:
```
tools: Bash, Read, Write, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page
```
To:
```
tools: Bash, Read, Write
```

- [ ] **Step 2: Replace Step 1 (Find the latest brief)**

Find this block in the agent file:
```
### Step 1 — Find the latest brief

Search the **Content Briefs** database (ID: `a2e785711fde46e89b3ef30a7ec28c98`) for the most recent page with Status = `Ready`.

Use `notion-search` to find it, then `notion-fetch` to read the full page content including the brief body. Record the brief's page ID — you will need it to mark it as Used after publishing.
```

Replace with:
```
### Step 1 — Find the latest brief

Query the **Content Briefs** database for the most recent page with Status = `Ready`:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/query_database.py \
  --database-id a2e785711fde46e89b3ef30a7ec28c98 \
  --filter '{"property": "Status", "select": {"equals": "Ready"}}' \
  --limit 1 \
  --output pipeline/context/brief-list.json
```

Read `pipeline/context/brief-list.json`. Take the first result — record its `id` as the brief page ID.

Then fetch the full page content including the brief body:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/fetch_page.py \
  --page-id <brief-page-id> \
  --output pipeline/context/brief.json
```

Read `pipeline/context/brief.json`. The `body` field contains the full brief text. The `properties` field contains the keyword, segment, and other metadata.
```

- [ ] **Step 3: Replace Step 4 (Publish to Notion)**

Find this instruction block:
```
Create a new page in the **Blog** database using the `notion-create-pages` tool.
```

Replace the entire Step 4 tool-call instruction paragraph with:

```
Create a new page in the **Blog** database:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/create_page.py \
  --database-id 2e880496-c886-80c7-9396-db6073f91041 \
  --properties '{
    "Title": "<post title>",
    "Status": "Review",
    "Target Keyword": "<primary keyword>",
    "Pillar": "<pillar>",
    "Slug": "<url-slug>",
    "Word Count": <word count as integer>,
    "cover": "<CLOUDINARY_URL>"
  }' \
  --body-file pipeline/context/blog-body.md \
  --output pipeline/context/blog-created.json
```

Before running, write the full blog post body to `pipeline/context/blog-body.md` using the Write tool. Then run the script. Read `pipeline/context/blog-created.json` for the new page `id` and `url`.

**Note:** Remove the instruction to fetch `notion://docs/enhanced-markdown-spec` — that was MCP-specific. Write the body as standard markdown; the script converts it to Notion blocks.
```

- [ ] **Step 4: Replace Step 5 (Mark brief as Used)**

Find:
```
Use `notion-update-page` with the brief's page ID.
```

Replace with:
```
```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <brief-page-id> \
  --properties '{"Status": "Used"}'
```
```

- [ ] **Step 5: Commit**

```bash
git add .claude/agents/blog-writer.md
git commit -m "feat: migrate blog-writer agent from Notion MCP to API scripts"
```

---

### Task 7: Update `topic-researcher` agent

**Files:**
- Modify: `.claude/agents/topic-researcher.md`

The topic-researcher only uses Notion for one operation: create a new brief page.

- [ ] **Step 1: Update the `tools:` frontmatter**

Change line 4 from:
```
tools: Bash, Read, mcp__claude_ai_Notion__notion-create-pages
```
To:
```
tools: Bash, Read
```

- [ ] **Step 2: Replace Step 4 (Publish the brief to Notion)**

Find:
```
Create a new page in the **Content Briefs** database using the `notion-create-pages` tool.
```

Replace the entire tool-call instruction with:

```
Write the full brief body to a temp file, then create the page:

```bash
# First write the body to a temp file (use the Write tool to create this file):
# pipeline/context/brief-body.md

cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/create_page.py \
  --database-id a2e785711fde46e89b3ef30a7ec28c98 \
  --properties '{
    "Title": "<topic title>",
    "Status": "Ready",
    "Target Keyword": "<primary keyword>",
    "Supporting Keywords": "<comma-separated keywords>",
    "Search Intent": "<informational|transactional|navigational>",
    "Audience Segment": "<restaurant|food truck|caterer|home baker>",
    "Suggested Angle": "<angle paragraph>",
    "Outline": "<bullet outline as single text block>",
    "CTA Recommendation": "<cta text>",
    "GSC Position": <position number>,
    "GSC Impressions": <impressions number>,
    "Opportunity Type": "<quick_win|high_impression_low_ctr|low_hanging>",
    "Created Date": "<YYYY-MM-DD>"
  }' \
  --body-file pipeline/context/brief-body.md \
  --output pipeline/context/brief-created.json
```

Read `pipeline/context/brief-created.json` for the new page `url` and output it.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/topic-researcher.md
git commit -m "feat: migrate topic-researcher agent from Notion MCP to API scripts"
```

---

### Task 8: Update `short-form-writer` agent

**Files:**
- Modify: `.claude/agents/short-form-writer.md`

Uses Notion for: (1) find latest Review blog post, (2) create script page, (3) update blog post status.

- [ ] **Step 1: Update the `tools:` frontmatter**

Change line 4 from:
```
tools: Bash, Read, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page
```
To:
```
tools: Bash, Read, Write
```

- [ ] **Step 2: Replace Step 1 (Read the blog post from Notion)**

Find:
```
Search the **Blog** database (ID: `2e880496-c886-80c7-9396-db6073f91041`) for the most recent page with Status = `Review`.

Use `notion-search` to find it, then `notion-fetch` to read the full page content. The handoff note from the blog writer (hook angles, keyword, word count) will be at the bottom of the page body.

Record the blog post's page ID — you will need it to update its status after the script is saved.
```

Replace with:
```
Query the **Blog** database for the most recent page with Status = `Review`:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/query_database.py \
  --database-id 2e880496-c886-80c7-9396-db6073f91041 \
  --filter '{"property": "Status", "select": {"equals": "Review"}}' \
  --limit 1 \
  --output pipeline/context/blog-list.json
```

Read `pipeline/context/blog-list.json`. Take the first result — record its `id` as the blog post page ID.

Then fetch the full page content:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/fetch_page.py \
  --page-id <blog-page-id> \
  --output pipeline/context/blog-post.json
```

Read `pipeline/context/blog-post.json`. The `body` field contains the full post text including the handoff note at the bottom.
```

- [ ] **Step 3: Replace Step 5 (Save the script to Notion)**

Find:
```
Create a new page in the **Short-Form Scripts** database using the `notion-create-pages` tool.
```

Replace the entire tool-call instruction with:

```
Write the full script body to a temp file, then create the page:

```bash
# Write the script body to pipeline/context/script-body.md using the Write tool first.

cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/create_page.py \
  --database-id 1120f885ed6845fb9bebb8e9ec56e856 \
  --properties '{
    "Title": "<slug-topic-YYYY-MM-DD>",
    "Status": "Draft",
    "Recommended Variant": "<A|B>",
    "Hook": "<hook text max 8 words>",
    "Problem": "<problem text max 12 words>",
    "Tip Lines": "<tipLines array as JSON string>",
    "CTA": "<cta text>",
    "Duration Frames": <durationInFrames integer>,
    "Created Date": "<YYYY-MM-DD>"
  }' \
  --body-file pipeline/context/script-body.md \
  --output pipeline/context/script-created.json
```

Read `pipeline/context/script-created.json` for the new page `url`.
```

- [ ] **Step 4: Replace Step 6 (Update blog post status)**

Find:
```
Use `notion-update-page` with the blog post's page ID.
```

Replace with:
```
```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <blog-page-id> \
  --properties '{"Status": "Script Ready"}'
```
```

- [ ] **Step 5: Commit**

```bash
git add .claude/agents/short-form-writer.md
git commit -m "feat: migrate short-form-writer agent from Notion MCP to API scripts"
```

---

### Task 9: Update `remotion-renderer` agent

**Files:**
- Modify: `.claude/agents/remotion-renderer.md`

Uses Notion for: (1) find latest Draft script, (2) mark script as Rendered.

- [ ] **Step 1: Update the `tools:` frontmatter**

Change line 4 from:
```
tools: Bash, Read, Write, Edit, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-update-page
```
To:
```
tools: Bash, Read, Write, Edit
```

- [ ] **Step 2: Replace Step 1 (Find the latest short-form script)**

Find:
```
Search the **Short-Form Scripts** database (ID: `1120f885ed6845fb9bebb8e9ec56e856`) for the most recent page with Status = `Draft`.

Use `notion-search` to find it, then `notion-fetch` to read the full page content.
```

Replace with:
```
Query the **Short-Form Scripts** database for the most recent page with Status = `Draft`:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/query_database.py \
  --database-id 1120f885ed6845fb9bebb8e9ec56e856 \
  --filter '{"property": "Status", "select": {"equals": "Draft"}}' \
  --limit 1 \
  --output pipeline/context/script-list.json
```

Read `pipeline/context/script-list.json`. Take the first result — record its `id` and check the `Recommended Variant` property.

Then fetch the full page content:

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/fetch_page.py \
  --page-id <script-page-id> \
  --output pipeline/context/script.json
```

Read `pipeline/context/script.json`. The `body` field contains the full script text with the Remotion props JSON blocks.
```

- [ ] **Step 3: Replace Step 6 (Mark script as Rendered)**

Find:
```
Use `notion-update-page` with the script page's ID.
```

Replace with:
```
```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python scripts/notion/update_page.py \
  --page-id <script-page-id> \
  --properties '{"Status": "Rendered"}'
```
```

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/remotion-renderer.md
git commit -m "feat: migrate remotion-renderer agent from Notion MCP to API scripts"
```

---

### Task 10: Update `community-monitor` agent

**Files:**
- Modify: `.claude/agents/community-monitor.md`

The community-monitor already uses `scripts/fetch_notion_subreddits.py` for all reads (Step 1). Only the optional status update path (if any) would use `notion-update-page`. Looking at the agent, there is no explicit status update step — the agent only reads and reports. Remove MCP tools from frontmatter only.

- [ ] **Step 1: Update the `tools:` frontmatter**

Change line 4 from:
```
tools: Bash, Read, Write, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-update-page
```
To:
```
tools: Bash, Read, Write
```

- [ ] **Step 2: Verify Step 1 still references the existing script**

Confirm the agent body still says:
```
python scripts/fetch_notion_subreddits.py
```
This script is unchanged — no edits needed to the step content.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/community-monitor.md
git commit -m "feat: remove Notion MCP tools from community-monitor (reads already use direct API script)"
```

---

### Task 11: End-to-end smoke test

- [ ] **Step 1: Verify all four scripts import cleanly**

```bash
cd "c:/Users/admin/Documents/Foodcosting.app" && \
  python -c "
import sys
sys.path.insert(0, 'scripts/notion')
import _client, query_database, fetch_page, create_page, update_page
print('All scripts import OK')
"
```

Expected: `All scripts import OK`

- [ ] **Step 2: Verify no agent file still references Notion MCP tools**

```bash
grep -r "mcp__claude_ai_Notion" .claude/agents/
```

Expected: no output (zero matches).

- [ ] **Step 3: Verify all agent frontmatter has Bash in tools list**

```bash
grep -A2 "^tools:" .claude/agents/*.md
```

Expected: every agent shows `Bash` in its tools line, no `mcp__claude_ai_Notion__` entries.

- [ ] **Step 4: Final commit**

```bash
git add .
git commit -m "chore: verify Notion MCP migration complete — all agents use direct API scripts"
```
