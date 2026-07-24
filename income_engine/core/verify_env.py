import os
import sys

REQUIRED_PATHS = [
    "/storage/emulated/0/RootBase/income_engine/core",
    "/storage/emulated/0/RootBase/income_engine/pipelines",
    "/storage/emulated/0/RootBase/income_engine/data/leads",
    "/storage/emulated/0/RootBase/income_engine/logs"
]

print("Checking engine environment configuration...")
all_clear = True

for path in REQUIRED_PATHS:
    full_path = os.path.expanduser(path)
    if os.path.exists(full_path):
        print(f"[OK] Found path: {path}")
    else:
        print(f"[MISSING] Path not resolved: {path}")
        all_clear = False

if not all_clear:
    print("Error: Missing expected directories. Run your directory layout block again.")
    sys.exit(1)
else:
    print("Environment verified. Read to initialize pipeline execution.")
