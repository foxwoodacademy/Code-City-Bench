#!/bin/bash
# SOURCE: /storage/emulated/0/RootBase/scripts/setup/initialize.sh
# AUTHOR: foxwoodacademy
# PURPOSE: Validate RootBase workspace from WORKSPACE.manifest

MANIFEST="/storage/emulated/0/RootBase/WORKSPACE.manifest"
ROOTBASE="/storage/emulated/0/RootBase"

echo "Validating WORKSPACE.manifest..."
[ -f "$MANIFEST" ] && echo "  OK: WORKSPACE.manifest" || echo "  MISSING: WORKSPACE.manifest"

echo "Checking CORE paths..."
[ -f "$ROOTBASE/Loosies/MOTHERBRAIN-1.sh" ] && echo "  OK: MOTHERBRAIN" || echo "  MISSING: MOTHERBRAIN"

echo "Checking SHIPPING paths..."
[ -f "$ROOTBASE/mrs_higgins_saas/front_desk_lady.py" ] && echo "  OK: front_desk_lady.py" || echo "  MISSING: front_desk_lady.py"

echo "Checking VAULT paths..."
[ -f "$ROOTBASE/Official-Vertical-AI-Boardroom/concierge.py" ] && echo "  OK: concierge.py" || echo "  MISSING: concierge.py"

echo "Checking DAEMON paths..."
[ -f "$ROOTBASE/scripts/utilities/higgins_daemon.py" ] && echo "  OK: higgins_daemon.py" || echo "  MISSING: higgins_daemon.py"

echo ""
echo "Workspace validation complete."
