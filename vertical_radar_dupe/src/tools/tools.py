from duckduckgo_search import DDGS
from langchain.tools import tool
import trafilatura
import time

@tool
def search_tool(query: str) -> str:
    """
    Performs a web search using DuckDuckGo. Includes retry logic.
    """
    print(f"\n[Agent searching: {query}]")
    for attempt in range(3):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if not results:
                    return "No results found."
                return "\n".join([f"{r['title']}: {r['href']}" for r in results])
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
            
    # Fallback to user override if automated search fails
    override = input(f"\n[MANUAL OVERRIDE] Automated search failed for: '{query}'. Enter a manual search URL or query (or press Enter to skip): ")
    if override:
        return f"Manual Query: {override}"
    return "Search failed after retries."

@tool
def scrape_web_data(url: str) -> str:
    """
    Scrapes a URL using trafilatura.
    """
    # If the user provided a manual query, just return a prompt
    if url.startswith("Manual Query: "):
        return f"Please research the topic: {url}"
        
    print(f"[Agent reading: {url}]")
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded, include_formatting=True) or "Extraction failed."
    return "Failed to fetch URL."
