import trafilatura
from duckduckgo_search import DDGS
from langchain.tools import tool

# --- FOSS SEARCH ENGINE ---
@tool
def search_tool(query: str) -> str:
    """
    Performs a free, private web search using DuckDuckGo.
    Use this for finding general information, news, and source links.
    """
    print(f"\n[Agent searching: {query}]\n")
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        # Format results as a simple string for the LLM
        return "\n".join([f"{r['title']}: {r['href']}" for r in results])

# --- FOSS SCRAPER ENGINE ---
@tool
def scrape_web_data(url: str) -> str:
    """
    Scrapes a specific URL and returns the content in clean text/markdown format.
    Uses trafilatura for high-quality extraction.
    """
    print(f"\n[Agent reading: {url}]\n")
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            content = trafilatura.extract(downloaded, include_formatting=True)
            return content[:15000] if content else "Could not extract content."
        return "Failed to fetch the URL."
    except Exception as e:
        return f"Failed to scrape the source. Error: {str(e)}"

# --- TEST ---
if __name__ == "__main__":
    print("Testing FOSS Tools...")
    search_res = search_tool.invoke({"query": "UK inflation report May 2026"})
    print(f"Search result: {search_res}")
    
    # Example URL extraction (if search returned links)
    # result = scrape_web_data.invoke({"url": "..."})
    print("\nTools ready for agent integration.")
