#!/usr/bin/env python3
"""
Mrs. Higgins Daemon
Runs shipping pipeline on schedule without cron
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

ROOTBASE = Path("/storage/emulated/0/RootBase")
STATE_FILE = ROOTBASE / "mrs_higgins_saas/state/daemon_state.json"
LOGDIR = ROOTBASE / "mrs_higgins_saas/logs"
LOGDIR.mkdir(parents=True, exist_ok=True)

# Schedule: every 6 hours
INTERVAL_SECONDS = 6 * 3600

class HigginsDaemon:
    def __init__(self):
        self.state_file = STATE_FILE
        self.load_state()
    
    def load_state(self):
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {"last_run": None, "runs": 0}
    
    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def should_run(self):
        if not self.state["last_run"]:
            return True
        
        last = datetime.fromisoformat(self.state["last_run"])
        now = datetime.now()
        return (now - last).total_seconds() >= INTERVAL_SECONDS
    
    def run_higgins(self):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        logfile = LOGDIR / f"higgins_run_{timestamp}.log"
        
        os.environ["LIGHTNING_ADDRESS"] = "ironicjewel052@walletofsatoshi.com"
        
        cmd = f"cd {ROOTBASE}/mrs_higgins_saas && python3 front_desk_lady.py"
        
        print(f"[{timestamp}] Running Mrs. Higgins...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        with open(logfile, 'w') as f:
            f.write(f"=== Mrs. Higgins Run: {timestamp} ===\n\n")
            f.write(result.stdout)
            if result.stderr:
                f.write(f"\n[STDERR]\n{result.stderr}")
        
        self.state["last_run"] = datetime.now().isoformat()
        self.state["runs"] += 1
        self.save_state()
        
        print(f"[{timestamp}] Run complete. Logged to: {logfile}")
        return result.returncode == 0
    
    def start(self):
        print("🚀 Mrs. Higgins Daemon Started")
        print(f"   Interval: {INTERVAL_SECONDS // 3600} hours")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            while True:
                if self.should_run():
                    self.run_higgins()
                else:
                    last = datetime.fromisoformat(self.state["last_run"])
                    next_run = last + timedelta(seconds=INTERVAL_SECONDS)
                    wait_secs = (next_run - datetime.now()).total_seconds()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Next run in {wait_secs // 60:.0f} minutes...")
                
                time.sleep(60)  # Check every minute if it's time to run
        
        except KeyboardInterrupt:
            print("\n\n[!] Daemon stopped.")
            sys.exit(0)

if __name__ == "__main__":
    daemon = HigginsDaemon()
    daemon.start()
