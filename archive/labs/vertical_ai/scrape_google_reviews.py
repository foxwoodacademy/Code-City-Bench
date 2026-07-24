#!/usr/bin/env python3
"""Scrape Google Business reviews to find high-rated businesses without websites."""

import requests
from bs4 import BeautifulSoup
import csv
import time

# Configure headers to mimic a browser visit
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_google_reviews(search_query, location, num_businesses=10):
    """Search for businesses and scrape their reviews."""
    search_url = f"https://www.google.com/search?q={search_query}+{location}&tbm=lcl"
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    businesses = []
    for result in soup.select('.Nv2PK')[:num_businesses]:
        name = result.select_one('.dbg0pd').text if result.select_one('.dbg0pd') else "N/A"
        rating = result.select_one('.YDIN4c').text if result.select_one('.YDIN4c') else "N/A"
        reviews_count = result.select_one('.UY7F9').text if result.select_one('.UY7F9') else "N/A"
        website = result.select_one('.lcr4fd.S9kvJb a')['href'] if result.select_one('.lcr4fd.S9kvJb a') else "No Website"
        
        businesses.append({
            "name": name,
            "rating": rating,
            "reviews_count": reviews_count,
            "website": website,
        })
        
    return businesses

def save_to_csv(businesses, filename="businesses_without_websites.csv"):
    """Save the scraped data to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "rating", "reviews_count", "website"])
        writer.writeheader()
        writer.writerows(businesses)

def main():
    search_query = "restaurants"
    location = "New York"
    
    print(f"Scraping Google Business reviews for {search_query} in {location}...")
    businesses = get_google_reviews(search_query, location)
    
    # Filter businesses without websites
    businesses_without_websites = [b for b in businesses if b["website"] == "No Website"]
    
    print(f"Found {len(businesses_without_websites)} businesses without websites.")
    save_to_csv(businesses_without_websites)
    print("Data saved to businesses_without_websites.csv")

if __name__ == "__main__":
    main()
