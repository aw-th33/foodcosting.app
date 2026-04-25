"""
Fetch recent Reddit threads from monitored subreddits and score them for
relevance to foodcosting.app. Writes a dated markdown report and JSON
to pipeline/out/community-monitor/.

Uses Reddit's public JSON endpoints (.json) — no API auth needed.

Usage:
    python scripts/fetch_reddit_community_threads.py
    python scripts/fetch_reddit_community_threads.py --days 1 --max-threads 10

Environment variables:
    None required. NOTION_API_KEY needed for subreddit list (otherwise uses cache).
"""

import os
import json
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
from urllib.error import HTTPError, URLError

OUT_DIR = Path(__file__).resolve().parent.parent / "pipeline" / "out" / "community-monitor"
CONFIG_PATH = Path(__file__).resolve().parent.parent / "pipeline" / "context" / "community-monitor-config.json"
CACHE_PATH = OUT_DIR / "subreddit-cache.json"

USER_AGENT = "windows:foodcosting.community.monitor:v0.1.0"


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


def fetch_json(url, retries=2):
    """Fetch a URL and return parsed JSON."""
    headers = {"User-Agent": USER_AGENT}
    req = Request(url, headers=headers)
    for attempt in range(retries + 1):
        try:
            with urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except (HTTPError, URLError) as e:
            if attempt < retries:
                time.sleep(2)
                continue
            print(f"  Fetch failed for {url}: {e}")
        except Exception as e:
            print(f"  Fetch failed for {url}: {e}")
    return None


def load_subreddits():
    """Load subreddits from cache (Notion fetch is the other script)."""
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            cache = json.load(f)
        data = cache.get("subreddits", [])
        fetched = cache.get("fetched_at", "unknown")
        print(f"Loaded {len(data)} subreddits from cache (fetched: {fetched})")
        return data, False
    return [], True


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {
        "max_thread_age_hours": 48,
        "max_comments": 50,
        "daily_limit": 5,
        "query_themes": {},
        "scoring": {
            "age_under_24h": 25,
            "age_24h_to_48h": 10,
            "comments_under_10": 15,
            "comments_10_to_30": 8,
            "high_intent_keyword": 20,
            "tool_keyword": 15,
            "business_type_mention": 15,
            "question_phrasing": 10,
        }
    }


def flatten_themes(query_themes):
    result = []
    for theme, keywords in query_themes.items():
        for kw in keywords:
            result.append((kw, theme))
    return result


def is_question(title):
    t = title.lower()
    return "?" in t or any(t.startswith(p) for p in [
        "how ", "what ", "should i", "how do", "how to",
        "is there", "can someone", "anyone know", "looking for"
    ])


def business_type_mentioned(title, body):
    text = (title + " " + body).lower()
    return any(w in text for w in [
        "restaurant", "food truck", "catering", "bakery", "cafe",
        "food business", "home baker", "meal prep", "ghost kitchen"
    ])


def tool_intent(title, body):
    text = (title + " " + body).lower()
    return any(w in text for w in [
        "spreadsheet", "excel", "calculator", "software", "app",
        "tool", "template", "google sheets"
    ])


def fetch_subreddit_json(subreddit, kind="new", q=None, limit=25):
    """Fetch subreddit listings via .json endpoint."""
    if kind == "search" and q:
        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={quote_plus(q)}&restrict_sr=1&sort=new&t=week&limit={limit}"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/{kind}.json?limit={limit}"
    return fetch_json(url)


def extract_posts(listing):
    """Extract post dicts from a Reddit JSON listing."""
    if not listing:
        return []
    children = listing.get("data", {}).get("children", [])
    posts = []
    for child in children:
        d = child.get("data", {})
        posts.append({
            "id": d.get("id"),
            "title": d.get("title", ""),
            "selftext": d.get("selftext", ""),
            "permalink": d.get("permalink", ""),
            "num_comments": d.get("num_comments", 0),
            "ups": d.get("ups", 0),
            "created_utc": d.get("created_utc", 0),
            "locked": d.get("locked", False),
            "subreddit": d.get("subreddit", ""),
        })
    return posts


def score_thread(post, priority, config, matched_terms):
    scoring = config.get("scoring", {})
    now = datetime.now(timezone.utc).timestamp()

    age_hours = (now - post["created_utc"]) / 3600
    max_age = config.get("max_thread_age_hours", 48)
    if age_hours > max_age:
        return None

    max_comments = config.get("max_comments", 50)
    if post["num_comments"] > max_comments:
        return None

    if post["locked"]:
        return None

    # Age
    if age_hours < 24:
        age_score = scoring.get("age_under_24h", 25)
    else:
        age_score = scoring.get("age_24h_to_48h", 10)

    # Comments
    if post["num_comments"] < 10:
        comment_score = scoring.get("comments_under_10", 15)
    elif post["num_comments"] <= 30:
        comment_score = scoring.get("comments_10_to_30", 8)
    else:
        return None

    # Keywords
    keyword_score = len(matched_terms) * scoring.get("high_intent_keyword", 20)

    # Bonuses
    tool_bonus = scoring.get("tool_keyword", 15) if tool_intent(post["title"], post["selftext"]) else 0
    business_bonus = scoring.get("business_type_mention", 15) if business_type_mentioned(post["title"], post["selftext"]) else 0
    question_bonus = scoring.get("question_phrasing", 10) if is_question(post["title"]) else 0

    total = (age_score + comment_score + keyword_score + tool_bonus + business_bonus + question_bonus) * float(priority)

    return {
        "total": int(total),
        "age_hours": round(age_hours, 1),
        "matched_terms": matched_terms,
    }


def _suggest_angle(themes, title, matched_terms):
    angles = []
    if "food_costing" in themes or "recipe_menu_costing" in themes:
        angles.append("Explain food cost calculation basics with a concrete example")
    if "pricing_profitability" in themes:
        angles.append("Walk through validating menu prices against market rates")
    if "operations" in themes:
        angles.append("Suggest tracking top 5 highest-cost SKUs first")
    if "tool_intent" in themes:
        angles.append("Share the spreadsheet pain honestly")
    return ". ".join(angles) if angles else "Answer directly with actionable advice"


def _classify_product_mention(title, body):
    text = (title + " " + body).lower()
    if any(w in text for w in ["software", "app", "calculator", "template", "tool", "spreadsheet help"]):
        return "direct"
    if any(w in text for w in ["excel", "sheet", "google sheets"]):
        return "soft"
    return "none"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--max-threads", type=int, default=None)
    args = parser.parse_args()

    load_env()

    config = load_config()
    subreddits, cache_missing = load_subreddits()

    if not subreddits:
        # Fallback seed list when Notion isn't set up yet
        fallback_subs = [
            {"name": "restaurantowners", "priority": 1.2, "promotion_risk": "low"},
            {"name": "foodtrucks", "priority": 1.1, "promotion_risk": "low"},
            {"name": "catering", "priority": 1.1, "promotion_risk": "low"},
            {"name": "smallbusiness", "priority": 0.8, "promotion_risk": "medium"},
            {"name": "restaurateur", "priority": 1.0, "promotion_risk": "medium"},
        ]
        source = "Notion" if not cache_missing else "fallback seed"
        print(f"WARNING: Using {source} subreddit list — run fetch_notion_subreddits.py when Notion is ready.")
        subreddits = fallback_subs

    themes = config.get("query_themes", {})
    all_themes = flatten_themes(themes)
    daily_limit = args.max_threads or config.get("daily_limit", 5)

    seen_ids = set()
    candidates = []

    for sub in subreddits:
        name = sub["name"]
        priority = sub.get("priority", 1.0)
        print(f"\nScanning r/{name} (priority: {priority})...", flush=True)

        # Fetch new posts
        listing = fetch_subreddit_json(name, kind="new", limit=25)
        for post in extract_posts(listing):
            if post["id"] and post["id"] not in seen_ids:
                seen_ids.add(post["id"])
                post["sub"] = name
                post["priority"] = priority
                candidates.append(post)

        # Keyword search (limited to avoid rate limiting)
        searched = 0
        for keyword, theme_name in all_themes:
            searched += 1
            if searched > 8:  # cap to stay under Reddit rate limit
                break

            time.sleep(1.5)  # polite delay
            listing = fetch_subreddit_json(name, kind="search", q=keyword, limit=10)
            for post in extract_posts(listing):
                if post["id"] and post["id"] not in seen_ids:
                    seen_ids.add(post["id"])
                    post["sub"] = name
                    post["priority"] = priority
                    candidates.append(post)

    # Score
    scored = []
    for post in candidates:
        combined = post["title"].lower() + " " + post["selftext"].lower()

        matched_terms = []
        matched_themes = set()
        for keyword, theme_name in all_themes:
            if keyword.lower() in combined:
                matched_terms.append(keyword)
                matched_themes.add(theme_name)

        if not matched_terms:
            continue

        result = score_thread(post, post["priority"], config, matched_terms)
        if result is None:
            continue

        scored.append({
            "id": post["id"],
            "title": post["title"],
            "url": f"https://reddit.com{post['permalink']}",
            "subreddit": post["sub"],
            "score": result["total"],
            "age_hours": result["age_hours"],
            "num_comments": post["num_comments"],
            "upvotes": post["ups"],
            "matched_terms": matched_terms,
            "matched_themes": list(matched_themes),
            "selftext_snippet": (post["selftext"][:300] if post["selftext"] else ""),
            "suggested_angle": _suggest_angle(matched_themes, post["title"], matched_terms),
            "product_mention": _classify_product_mention(post["title"], post["selftext"]),
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:daily_limit]

    # Write outputs
    today = datetime.now().strftime("%Y-%m-%d")
    today_out = OUT_DIR / f"{today}"
    today_out.mkdir(parents=True, exist_ok=True)

    md_path = today_out / "report.md"
    json_path = today_out / "threads.json"

    _write_markdown(top, md_path, today, len(scored))

    with open(json_path, "w") as f:
        json.dump({"date": today, "threads": top, "total_candidates": len(scored)}, f, indent=2)

    print(f"\nDone. Wrote {len(top)} threads to:")
    print(f"  {md_path}")
    print(f"  {json_path}")
    return top


def _write_markdown(threads, path, date_str, total_candidates):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Community Monitor — {date_str}\n\n")
        if not threads:
            f.write("Nothing worth responding to today.\n"
                    f"({total_candidates} threads scanned, none passed the bar.)\n")
            return

        f.write(f"**{total_candidates} candidates** → surfacing top {len(threads)}\n\n")
        f.write("## Threads\n\n")
        for i, t in enumerate(threads, 1):
            f.write(f"### {i}. {t['title']}\n\n")
            f.write(f"| Field | Value |\n")
            f.write(f"|---|---|\n")
            f.write(f"| Subreddit | r/{t['subreddit']} |\n")
            f.write(f"| [URL]({t['url']}) | Score: **{t['score']}** |\n")
            f.write(f"| Age | {t['age_hours']}h | Comments: {t['num_comments']} |\n")
            f.write(f"| Themes | {', '.join(t['matched_themes'])} |\n")
            f.write(f"| Keywords | {', '.join(t['matched_terms'])} |\n")
            f.write(f"| Product mention | {t['product_mention']} |\n\n")
            f.write(f"**Suggested angle:** {t['suggested_angle']}\n\n")

            if t["selftext_snippet"]:
                f.write(f"**Context:**\n> {t['selftext_snippet']}\n\n")
            f.write("---\n\n")


if __name__ == "__main__":
    main()
