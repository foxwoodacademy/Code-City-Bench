import aiohttp
import json
import logging

logger = logging.getLogger("IncomeEngine.Ingest")

async def fetch_local_businesses(query, location="37.2684,-97.3976", radius=25000):
    """
    Queries live open-source business listings using OpenStreetMap Overpass API.
    Broadened taxonomy to capture regional repair nodes, dealerships, and shops.
    """
    logger.info(f"Targeting LIVE Overpass extraction for broad search: '{query}'...")
    
    lat, lon = location.split(",")
    
    # Broaden the query to pull repair centers, car repair, and tool shops globally in the radius
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="car_repair"](around:{radius},{lat},{lon});
      way["amenity"="car_repair"](around:{radius},{lat},{lon});
      node["shop"="car_repair"](around:{radius},{lat},{lon});
      way["shop"="car_repair"](around:{radius},{lat},{lon});
      node["shop"="motorcycle"](around:{radius},{lat},{lon});
      way["shop"="motorcycle"](around:{radius},{lat},{lon});
    );
    out tags center;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data={"data": overpass_query}) as response:
                if response.status == 200:
                    data = await response.json()
                    elements = data.get("elements", [])
                    
                    cleaned_leads = []
                    for el in elements:
                        tags = el.get("tags", {})
                        
                        # Only ingest items that have a verified name assigned
                        if "name" in tags:
                            addr_city = tags.get("addr:city", "Local Area")
                            addr_street = tags.get("addr:street", "")
                            
                            # Synthesize notes based on real OSM profile properties
                            notes_parts = []
                            if not tags.get("website") and not tags.get("contact:website"):
                                notes_parts.append("No active web asset detected in public listing mapping.")
                            if not tags.get("phone") and not tags.get("contact:phone"):
                                notes_parts.append("Missing primary direct contact phone attribute.")
                                
                            notes_str = " ".join(notes_parts) if notes_parts else "Basic structural elements present."
                            
                            cleaned_leads.append({
                                "name": tags.get("name"),
                                "email": tags.get("email", None),
                                "phone": tags.get("phone", tags.get("contact:phone", "N/A")),
                                "website": tags.get("website", tags.get("contact:website", "")),
                                "notes": f"OSM ID: {el.get('id')}. {notes_str} Address: {addr_street}, {addr_city}."
                            })
                    
                    return cleaned_leads
                else:
                    logger.error(f"Overpass API returned network error status: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Failed live data ingestion through Overpass: {e}")
            return []
