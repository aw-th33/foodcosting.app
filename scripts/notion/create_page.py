"""
Create a new Notion page in a database with properties and a markdown body.

Usage:
    python scripts/notion/create_page.py \\
        --database-id <id> \\
        [--data-source-id <id>] \\
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
from _client import load_env, get_auth, notion_request, write_output, get_schema, is_data_source_api


def get_db_schema(api_key, api_version, database_id):
    """Fetch DB schema to know each property's type."""
    try:
        schema, _, _ = get_schema(api_key, api_version, database_id=database_id)
    except RuntimeError as e:
        print(f"ERROR fetching database schema: {e}", file=sys.stderr)
        sys.exit(1)
    return schema


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


def parse_inline(text):
    """Parse inline markdown (bold, italic) into Notion rich_text segments.

    Strips [INTERNAL_LINK: ...] placeholders silently.
    """
    import re
    # Remove internal link placeholders
    text = re.sub(r'\[INTERNAL_LINK:[^\]]*\]', '', text).strip()

    segments = []
    # Tokenise: **bold**, *italic*, plain
    pattern = re.compile(r'(\*\*(.+?)\*\*|\*(.+?)\*)')
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            segments.append({"type": "text", "text": {"content": text[last:m.start()]}})
        if m.group(0).startswith('**'):
            segments.append({
                "type": "text",
                "text": {"content": m.group(2)},
                "annotations": {"bold": True},
            })
        else:
            segments.append({
                "type": "text",
                "text": {"content": m.group(3)},
                "annotations": {"italic": True},
            })
        last = m.end()
    if last < len(text):
        segments.append({"type": "text", "text": {"content": text[last:]}})
    return segments if segments else [{"type": "text", "text": {"content": text}}]


_CALLOUT_COLOR_MAP = {
    "red_bg": "red_background",
    "yellow_bg": "yellow_background",
    "green_bg": "green_background",
    "blue_bg": "blue_background",
    "gray_bg": "gray_background",
    "purple_bg": "purple_background",
    "pink_bg": "pink_background",
    "brown_bg": "brown_background",
    "orange_bg": "orange_background",
}


def _parse_callout_open(line):
    """Return (icon, color) if line is a <callout ...> opening tag, else None."""
    import re
    m = re.match(r'\s*<callout([^>]*)>', line, re.IGNORECASE)
    if not m:
        return None
    attrs = m.group(1)
    icon_m = re.search(r'icon=["\']([^"\']+)["\']', attrs)
    color_m = re.search(r'color=["\']([^"\']+)["\']', attrs)
    icon = icon_m.group(1) if icon_m else "💡"
    raw_color = color_m.group(1) if color_m else "gray_background"
    color = _CALLOUT_COLOR_MAP.get(raw_color, raw_color)
    return icon, color


def markdown_to_blocks(markdown_text):
    """Convert a markdown string to Notion block objects.

    Handles standard markdown (headings, lists, code fences, blockquotes,
    dividers) plus custom blog syntax: <callout>, <table>, <details>.
    Inline bold/italic and [INTERNAL_LINK:] placeholders are also handled.
    """
    import re
    blocks = []
    lines = markdown_text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── <callout> block ─────────────────────────────────────────────────
        callout_attrs = _parse_callout_open(stripped)
        if callout_attrs is not None:
            icon, color = callout_attrs
            body_lines = []
            i += 1
            while i < len(lines) and not re.match(r'\s*</callout>', lines[i], re.IGNORECASE):
                body_lines.append(lines[i].strip())
                i += 1
            body_text = " ".join(bl for bl in body_lines if bl)
            blocks.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": parse_inline(body_text),
                    "icon": {"type": "emoji", "emoji": icon},
                    "color": color,
                },
            })

        # ── <table> block ───────────────────────────────────────────────────
        elif re.match(r'\s*<table[^>]*>', stripped, re.IGNORECASE):
            header_row_attr = 'header-row="true"' in stripped.lower()
            table_rows = []
            i += 1
            while i < len(lines) and not re.match(r'\s*</table>', lines[i], re.IGNORECASE):
                row_line = lines[i].strip()
                if re.match(r'<tr[^>]*>', row_line, re.IGNORECASE):
                    cells = []
                    i += 1
                    while i < len(lines) and not re.match(r'\s*</tr>', lines[i], re.IGNORECASE):
                        cell_line = lines[i].strip()
                        td_m = re.match(r'<td[^>]*>(.*?)</td>', cell_line, re.IGNORECASE | re.DOTALL)
                        if td_m:
                            cells.append(parse_inline(td_m.group(1).strip()))
                        elif cell_line and not re.match(r'</?t[dh]', cell_line, re.IGNORECASE):
                            # multi-line cell content — append to last cell as text
                            if cells:
                                cells[-1].append({"type": "text", "text": {"content": " " + cell_line}})
                        i += 1
                    if cells:
                        table_rows.append(cells)
                else:
                    i += 1
                    continue
            if table_rows:
                col_count = max(len(r) for r in table_rows)
                table_block = {
                    "object": "block",
                    "type": "table",
                    "table": {
                        "table_width": col_count,
                        "has_column_header": header_row_attr,
                        "has_row_header": False,
                        "children": [],
                    },
                }
                for row_cells in table_rows:
                    # Pad short rows
                    while len(row_cells) < col_count:
                        row_cells.append([{"type": "text", "text": {"content": ""}}])
                    table_block["table"]["children"].append({
                        "object": "block",
                        "type": "table_row",
                        "table_row": {"cells": row_cells},
                    })
                blocks.append(table_block)

        # ── <details> / toggle block ─────────────────────────────────────────
        elif re.match(r'\s*<details[^>]*>', stripped, re.IGNORECASE):
            i += 1
            summary_text = "Details"
            if i < len(lines):
                sm = re.match(r'\s*<summary[^>]*>(.*?)</summary>', lines[i], re.IGNORECASE)
                if sm:
                    summary_text = sm.group(1).strip()
                    i += 1
            toggle_children = []
            while i < len(lines) and not re.match(r'\s*</details>', lines[i], re.IGNORECASE):
                inner = lines[i].strip()
                if inner:
                    # Numbered list items inside toggle
                    num_m = re.match(r'^(\d+)\.\s+(.*)', inner)
                    if num_m:
                        toggle_children.append({
                            "object": "block",
                            "type": "numbered_list_item",
                            "numbered_list_item": {"rich_text": parse_inline(num_m.group(2))},
                        })
                    elif inner.startswith("- "):
                        toggle_children.append({
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {"rich_text": parse_inline(inner[2:])},
                        })
                    else:
                        toggle_children.append({
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {"rich_text": parse_inline(inner)},
                        })
                i += 1
            toggle_block = {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": parse_inline(summary_text),
                    "children": toggle_children,
                },
            }
            blocks.append(toggle_block)

        # ── Code fences ──────────────────────────────────────────────────────
        elif line.startswith("```"):
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

        # ── Headings ─────────────────────────────────────────────────────────
        elif line.startswith("### "):
            blocks.append({"object": "block", "type": "heading_3",
                           "heading_3": {"rich_text": parse_inline(line[4:])}})
        elif line.startswith("## "):
            blocks.append({"object": "block", "type": "heading_2",
                           "heading_2": {"rich_text": parse_inline(line[3:])}})
        elif line.startswith("# "):
            blocks.append({"object": "block", "type": "heading_1",
                           "heading_1": {"rich_text": parse_inline(line[2:])}})

        # ── Lists ─────────────────────────────────────────────────────────────
        elif line.startswith("- "):
            blocks.append({"object": "block", "type": "bulleted_list_item",
                           "bulleted_list_item": {"rich_text": parse_inline(line[2:])}})
        elif re.match(r'^\d+\.\s', line):
            text = re.split(r'^\d+\.\s', line, maxsplit=1)[1]
            blocks.append({"object": "block", "type": "numbered_list_item",
                           "numbered_list_item": {"rich_text": parse_inline(text)}})

        # ── Blockquote ────────────────────────────────────────────────────────
        elif line.startswith("> "):
            blocks.append({"object": "block", "type": "quote",
                           "quote": {"rich_text": parse_inline(line[2:])}})

        # ── Divider ───────────────────────────────────────────────────────────
        elif stripped == "---":
            blocks.append({"object": "block", "type": "divider", "divider": {}})

        # ── [INTERNAL_LINK] standalone line — skip ────────────────────────────
        elif re.match(r'^\[INTERNAL_LINK:', stripped):
            pass  # placeholder; no block needed

        # ── Blank lines ───────────────────────────────────────────────────────
        elif stripped == "":
            pass

        # ── Paragraph ─────────────────────────────────────────────────────────
        else:
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": parse_inline(line)}})

        i += 1

    return blocks


def create_page(api_key, api_version, database_id=None, properties_dict=None, body_markdown=None, data_source_id=None):
    try:
        schema, target_id, target_kind = get_schema(
            api_key,
            api_version,
            database_id=database_id,
            data_source_id=data_source_id,
        )
    except RuntimeError as e:
        print(f"ERROR fetching schema: {e}", file=sys.stderr)
        sys.exit(1)

    notion_properties = {}
    for name, value in (properties_dict or {}).items():
        if value is None:
            continue
        notion_properties[name] = build_property_value(name, value, schema)

    parent = {"type": "database_id", "database_id": target_id}
    if target_kind == "data_source" or is_data_source_api(api_version):
        parent = {"type": "data_source_id", "data_source_id": target_id}

    payload = {
        "parent": parent,
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
    parser.add_argument("--database-id", default=None)
    parser.add_argument("--data-source-id", default=None, help="Notion data source ID for 2025-09-03+ API versions")
    parser.add_argument("--properties", required=True, help="Properties as JSON string")
    parser.add_argument("--body", default=None, help="Page body as markdown string")
    parser.add_argument("--body-file", default=None, help="Read body from a file instead of --body")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    if not args.database_id and not args.data_source_id:
        print("ERROR: --database-id or --data-source-id is required", file=sys.stderr)
        sys.exit(1)

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

    result = create_page(
        api_key,
        api_version,
        database_id=args.database_id,
        data_source_id=args.data_source_id,
        properties_dict=properties_dict,
        body_markdown=body,
    )
    write_output(result, args.output)


if __name__ == "__main__":
    main()
