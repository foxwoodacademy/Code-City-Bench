#!/bin/bash
# RootBase "The Great Reset" Oneshot - v1.0
# Orchestrates Mrs. Higgins and Firefly Scout for autonomous revenue generation.

LOG_FILE="logs/oneshot_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

log() { echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

log "🚀 Initializing RootBase Autonomous Pipeline..."

# 1. Environment Check
if [ ! -f ".env" ]; then
    log "ERR: .env file missing. Please configure API keys."
    exit 1
fi

# 2. Scout Phase (Harvesting)
log "🔍 Launching Afirefly Scouts (FireflyScout)..."
# Running scout in a single-pass mode for the oneshot
python3 src/saas/higgins/firefly_scout.py --oneshot || log "WARN: Scout encountered an issue."

# 3. Aggregation & Intelligence Phase
log "🧠 Aggregating leads and performing AI Analysis..."
# This would call the 'Thoth' or 'Briefing' logic to analyze firefly_leads.json
python3 src/saas/higgins/briefing.py || log "WARN: Analysis phase skipped."

# 4. Revenue Tending (Invoicing/Closing)
log "💰 Tending revenue generative automations..."
python3 src/saas/higgins/the_ledger.py --reconcile
python3 src/saas/higgins/the_closer.py --notify

log "✅ Oneshot execution complete. Checking logs for metrics."
cat logs/income_summary.json 2>/dev/null | grep "total_revenue" || log "INFO: No new revenue reconciled this run."
