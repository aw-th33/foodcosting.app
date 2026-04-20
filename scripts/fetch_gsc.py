"""
Fetch Google Search Console data for foodcosting.app.
Outputs JSON to stdout for the topic researcher agent to consume.

Usage:
    python scripts/fetch_gsc.py
    python scripts/fetch_gsc.py --days 90
    python scripts/fetch_gsc.py --days 28 --output pipeline/gsc_snapshot.json
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

def get_credentials():
    cred_path = os.environ.get("GSC_SERVICE_ACCOUNT_PATH", "credentials/gsc_service_account.json")
    if not Path(cred_path).exists():
        raise FileNotFoundError(f"Service account file not found: {cred_path}")

    from google.oauth2 import service_account
    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    return service_account.Credentials.from_service_account_file(cred_path, scopes=scopes)


def fetch_queries(service, site_url, start_date, end_date, row_limit=500):
    request = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": row_limit,
        "orderBy": [{"fieldName": "impressions", "sortOrder": "DESCENDING"}],
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    return response.get("rows", [])


def fetch_pages(service, site_url, start_date, end_date, row_limit=200):
    request = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page"],
        "rowLimit": row_limit,
        "orderBy": [{"fieldName": "impressions", "sortOrder": "DESCENDING"}],
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    return response.get("rows", [])


def classify_opportunities(rows):
    """
    Tag each query with its opportunity type:
    - quick_win: position 11-20 (just off page 1), decent impressions
    - high_impression_low_ctr: lots of impressions but CTR < 2%
    - strong_performer: already doing well, reinforce
    - low_hanging: position 4-10, could improve with better content
    """
    tagged = []
    for row in rows:
        query = row["keys"][0]
        impressions = row.get("impressions", 0)
        clicks = row.get("clicks", 0)
        ctr = row.get("ctr", 0)
        position = row.get("position", 0)

        tags = []
        if 11 <= position <= 20 and impressions >= 50:
            tags.append("quick_win")
        if impressions >= 100 and ctr < 0.02:
            tags.append("high_impression_low_ctr")
        if 4 <= position <= 10 and impressions >= 30:
            tags.append("low_hanging")
        if clicks >= 10 and ctr >= 0.05:
            tags.append("strong_performer")
        if not tags:
            tags.append("monitor")

        tagged.append({
            "query": query,
            "impressions": impressions,
            "clicks": clicks,
            "ctr": round(ctr * 100, 2),
            "position": round(position, 1),
            "opportunity_tags": tags,
        })

    return tagged


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=90, help="Lookback window in days")
    parser.add_argument("--output", type=str, default=None, help="Write JSON to file instead of stdout")
    args = parser.parse_args()

    site_url = os.environ.get("GSC_SITE_URL", "sc-domain:foodcosting.app")
    end_date = datetime.today() - timedelta(days=3)  # GSC has ~3 day lag
    start_date = end_date - timedelta(days=args.days)

    from googleapiclient.discovery import build
    credentials = get_credentials()
    service = build("searchconsole", "v1", credentials=credentials)

    queries = fetch_queries(service, site_url, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    pages = fetch_pages(service, site_url, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    tagged_queries = classify_opportunities(queries)

    output = {
        "fetched_at": datetime.now().isoformat(),
        "site_url": site_url,
        "date_range": {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "days": args.days,
        },
        "summary": {
            "total_queries": len(tagged_queries),
            "quick_wins": sum(1 for q in tagged_queries if "quick_win" in q["opportunity_tags"]),
            "high_impression_low_ctr": sum(1 for q in tagged_queries if "high_impression_low_ctr" in q["opportunity_tags"]),
            "low_hanging": sum(1 for q in tagged_queries if "low_hanging" in q["opportunity_tags"]),
        },
        "top_pages": [
            {
                "page": r["keys"][0],
                "impressions": r.get("impressions", 0),
                "clicks": r.get("clicks", 0),
                "ctr": round(r.get("ctr", 0) * 100, 2),
                "position": round(r.get("position", 0), 1),
            }
            for r in pages[:20]
        ],
        "queries": tagged_queries,
    }

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Written to {args.output}")
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
