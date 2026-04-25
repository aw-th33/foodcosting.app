"""
Shared Notion API client utilities.
Extracted from scripts/fetch_notion_subreddits.py — same pattern, reusable.

Environment variables required:
    NOTION_API_KEY      - required
    NOTION_VERSION      - optional, default 2022-06-28
"""

import os
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


DEFAULT_NOTION_VERSION = "2022-06-28"
DATA_SOURCE_API_VERSION = "2025-09-03"


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
    api_version = os.environ.get("NOTION_VERSION", DEFAULT_NOTION_VERSION)
    return api_key, api_version


def _parse_version(api_version):
    """Return (year, month, day) for Notion API date strings."""
    try:
        year, month, day = api_version.split("-", 2)
        return int(year), int(month), int(day)
    except (AttributeError, ValueError):
        return 0, 0, 0


def is_data_source_api(api_version):
    """Whether this Notion version uses data sources for database operations."""
    return _parse_version(api_version) >= _parse_version(DATA_SOURCE_API_VERSION)


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


def discover_data_source_id(api_key, api_version, database_id):
    """Resolve a database with exactly one child data source to that data source ID."""
    if not database_id:
        raise RuntimeError("--database-id is required when --data-source-id is not provided")

    db = notion_request(api_key, api_version, f"databases/{database_id}")
    data_sources = db.get("data_sources", [])
    if len(data_sources) == 1:
        return data_sources[0]["id"]
    if len(data_sources) > 1:
        ids = ", ".join(ds.get("id", "<missing>") for ds in data_sources)
        raise RuntimeError(
            "Database has multiple data sources; pass --data-source-id explicitly. "
            f"Available data source IDs: {ids}"
        )
    raise RuntimeError(
        "No data source was returned for this database. "
        "For modern Notion API versions, pass --data-source-id explicitly."
    )


def resolve_query_target(api_key, api_version, database_id=None, data_source_id=None):
    """Return (kind, id, endpoint) for querying database-like content."""
    if is_data_source_api(api_version):
        resolved = data_source_id or discover_data_source_id(api_key, api_version, database_id)
        return "data_source", resolved, f"data_sources/{resolved}/query"

    if not database_id:
        raise RuntimeError("--database-id is required for NOTION_VERSION before 2025-09-03")
    return "database", database_id, f"databases/{database_id}/query"


def get_schema(api_key, api_version, database_id=None, data_source_id=None):
    """Fetch the property schema for a database or data source."""
    if is_data_source_api(api_version):
        resolved = data_source_id or discover_data_source_id(api_key, api_version, database_id)
        result = notion_request(api_key, api_version, f"data_sources/{resolved}")
        return result.get("properties", {}), resolved, "data_source"

    if not database_id:
        raise RuntimeError("--database-id is required for schema lookup before 2025-09-03")
    result = notion_request(api_key, api_version, f"databases/{database_id}")
    return result.get("properties", {}), database_id, "database"


def get_page_schema(api_key, api_version, page_id):
    """Fetch a page and return its parent-aware schema plus the page object."""
    page = notion_request(api_key, api_version, f"pages/{page_id}")
    parent = page.get("parent", {})
    parent_type = parent.get("type")

    if parent_type == "data_source_id":
        schema, _, _ = get_schema(
            api_key,
            api_version,
            data_source_id=parent.get("data_source_id"),
        )
        return schema, page

    if parent_type == "database_id":
        schema, _, _ = get_schema(
            api_key,
            api_version,
            database_id=parent.get("database_id"),
        )
        return schema, page

    raise RuntimeError("page is not in a database or data source - cannot resolve property types")


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
