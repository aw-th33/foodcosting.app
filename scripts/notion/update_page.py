"""
Update properties on an existing Notion page.

Usage:
    python scripts/notion/update_page.py \\
        --page-id <id> \\
        --properties '{"Status": "Used"}'

Output (stdout):
    { "id": "...", "url": "...", "updated": ["Status"] }

The script fetches the page's parent database or data source schema to map property types correctly.
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _client import load_env, get_auth, notion_request, write_output, get_page_schema
from create_page import build_property_value


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
    try:
        schema, _ = get_page_schema(api_key, api_version, page_id)
    except RuntimeError as e:
        print(f"ERROR resolving page schema: {e}", file=sys.stderr)
        sys.exit(1)

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
