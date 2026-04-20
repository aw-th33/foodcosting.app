"""
Google Search Console client for foodcosting.app agents.

Usage:
    from gsc_client import GSCClient

    gsc = GSCClient()
    rows = gsc.get_keywords(days=28)
    rows = gsc.get_top_pages(days=28)
    rows = gsc.get_keyword_detail("food cost calculator", days=90)
    summary = gsc.get_summary(days=28)

Requires:
    pip install google-auth google-auth-httplib2 google-api-python-client python-dotenv
"""

import os
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SERVICE_ACCOUNT_PATH = os.getenv("GSC_SERVICE_ACCOUNT_PATH", "credentials/gsc_service_account.json")
SITE_URL = os.getenv("GSC_SITE_URL", "sc-domain:foodcosting.app")


class GSCClient:
    def __init__(self, site_url: str = SITE_URL, credentials_path: str = SERVICE_ACCOUNT_PATH):
        self.site_url = site_url
        creds_file = Path(credentials_path)
        if not creds_file.exists():
            raise FileNotFoundError(
                f"Service account key not found at '{creds_file}'. "
                "Download it from Google Cloud Console and place it there."
            )
        creds = service_account.Credentials.from_service_account_file(
            str(creds_file), scopes=SCOPES
        )
        self.service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    def _date_range(self, days: int) -> tuple:
        end = date.today() - timedelta(days=3)  # GSC data lags ~3 days
        start = end - timedelta(days=days - 1)
        return start.isoformat(), end.isoformat()

    def _query(self, dimensions: list, days: int, row_limit: int = 500, dimension_filter=None) -> list:
        start_date, end_date = self._date_range(days)
        request = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": row_limit,
        }
        if dimension_filter:
            request["dimensionFilterGroups"] = dimension_filter

        response = (
            self.service.searchanalytics()
            .query(siteUrl=self.site_url, body=request)
            .execute()
        )

        rows = []
        for row in response.get("rows", []):
            record = {dim: row["keys"][i] for i, dim in enumerate(dimensions)}
            record["clicks"] = int(row["clicks"])
            record["impressions"] = int(row["impressions"])
            record["ctr"] = round(row["ctr"] * 100, 2)
            record["position"] = round(row["position"], 1)
            rows.append(record)

        return rows

    def get_keywords(self, days: int = 28, row_limit: int = 500) -> list:
        """Top keywords by clicks over the last N days."""
        rows = self._query(["query"], days=days, row_limit=row_limit)
        return sorted(rows, key=lambda r: r["clicks"], reverse=True)

    def get_top_pages(self, days: int = 28, row_limit: int = 200) -> list:
        """Top pages by clicks over the last N days."""
        rows = self._query(["page"], days=days, row_limit=row_limit)
        return sorted(rows, key=lambda r: r["clicks"], reverse=True)

    def get_keyword_detail(self, keyword: str, days: int = 90) -> list:
        """Clicks, impressions, position for a specific keyword over time."""
        dim_filter = [{
            "filters": [{
                "dimension": "query",
                "operator": "equals",
                "expression": keyword,
            }]
        }]
        rows = self._query(["date"], days=days, row_limit=days, dimension_filter=dim_filter)
        return sorted(rows, key=lambda r: r["date"])

    def get_keywords_by_position(self, min_pos: float = 5.0, max_pos: float = 20.0, days: int = 28) -> list:
        """Keywords ranking between two positions — useful for finding 'almost ranking' terms."""
        rows = self.get_keywords(days=days, row_limit=1000)
        filtered = [r for r in rows if min_pos <= r["position"] <= max_pos]
        return sorted(filtered, key=lambda r: r["position"])

    def get_summary(self, days: int = 28) -> dict:
        """High-level summary: total clicks, impressions, avg CTR, avg position."""
        rows = self.get_keywords(days=days, row_limit=1000)
        if not rows:
            return {}
        total_clicks = sum(r["clicks"] for r in rows)
        total_impressions = sum(r["impressions"] for r in rows)
        avg_ctr = round(sum(r["ctr"] for r in rows) / len(rows), 2)
        avg_position = round(sum(r["position"] for r in rows) / len(rows), 1)
        return {
            "period_days": days,
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "avg_ctr_pct": avg_ctr,
            "avg_position": avg_position,
            "total_keywords": len(rows),
        }


def _print_table(rows: list, cols: list = None, limit: int = 10):
    if not rows:
        print("  (no data)")
        return
    if cols is None:
        cols = list(rows[0].keys())
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in rows[:limit])) for c in cols}
    header = "  ".join(c.ljust(widths[c]) for c in cols)
    print(header)
    print("-" * len(header))
    for row in rows[:limit]:
        print("  ".join(str(row.get(c, "")).ljust(widths[c]) for c in cols))


if __name__ == "__main__":
    gsc = GSCClient()

    print("=== Last 28 days — Summary ===")
    summary = gsc.get_summary(days=28)
    for k, v in summary.items():
        print(f"  {k}: {v}")

    print("\n=== Top 10 keywords ===")
    _print_table(gsc.get_keywords(days=28), cols=["query", "clicks", "impressions", "ctr", "position"])

    print("\n=== Top 10 pages ===")
    _print_table(gsc.get_top_pages(days=28), cols=["page", "clicks", "impressions", "ctr", "position"])

    print("\n=== Opportunity zone: positions 5–20 ===")
    _print_table(gsc.get_keywords_by_position(5, 20, days=28), cols=["query", "clicks", "impressions", "position"])
