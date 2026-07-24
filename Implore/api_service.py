from fastapi import FastAPI, HTTPException
from workflow import app as workflow_app
import uvicorn
import uuid
import os
import json
import glob
from datetime import datetime
from path_resolver import resolver

app = FastAPI(title="Implore Grant Intelligence Service")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/telemetry")
async def get_telemetry():
    """Aggregates telemetry from the ecosystem_bridge."""
    bridge_dir = resolver.resolve("ecosystem_bridge")
    telemetry = {"agents": [], "system_status": "STABLE"}
    
    if not os.path.exists(bridge_dir):
        os.makedirs(bridge_dir)

    for file_path in glob.glob(os.path.join(bridge_dir, "*.json")):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                telemetry["agents"].append(data)
            except:
                pass
    return telemetry

@app.post("/trigger")
async def trigger_action(action: str, params: dict = {}):
    """General trigger for swarmH actions (e.g., 'start_scan', 'reset_governance')."""
    if action == "start_scan":
        directory = params.get("directory", ".")
        # In a real scenario, this would trigger the pipeline asynchronously
        return {"status": "initiated", "action": "pipeline_start", "target": directory}
    elif action == "ping":
        return {"status": "pong", "timestamp": datetime.utcnow().isoformat()}
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")

@app.post("/run-pipeline")
async def run_pipeline(directory: str):
    # Trigger the LangGraph workflow
    result = workflow_app.invoke({"messages": [], "data": {"directory": directory}})
    data = result["data"]
    
    # Map to standardized schema
    response = {
        "status": "success",
        "pipeline_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "project_metrics": {
            "code_fitness_score": 0.92, # Placeholder
            "grant_readiness": 0.85,    # Placeholder
            "key_technologies": ["python", "langgraph", "fastapi"]
        },
        "grant_match": {
            "id": data["opportunity"].get("id"),
            "title": data["opportunity"].get("title"),
            "relevance_score": 0.95, # Placeholder
            "intent_alignment": "high",
            "funder": data["opportunity"].get("agency")
        },
        "generated_artifacts": {
            "narrative_url": f"http://implore-host:8000/artifacts/{data['opportunity'].get('id')}.txt",
            "sf424_json": data.get("forms", {}).get("sf424", {})
        },
        "audit_trail": {
            "status": "passed" if data.get("audit_passed") else "failed",
            "verification_timestamp": datetime.utcnow().isoformat()
        }
    }
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
