#!/bin/bash
# Syntax AI — Live Demo
# "This is what runs in the background so you don't have to."

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
DIM='\033[2m'
RESET='\033[0m'

clear
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║${WHITE}         SYNTAX AI — BUSINESS ENGINE        ${CYAN}║${RESET}"
echo -e "${CYAN}║${DIM}      routing work so you don't have to     ${CYAN}║${RESET}"
echo -e "${CYAN}╚════════════════════════════════════════════╝${RESET}"
echo ""
sleep 1

steps=(
  "Scanning for new service requests..."
  "Lead detected: Upwork — 'emergency pipe repair, Wellington KS'"
  "Qualifying lead... budget confirmed, timeline urgent"
  "Drafting response... personalized to request"
  "Invoice generated: \$285 — sent via Lightning / standard"
  "Job logged. Follow-up scheduled: 48hrs"
  "Routing complete. You just got a customer."
)

for step in "${steps[@]}"; do
  echo -ne "${GREEN}  ▶ ${WHITE}${step}${RESET}"
  sleep 0.8
  echo -e "${GREEN}  ✓${RESET}"
  sleep 0.4
done

echo ""
echo -e "${YELLOW}  ┌─────────────────────────────────────┐${RESET}"
echo -e "${YELLOW}  │  Jobs routed today:        3        │${RESET}"
echo -e "${YELLOW}  │  Invoices sent:            3        │${RESET}"
echo -e "${YELLOW}  │  Follow-ups scheduled:     3        │${RESET}"
echo -e "${YELLOW}  │  Your time spent:          0 min    │${RESET}"
echo -e "${YELLOW}  └─────────────────────────────────────┘${RESET}"
echo ""
echo -e "${DIM}  Running on your phone. No subscription. No middleman.${RESET}"
echo ""
