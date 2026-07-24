import subprocess, sys, os
sys.path.insert(0, "/storage/emulated/0/RootBase/askhole_autopilot/lib")
from state_engine import State

MRS = "/storage/emulated/0/RootBase/mrs_higgins_saas"
VAI = "/storage/emulated/0/RootBase/vertical_ai"

def run(cmd, cwd=MRS, timeout=300):
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=timeout, cwd=cwd
        )
        State().trigger("exec", {
            "cmd": cmd,
            "rc": r.returncode,
            "out": r.stdout[:500]
        })
        return r
    except Exception as e:
        State().trigger("error", {"cmd": cmd, "err": str(e)})
        return None

def pipeline(dry=False, platform=None):
    c = f"bash {MRS}/mrs_higgins.sh"
    if dry:      c += " --dry-run"
    if platform: c += f" --platform {platform}"
    return run(c)

def bookkeeper():
    return run(f"python3 {MRS}/bookkeeper.py")

def copywriter(pkg, platform):
    return run(f"python3 {MRS}/copywriter.py --package {pkg} --platform {platform}")

def scout(target):
    return run(f"python3 {VAI}/scouts/swarm_intel.py --query {target}", cwd=VAI)
