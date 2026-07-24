import subprocess
import json
import requests
import os
import sys

# Add RootBase paths to sys.path to allow importing from other projects
# In a real scenario, these should be managed via a proper environment/venv
sys.path.append('/storage/emulated/0/RootBase/project_bundle_20260513_120226/datacampus')

try:
    from datacampus import runtime as dc_runtime
except ImportError:
    dc_runtime = None

class ZeroClawAdapter:
    """Wraps the ZeroClaw Lab Broker CLI for quick task management."""
    CLI_PATH = "/storage/emulated/0/RootBase/project_bundle_20260513_120226/project_incubator/zeroclaw_lab_broker"

    @staticmethod
    def _run_cli(args):
        cmd = ["python", "-m", "zeroclaw_lab_broker.cli"] + args
        result = subprocess.run(cmd, cwd=ZeroClawAdapter.CLI_PATH, capture_output=True, text=True)
        if result.returncode != 0:
            return {"error": result.stderr}
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout

    def create_task(self, assignment_id, lab_id, capabilities, risk="low"):
        cap_args = []
        for c in capabilities:
            cap_args.extend(["--capability", c])
        
        return self._run_cli(["create-task", "--assignment-id", assignment_id, "--lab-id", lab_id] + cap_args + ["--risk-level", risk])

    def get_status(self):
        return self._run_cli(["status"])

    def list_open_tasks(self):
        return self._run_cli(["open-tasks"])

class LoughAdapter:
    """Interfaces with the Lough field_server for event emitting and polling."""
    BASE_URL = "http://localhost:7070"

    def emit(self, event_type, payload, source="thoth", location="orchestrator"):
        data = {
            "event_type": event_type,
            "payload": payload,
            "source": source,
            "location": location
        }
        try:
            response = requests.post(f"{self.BASE_URL}/emit", json=data, timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def poll(self, limit=10):
        try:
            response = requests.get(f"{self.BASE_URL}/poll", params={"limit": limit}, timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class DataCampusAdapter:
    """Wraps DataCampus runtime for curriculum and student management."""
    def __init__(self):
        if dc_runtime is None:
            print("[WARN] DataCampus runtime not found. Some functions will be disabled.")

    def create_assignment(self, cohort_id, lab_id, source="Artificial-Criminal"):
        if not dc_runtime: return {"error": "DataCampus runtime unavailable"}
        return dc_runtime.create_assignment(cohort_id, lab_id, source_project=source)

    def create_student(self, name, metadata=None):
        if not dc_runtime: return {"error": "DataCampus runtime unavailable"}
        return dc_runtime.create_student(name, metadata)

    def import_lab(self, manifest):
        if not dc_runtime: return {"error": "DataCampus runtime unavailable"}
        return dc_runtime.import_lab_manifest(manifest)

# Singleton instances for easy access
zeroclaw = ZeroClawAdapter()
lough = LoughAdapter()
datacampus = DataCampusAdapter()
