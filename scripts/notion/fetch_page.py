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
