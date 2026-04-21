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
