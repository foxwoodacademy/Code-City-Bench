import aiohttp
import time
import logging

logger = logging.getLogger("IncomeEngine.Auditor")

async def audit_live_endpoint(url):
    """
    Performs a real-time network request to a target business URL.
    Inspects headers and content size to find genuine optimization gaps.
    """
    if not url:
        return ["Missing primary digital asset (No website listed)"], 0
        
    # Standardize URL format
    target_url = url if url.startswith(("http://", "https://")) else f"https://{url}"
    logger.info(f"Initiating live production audit on endpoint: {target_url}")
    
    friction_points = []
    confidence_score = 0
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    }
    
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(target_url, headers=headers, timeout=12) as response:
                latency = time.time() - start_time
                content = await response.text()
                content_size_kb = len(content.encode('utf-8')) / 1024
                
                # Metric 1: Real-world latency bottlenecks
                if latency > 2.5:
                    friction_points.append(f"High initial server latency response ({latency:.2f}s delay)")
                    confidence_score += 35
                
                # Metric 2: Heavy asset payloads without compression
                if content_size_kb > 1500:
                    friction_points.append(f"Uncompressed homepage payload bottleneck ({content_size_kb:.1f} KB)")
                    confidence_score += 35
                    
                # Metric 3: Missing standard discoverability metadata tags
                if "<meta name=\"description\"" not in content.lower() and "<meta name='description'" not in content.lower():
                    friction_points.append("Missing standard SEO meta description tag attributes")
                    confidence_score += 30
                    
                if not friction_points:
                    friction_points.append("General conversion and schema presentation alignment")
                    confidence_score = 20
                    
                logger.info(f"Live audit complete for {url}. Found {len(friction_points)} genuine gaps.")
                return friction_points, confidence_score
                
        except aiohttp.ClientConnectorError:
            logger.warning(f"Connection refused or endpoint down for: {target_url}")
            return ["Target domain configuration or SSL certificate mismatch issues"], 50
        except Exception as e:
            logger.error(f"Network processing timeout or exception on {target_url}: {e}")
            return ["Unoptimized infrastructure or slow response fallback state"], 40
