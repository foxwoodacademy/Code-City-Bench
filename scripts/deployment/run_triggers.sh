#!/bin/bash
# Updated Trigger executor for passive_income_swarm
while true; do
  /storage/emulated/0/RootBase/zeroclaw_marketplace_final/passive_income_swarm/control/inbox/call_mrs_higgins.sh
  /storage/emulated/0/RootBase/zeroclaw_marketplace_final/passive_income_swarm/control/inbox/run_dominance_cycle.sh
  sleep 3600
done
