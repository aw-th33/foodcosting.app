"""
Fetch richer Google Search Console data for the SEO specialist agent.

Outputs query, page, and page+query Search Analytics data for short and long
lookback windows. This script is read-only and does not write to Notion.

Usage:
    python scripts/fetch_seo_gsc.py
    python scripts/fetch_seo_gsc.py --short-days 28 --long-days 90
    python scripts/fetch_seo_gsc.py --output pipeline/context/seo-gsc-snapshot.json
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path


DEFAULT_OUTPUT = "pipeline/context/seo-gsc-snapshot.json"
DEFAULT_SITE_URL = "sc-domain:foodcosting.app"
DEFAULT_SERVICE_ACCOUNT_PATH = "credentials/gsc_service_account.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def load_env():
    """Load .env from the repo root without requiring python-dotenv."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key and value and key not in os.environ:
            os.environ[key] = value


def get_credentials():
    credentials_path = os.environ.get("GSC_SERVICE_ACCOUNT_PATH", DEFAULT_SERVICE_ACCOUNT_PATH)
    creds_file = Path(credentials_path)
    if not creds_file.exists():
        raise FileNotFoundError(
            f"Service account file not found: {creds_file}. "
            "Set GSC_SERVICE_ACCOUNT_PATH or place the key at credentials/gsc_service_account.json."
        )

    from google.oauth2 import service_account

    return service_account.Credentials.from_service_account_file(
        str(creds_file),
        scopes=SCOPES,
    )


def build_date_range(days):
    end = datetime.today() - timedelta(days=3)
    start = end - timedelta(days=days - 1)
    return {
        "days": days,
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
    }


def clean_row(row, dimensions, window_name):
    record = {
        "window": window_name,
        "clicks": int(row.get("clicks", 0)),
        "impressions": int(row.get("impressions", 0)),
        "ctr": round(row.get("ctr", 0) * 100, 2),
        "position": round(row.get("position", 0), 1),
    }
    keys = row.get("keys", [])
    for index, dimension in enumerate(dimensions):
        record[dimension] = keys[index] if index < len(keys) else ""
    return record


def fetch_dimension_rows(service, site_url, date_range, dimensions, row_limit, window_name):
    request = {
        "startDate": date_range["start"],
        "endDate": date_range["end"],
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    response = (
        service.searchanalytics()
        .query(siteUrl=site_url, body=request)
        .execute()
    )
    rows = [
        clean_row(row, dimensions, window_name)
        for row in response.get("rows", [])
    ]
    return sorted(rows, key=lambda row: row["impressions"], reverse=True)


def fetch_window(service, site_url, window_name, date_range, row_limit):
    return {
        "queries": fetch_dimension_rows(
            service,
            site_url,
            date_range,
            ["query"],
            row_limit,
            window_name,
        ),
        "pages": fetch_dimension_rows(
            service,
            site_url,
            date_range,
            ["page"],
            row_limit,
            window_name,
        ),
        "page_queries": fetch_dimension_rows(
            service,
            site_url,
            date_range,
            ["page", "query"],
            row_limit,
            window_name,
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch SEO-focused GSC data")
    parser.add_argument("--short-days", type=int, default=28)
    parser.add_argument("--long-days", type=int, default=90)
    parser.add_argument("--row-limit", type=int, default=1000)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    load_env()

    site_url = os.environ.get("GSC_SITE_URL", DEFAULT_SITE_URL)
    credentials = get_credentials()

    from googleapiclient.discovery import build

    service = build("searchconsole", "v1", credentials=credentials, cache_discovery=False)
    date_ranges = {
        "short": build_date_range(args.short_days),
        "long": build_date_range(args.long_days),
    }

    short_rows = fetch_window(service, site_url, "short", date_ranges["short"], args.row_limit)
    long_rows = fetch_window(service, site_url, "long", date_ranges["long"], args.row_limit)

    output = {
        "fetched_at": datetime.now().isoformat(),
        "site_url": site_url,
        "date_ranges": date_ranges,
        "queries": short_rows["queries"] + long_rows["queries"],
        "pages": short_rows["pages"] + long_rows["pages"],
        "page_queries": short_rows["page_queries"] + long_rows["page_queries"],
        "optional_paid_data": {
            "ahrefs_csv_path": "pipeline/context/ahrefs-keywords.csv",
            "loaded": Path("pipeline/context/ahrefs-keywords.csv").exists(),
        },
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Written to {output_path}")


if __name__ == "__main__":
    main()
