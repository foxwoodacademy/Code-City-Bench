# ⚡ Passive Income Swarm: QRD (Quick Reference Document)

*The 10x Developer’s Playbook for Autonomous Value Generation.*

## 1. Core Objectives
This swarm is designed to turn the MotherBrain into an autonomous revenue engine. It continuously scouts freelance markets, identifies trends, manages SaaS deployment, and handles value exchange via Nostr/LNbits.

## 2. Agent Playbook
- **MarketScout**: Monitors Reddit (r/freelance, r/forhire), Upwork, and Fiverr for high-intent requests.
- **StratAnalyst**: Processes scraped data to identify lucrative "gaps" in the market.
- **Forecaster**: Predicts the saturation levels and potential income volatility for a specific freelance niche or SaaS idea.
- **Plotter**: Generates visual ROI charts for your blue-sky meetings.

## 3. Operational Workflow (The "Money Loop")
1.  **Scout**: `MarketScout` posts to the `task_queue` whenever a high-paying job or low-competition niche appears.
2.  **Analyze**: `MotherBrain` triggers `StratAnalyst`. Set your **Thinking Hat** to `YELLOW` (Optimism) for brainstorming, then `BLACK` (Caution) for feasibility.
3.  **Act**: If a high-viability lead is found, the agent prepares a drafted response or pivot plan.
4.  **Transaction**: Integrated with **Nostr/LNbits** to handle micropayments or automated invoicing.

## 4. Power User Commands
```bash
# Boot the boardroom
cd janebot-motherbrain
PYTHONPATH=. python scripts/passive_income_sim.py

# Switch to 'Green Hat' for innovative SaaS pivots
curl -X POST http://localhost:8765/api/mode -d '{"mode": "GREEN"}'

# Trigger an immediate boardroom report
curl -X POST http://localhost:8765/api/task -d '{"capability": "analyze_pain_points", "data": "freelance_scout_report"}'
```

## 5. Expansion Suggestions (v2)
- **Automatic Code Deployment**: Agents that push MVP code to Vercel/Fly.io automatically upon project approval.
- **Agent Self-Scaling**: Agents that clone themselves based on task queue depth (e.g., spawn 5 more `MarketScout` agents when Reddit traffic spikes).
- **Sentiment-Driven Bidding**: Real-time sentiment analysis of freelance leads to adjust your persona (`JaneBot` vs `EquiLex`) dynamically for the best closing rate.
- **Distributed Vaults**: Automated LNbits wallet management per agent project.

---
*Stay modular, stay autonomous, and watch the pipeline.*
