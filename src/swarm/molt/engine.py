#!/usr/bin/env python3
"""
Molt Engine v5 - Main Orchestrator Entry Point
Integrates ModelSwitcher, LoggingManager, and executes secure code mutation loops.
"""

import sys
import os
import argparse
import json
from pathlib import Path
from logging_manager import LoggingManager
from model_switcher import ModelSwitcher

# Define base workspace paths
ROOT_BASE = "/storage/emulated/0/RootBase"
LOG_DIR = os.path.join(ROOT_BASE, "molt_v5_log")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Molt Engine v5: Secure Recursive Optimization Engine")
    parser.add_argument("target", help="Path to the script undergoing evaluation/improvement")
    parser.add_argument("--instructions", type=str, required=True, help="Optimization directives for the engine")
    parser.add_argument("--iters", type=int, default=1, help="Number of recursive optimization loops")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # 1. Initialize Safety and System Monitoring Systems
    logger = LoggingManager(log_dir=LOG_DIR)
    switcher = ModelSwitcher()
    
    print(f"[+] Molt-V5 Initialized.")
    print(f"[+] Target Script: {args.target}")
    
    if not os.path.exists(args.target):
        print(f"[-] Error: Target file {args.target} does not exist.")
        sys.exit(1)

    # 2. Evaluate System Resources to Select Model Target
    selected_model = switcher.get_optimal_model()
    print(f"[+] System State Verified. Allocated Model: {selected_model}")

    # 3. Create Pre-Flight Safe Snapshot (.bak)
    backup_path = logger.create_backup(Path(args.target))
    if backup_path:
        print(f"[+] Pre-flight snapshot secured at: {backup_path}")
    else:
        print("[-] Critical: Backup failed. Aborting mutation loop for safety.")
        sys.exit(1)

        # 4. Read Target State to Pass to the Pipeline
    with open(args.target, 'r') as f:
        current_code = f.read()

    print(f"[+] Querying local execution engine via model: {selected_model}...")
    
    # Construct the payload for local Ollama API
    import requests
    
    prompt_payload = f"""
    You are an expert Python refactoring agent. Optimize the following code based on these instructions: {args.instructions}
    
    CRITICAL: You must return ONLY a raw, valid JSON object matching this exact schema. No markdown formatting, no ```json tags, no prose.
    {{
        "file": "{args.target}",
        "action": "replace_all",
        "content": "YOUR NEW Python CODE HERE (make sure newlines and quotes are properly escaped)"
    }}
    
    Code to optimize:
    {current_code}
    """

    response = dispatch_ollama_query(selected_model, prompt_payload)
    proposed_patch = parse_patch_response(response)
    
    validate_patch(proposed_patch, logger)
    stage_mutation(proposed_patch)
    check_arena_trigger()

def dispatch_ollama_query(model, prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "format": "json"},
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[-] Operational Failure: {e}")
        sys.exit(1)

def parse_patch_response(response_json):
    text = response_json.get("response", "").strip()
    return json.loads(text)

def validate_patch(patch, logger):
    print("[+] Run-time generation caught. Passing to AST validation suite...")
    if not logger.validate_syntax(patch["content"]):
        with open(os.path.join(LOG_DIR, "failed_ast_output.log"), "w") as f:
            f.write(patch["content"])
        print("[-] CRITICAL: AST validation failed.")
        sys.exit(1)

def stage_mutation(patch):
    import uuid
    arena_path = os.path.join(ROOT_BASE, "Molt-V5", "arena", "pending", f"mutation_{uuid.uuid4().hex[:8]}.json")
    with open(arena_path, 'w') as f:
        json.dump(patch, f)
    print(f"[+] Mutation staged in Arena: {arena_path}")

def check_arena_trigger():
    pending = os.listdir(os.path.join(ROOT_BASE, "Molt-V5", "arena", "pending"))
    if len(pending) >= 5:
        print(f"[!] ARENA CAPACITY REACHED. {len(pending)} mutations ready.")
    else:
        print(f"[+] Arena queue: {len(pending)}/5 mutations.")

if __name__ == "__main__":
    main()
