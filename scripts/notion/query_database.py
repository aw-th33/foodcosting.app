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
