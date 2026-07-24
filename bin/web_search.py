"""
VERTICAL AI — Web Search Scout
DuckDuckGo search. No API key. No rate limit surprises.
Pulls real web signals on any target.
"""

import json
import sys
from typing import Optional


def search(query: str, max_results: int = 5) -> list[dict]:
    """
    Live DuckDuckGo search. Returns list of result dicts.
    Falls back gracefully if duckduckgo_search not installed.
    """
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "source": "duckduckgo"
                }
                for r in results
            ]
    except ImportError:
        return [{"error": "duckduckgo_search not installed — run: pip install duckduckgo-search --break-system-packages"}]
    except Exception as e:
        return [{"error": f"Search failed: {e}"}]


def get_business_signals(business_name: str, location: Optional[str] = None) -> dict:
    """
    Pulls web signals relevant to a business target.
    Runs multiple targeted queries and aggregates results.
    """
    queries = [
        f"{business_name} reviews complaints",
        f"{business_name} {location} news" if location else f"{business_name} news 2024 2025",
        f"{business_name} website contact"
    ]

    all_results = []
    for query in queries:
        results = search(query, max_results=3)
        all_results.extend(results)

    # Deduplicate by URL
    seen = set()
    unique = []
    for r in all_results:
        url = r.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(r)

    # Flag signals
    opportunity_flags = []
    risk_flags = []

    for r in unique:
        snippet = (r.get("snippet") or "").lower()
        title = (r.get("title") or "").lower()
        combined = snippet + title

        if any(w in combined for w in ["lawsuit", "fraud", "scam", "complaint", "violation", "fine", "penalty"]):
            risk_flags.append(f"Negative signal: {r.get('title', '')[:80]}")
        if any(w in combined for w in ["award", "best", "top rated", "certified", "expanding", "hiring"]):
            opportunity_flags.append(f"Positive signal: {r.get('title', '')[:80]}")
        if "no website" in combined or "doesn't have a website" in combined:
            opportunity_flags.append("Confirmed: no web presence detected in search results")

    return {
        "business": business_name,
        "location": location,
        "results": unique,
        "result_count": len(unique),
        "risk_flags": risk_flags,
        "opportunity_flags": opportunity_flags
    }


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "Mike's Plumbing Phoenix"
    print(f"Searching web signals for: {target}")
    result = get_business_signals(target)
    print(json.dumps(result, indent=2))
