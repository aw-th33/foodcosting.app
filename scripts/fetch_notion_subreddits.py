"""
Fetch the subreddit list from Notion's community monitor database.
Saves a local cache at pipeline/out/community-monitor/subreddit-cache.json
for fallback use when Notion is unavailable.

Usage:
    python scripts/fetch_notion_subreddits.py
    python scripts/fetch_notion_subreddits.py --output custom/path.json

Environment variables:
    NOTION_API_KEY                            - Required
    NOTION_REDDIT_SUBREDDITS_DATABASE_ID      - Required
    NOTION_REDDIT_SUBREDDITS_DATA_SOURCE_ID   - Optional (auto-discovered if only one source)
    NOTION_VERSION                            - Optional, default 2026-03-11
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


CACHE_DIR = Path(__file__).resolve().parent.parent / "pipeline" / "out" / "community-monitor"
DEFAULT_CACHE_PATH = CACHE_DIR / "subreddit-cache.json"


def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
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


def notion_request(api_key, api_version, endpoint, method="GET", body=None):
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
        raise RuntimeError(f"Notion API {method} {endpoint}: {e.code} - {error_body}") from e


def get_config():
    api_key = os.environ.get("NOTION_API_KEY")
    database_id = os.environ.get("NOTION_REDDIT_SUBREDDITS_DATABASE_ID")
    data_source_id = os.environ.get("NOTION_REDDIT_SUBREDDITS_DATA_SOURCE_ID")
    api_version = os.environ.get("NOTION_VERSION", "2026-03-11")

    if not api_key:
        raise ValueError("NOTION_API_KEY environment variable is required")
    if not database_id:
        raise ValueError("NOTION_REDDIT_SUBREDDITS_DATABASE_ID is required")

    return api_key, database_id, data_source_id, api_version


def extract_text_value(prop):
    """Extract text from a Notion property, handling various types."""
    if not prop:
        return ""
    ptype = prop.get("type", "")
    if ptype == "rich_text":
        items = prop.get("rich_text", [])
        return " ".join(item.get("plain_text", "") for item in items)
    elif ptype == "title":
        items = prop.get("title", [])
        return " ".join(item.get("plain_text", "") for item in items)
    elif ptype == "select":
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""
    elif ptype == "multi_select":
        items = prop.get("multi_select", [])
        return [item.get("name", "") for item in items]
    elif ptype == "url":
        return prop.get("url", "") or ""
    elif ptype == "number":
        return prop.get("number")
    elif ptype == "date":
        d = prop.get("date")
        return d.get("start", "") if d else ""
    return ""


def discover_data_source(api_key, api_version, database_id):
    """Try to discover the data source for a Notion database."""
    db = notion_request(api_key, api_version, f"databases/{database_id}")
    # Notion API may return data_sources in the response
    data_sources = db.get("data_sources", [])
    if len(data_sources) == 1:
        return data_sources[0].get("id")
    return None


def fetch_subreddits(api_key, api_version, database_id, data_source_id=None):
    """Fetch all rows from the subreddit database."""
    # If no data_source_id provided, try using the database query endpoint directly
    # (older Notion databases were queryable directly)
    if not data_source_id:
        try:
            body = {
                "filter": {
                    "or": [
                        {"property": "Status", "select": {"equals": "Active"}},
                        {"property": "Status", "select": {"equals": "Watch"}},
                    ]
                }
            }
            result = notion_request(api_key, api_version, f"databases/{database_id}/query", method="POST", body=body)
            return result.get("results", [])
        except RuntimeError:
            # Fall back to trying data source discovery
            discovered = discover_data_source(api_key, api_version, database_id)
            if discovered:
                data_source_id = discovered
            else:
                raise

    # Query the data source
    body = {
        "filter": {
            "or": [
                {"property": "Status", "select": {"equals": "Active"}},
                {"property": "Status", "select": {"equals": "Watch"}},
            ]
        }
    }
    result = notion_request(api_key, api_version, f"data_sources/{data_source_id}/query", method="POST", body=body)
    return result.get("results", [])


def filter_subreddits(pages, property_map):
    """Convert Notion pages to subreddit dicts and filter out high-risk entries."""
    subreddits = []
    pm = property_map

    for page in pages:
        props = page.get("properties", {})

        subreddit_name = extract_text_value(props.get(pm.get("subreddit", "Subreddit")))
        status = extract_text_value(props.get(pm.get("status", "Status")))
        priority = extract_text_value(props.get(pm.get("priority", "Priority")))
        promotion_risk = extract_text_value(props.get(pm.get("promotion_risk", "Promotion Risk")))
        audience = extract_text_value(props.get(pm.get("audience", "Audience")))
        angle = extract_text_value(props.get(pm.get("angle", "Angle")))
        notes = extract_text_value(props.get(pm.get("notes", "Notes")))

        if not subreddit_name:
            continue
        # Clean up subreddit names (remove r/ prefix for API use)
        clean_name = subreddit_name.replace("r/", "").replace("https://reddit.com/r/", "").strip()

        subreddits.append({
            "name": clean_name,
            "priority": priority if priority else 1.0,
            "promotion_risk": promotion_risk.lower() if promotion_risk else "medium",
            "audience": audience if isinstance(audience, list) else ([audience] if audience else []),
            "angle": angle if isinstance(angle, list) else ([angle] if angle else []),
            "notes": notes,
        })

    # Filter out high-risk subreddits unless explicitly active
    subreddits = [s for s in subreddits if s["promotion_risk"] != "high"]
    return subreddits


def save_cache(subreddits, output_path=None):
    path = Path(output_path) if output_path else DEFAULT_CACHE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    cache = {
        "fetched_at": datetime.now().isoformat(),
        "source": "notion",
        "database": "foodcosting / Reddit / Sub-Reddits",
        "subreddits": subreddits,
    }

    with open(path, "w") as f:
        json.dump(cache, f, indent=2)

    print(f"Subreddit cache saved to {path}")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default=None, help="Custom cache output path")
    args = parser.parse_args()

    api_key, database_id, data_source_id, api_version = get_config()

    print("Fetching subreddits from Notion...", flush=True)
    pages = fetch_subreddits(api_key, api_version, database_id, data_source_id)

    # Load config for property map
    config_path = Path(__file__).resolve().parent.parent / "pipeline" / "context" / "community-monitor-config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        property_map = config.get("notion_property_map", {})
    else:
        property_map = {}

    subreddits = filter_subreddits(pages, property_map)
    print(f"Found {len(subreddits)} active subreddits: {', '.join(s['name'] for s in subreddits)}")

    save_cache(subreddits, args.output)
    return subreddits


if __name__ == "__main__":
    load_env()
    main()
