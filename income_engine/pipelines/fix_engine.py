import os
import json
import logging
from pathlib import Path
import http.client

logger = logging.getLogger("ModMind.FixEngine")

def check_local_inference_port() -> bool:
    """Probes the local system port loopback to verify if Ollama is actively serving."""
    try:
        conn = http.client.HTTPConnection("127.0.0.1", 11434, timeout=None)
        conn.request("GET", "/api/tags")
        response = conn.getresponse()
        if response.status == 200:
            return True
    except Exception:
        pass
    return False

def generate_local_model_fix(business_name: str, friction: str) -> dict:
    """
    Synchronous worker block that calls your local local llama3.2:1b instance
    to write structural, production-ready optimization tags.
    """
    logger.info(f"Ollama port detected active. Requesting edge asset compile for: {business_name}")
    
    prompt = (
        f"You are a local-first enterprise SEO web optimization script agent.\n"
        f"Write a raw, optimized JSON-LD schema block or HTML meta tag element for this business:\n"
        f"Business: {business_name}\n"
        f"Problem: {friction}\n\n"
        f"Output ONLY the raw code or tag content string. Do not include markdown accents, code fences, or chat text."
    )
    
    payload = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        conn = http.client.HTTPConnection("127.0.0.1", 11434, timeout=None)
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/api/generate", json.dumps(payload), headers)
        response = conn.getresponse()
        
        if response.status == 200:
            raw_data = response.read().decode('utf-8')
            result = json.loads(raw_data)
            generated_code = result.get("response", "").strip()
            return {"seo_optimization_patch.html": generated_code}
    except Exception as e:
        logger.warning(f"Edge generation cycle missed. Fallback to clean template baseline. Error: {e}")
    
    return {}

def generate_remediation_package(profile: dict) -> tuple:
    """
    Enterprise entry point for building solution directories.
    Wires up your local model inferences dynamically if your port is hot.
    """
    business_name = profile.get("name", "Unknown_Business")
    frictions = profile.get("friction_points", [])
    
    # Standardize directory name syntax
    clean_name = business_name.lower().replace(" ", "_").replace("-", "_")
    target_dir = Path(f"/storage/emulated/0/RootBase/income_engine/data/leads/fixes_{clean_name}")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    compiled_assets = []
    payload_matrix = {}
    
    # If Ollama is hot, let your local model write the solutions right now
    if check_local_inference_port() and frictions:
        for friction in frictions:
            model_fixes = generate_local_model_fix(business_name, friction)
            payload_matrix.update(model_fixes)
    else:
        # Static baseline templates if the local service is offline
        if any("meta description" in f.lower() for f in frictions):
            payload_matrix["seo_local_schema.json"] = json.dumps({
                "@context": "https://schema.org",
                "@type": "AutomotiveBusiness",
                "name": business_name,
                "description": f"Professional automotive diagnostic and mechanical optimization utilities for {business_name}."
            }, indent=4)

    # Write generated payloads to your storage partition
    for filename, code_content in payload_matrix.items():
        file_path = target_dir / filename
        with open(file_path, "w") as f:
            f.write(code_content)
        compiled_assets.append(filename)
        
    return str(target_dir), compiled_assets
