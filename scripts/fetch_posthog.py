"""
Fetch PostHog analytics data for foodcosting.app.
Outputs JSON to stdout for agents to consume and act on.

Uses the PostHog HogQL query API (current, non-legacy).

Usage:
    python scripts/fetch_posthog.py
    python scripts/fetch_posthog.py --days 30
    python scripts/fetch_posthog.py --days 7 --output pipeline/posthog_snapshot.json

Environment variables:
    POSTHOG_API_KEY       - Personal API key (required)
    POSTHOG_PROJECT_ID    - Project ID (required)
    POSTHOG_HOST          - API host (default: https://us.posthog.com)
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def load_env():
    """Load .env file from project root if it exists."""
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


def get_config():
    api_key = os.environ.get("POSTHOG_API_KEY")
    project_id = os.environ.get("POSTHOG_PROJECT_ID")
    host = os.environ.get("POSTHOG_HOST", "https://us.posthog.com")

    if not api_key:
        raise ValueError("POSTHOG_API_KEY environment variable is required")
    if not project_id:
        raise ValueError("POSTHOG_PROJECT_ID environment variable is required")

    return api_key, project_id, host.rstrip("/")


def hogql_query(host, project_id, api_key, query):
    """Execute a HogQL query via the PostHog query API."""
    url = f"{host}/api/projects/{project_id}/query/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {"query": {"kind": "HogQLQuery", "query": query}}
    data = json.dumps(body).encode()
    req = Request(url, data=data, headers=headers, method="POST")
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"PostHog API error {e.code}: {error_body}") from e


def run_query(host, project_id, api_key, query):
    """Run HogQL query and return list of dicts."""
    result = hogql_query(host, project_id, api_key, query)
    columns = result.get("columns", [])
    rows = result.get("results", [])
    return [dict(zip(columns, row)) for row in rows]


def country_exclusion_filter(country_code):
    if not country_code:
        return ""
    country_code = country_code.upper().replace("'", "")
    return f"AND coalesce(properties.$geoip_country_code, '') != '{country_code}'"


def fetch_daily_pageviews(host, project_id, api_key, date_from, date_to, extra_filter=""):
    query = f"""
        SELECT
            toDate(timestamp) AS day,
            count() AS pageviews,
            count(DISTINCT distinct_id) AS unique_visitors
        FROM events
        WHERE event = '$pageview'
          AND timestamp >= '{date_from}'
          AND timestamp <= '{date_to} 23:59:59'
          {extra_filter}
        GROUP BY day
        ORDER BY day
    """
    return run_query(host, project_id, api_key, query)


def fetch_top_pages(host, project_id, api_key, date_from, date_to, limit=30, extra_filter=""):
    query = f"""
        SELECT
            properties.$host AS host,
            properties.$pathname AS path,
            concat('https://', properties.$host, properties.$pathname) AS url,
            count() AS pageviews,
            count(DISTINCT distinct_id) AS unique_visitors
        FROM events
        WHERE event = '$pageview'
          AND timestamp >= '{date_from}'
          AND timestamp <= '{date_to} 23:59:59'
          {extra_filter}
        GROUP BY host, path, url
        ORDER BY pageviews DESC
        LIMIT {limit}
    """
    return run_query(host, project_id, api_key, query)


def fetch_referrers(host, project_id, api_key, date_from, date_to, limit=20, extra_filter=""):
    query = f"""
        SELECT
            properties.$referring_domain AS referrer,
            count() AS pageviews,
            count(DISTINCT distinct_id) AS unique_visitors
        FROM events
        WHERE event = '$pageview'
          AND timestamp >= '{date_from}'
          AND timestamp <= '{date_to} 23:59:59'
          AND properties.$referrer IS NOT NULL
          AND properties.$referrer != ''
          {extra_filter}
        GROUP BY referrer
        ORDER BY pageviews DESC
        LIMIT {limit}
    """
    return run_query(host, project_id, api_key, query)


def fetch_utm_sources(host, project_id, api_key, date_from, date_to, limit=20, extra_filter=""):
    query = f"""
        SELECT
            properties.utm_source AS utm_source,
            count() AS pageviews,
            count(DISTINCT distinct_id) AS unique_visitors
        FROM events
        WHERE event = '$pageview'
          AND timestamp >= '{date_from}'
          AND timestamp <= '{date_to} 23:59:59'
          AND properties.utm_source IS NOT NULL
          AND properties.utm_source != ''
          {extra_filter}
        GROUP BY utm_source
        ORDER BY pageviews DESC
        LIMIT {limit}
    """
    return run_query(host, project_id, api_key, query)


def fetch_devices(host, project_id, api_key, date_from, date_to, extra_filter=""):
    query = f"""
        SELECT
            properties.$device_type AS device_type,
            count() AS pageviews,
            count(DISTINCT distinct_id) AS unique_visitors
        FROM events
        WHERE event = '$pageview'
          AND timestamp >= '{date_from}'
          AND timestamp <= '{date_to} 23:59:59'
          {extra_filter}
        GROUP BY device_type
        ORDER BY pageviews DESC
    """
    return run_query(host, project_id, api_key, query)


def fetch_event_names(host, project_id, api_key, date_from, date_to, limit=50, extra_filter=""):
    """List all event names and their counts — useful for discovering custom events."""
    query = f"""
        SELECT
            event,
            count() AS total
        FROM events
        WHERE timestamp >= '{date_from}'
          AND timestamp <= '{date_to} 23:59:59'
          {extra_filter}
        GROUP BY event
        ORDER BY total DESC
        LIMIT {limit}
    """
    return run_query(host, project_id, api_key, query)


def fetch_countries(host, project_id, api_key, date_from, date_to, limit=30):
    query = f"""
        SELECT
            properties.$geoip_country_code AS country_code,
            properties.$geoip_country_name AS country_name,
            count() AS pageviews,
            count(DISTINCT distinct_id) AS unique_visitors
        FROM events
        WHERE event = '$pageview'
          AND timestamp >= '{date_from}'
          AND timestamp <= '{date_to} 23:59:59'
        GROUP BY country_code, country_name
        ORDER BY pageviews DESC
        LIMIT {limit}
    """
    return run_query(host, project_id, api_key, query)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30, help="Lookback window in days")
    parser.add_argument("--output", type=str, default=None, help="Write JSON to file instead of stdout")
    parser.add_argument("--events-only", action="store_true", help="Only list event names (for discovery)")
    parser.add_argument("--exclude-country-code", type=str, default=None, help="Exclude traffic from an ISO country code, e.g. KE")
    args = parser.parse_args()

    api_key, project_id, host = get_config()
    date_to = datetime.today().strftime("%Y-%m-%d")
    date_from = (datetime.today() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    extra_filter = country_exclusion_filter(args.exclude_country_code)
    print(f"Fetching PostHog data ({date_from} to {date_to})...", flush=True)

    # --- Event discovery mode ---
    if args.events_only:
        events = fetch_event_names(host, project_id, api_key, date_from, date_to, extra_filter=extra_filter)
        output = {
            "fetched_at": datetime.now().isoformat(),
            "date_range": {"start": date_from, "end": date_to, "days": args.days},
            "filters": {"exclude_country_code": args.exclude_country_code},
            "events": events,
        }
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w") as f:
                json.dump(output, f, indent=2)
            print(f"Written to {args.output}")
        else:
            print(json.dumps(output, indent=2))
        return

    # --- Full analytics fetch ---
    daily = fetch_daily_pageviews(host, project_id, api_key, date_from, date_to, extra_filter=extra_filter)
    top_pages = fetch_top_pages(host, project_id, api_key, date_from, date_to, extra_filter=extra_filter)
    referrers = fetch_referrers(host, project_id, api_key, date_from, date_to, extra_filter=extra_filter)
    utm_sources = fetch_utm_sources(host, project_id, api_key, date_from, date_to, extra_filter=extra_filter)
    devices = fetch_devices(host, project_id, api_key, date_from, date_to, extra_filter=extra_filter)
    countries = fetch_countries(host, project_id, api_key, date_from, date_to)
    events = fetch_event_names(host, project_id, api_key, date_from, date_to, extra_filter=extra_filter)

    total_pageviews = sum(d.get("pageviews", 0) for d in daily)
    total_visitors = sum(d.get("unique_visitors", 0) for d in daily)

    output = {
        "fetched_at": datetime.now().isoformat(),
        "project_id": project_id,
        "date_range": {
            "start": date_from,
            "end": date_to,
            "days": args.days,
        },
        "filters": {
            "exclude_country_code": args.exclude_country_code,
        },
        "summary": {
            "total_pageviews": total_pageviews,
            "total_unique_visitors": total_visitors,
            "avg_daily_pageviews": round(total_pageviews / max(args.days, 1), 1),
            "avg_daily_visitors": round(total_visitors / max(args.days, 1), 1),
        },
        "pageviews_daily": daily,
        "top_pages": top_pages,
        "referrers": referrers,
        "utm_sources": utm_sources,
        "devices": devices,
        "countries": countries,
        "all_events": events,
    }

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Written to {args.output}")
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    load_env()
    main()
