# AI Boardroom: Orchestration Blueprint

## 1. System Overview
The **MotherBrain** acts as the central hub, maintaining the **Operational State** (Persona + Decision Hat). The swarm acts as a distributed cognitive framework that translates raw market inputs into high-level strategic boardroom insights.

## 2. Agent Roles
- **MarketScout**: Continuous scraper. Ingests raw data (price points, demand volumes) and publishes to `market.data`.
- **StrategicAnalysisAgent (StratAnalyst)**: The "Brain". Consumes `market.data` + `OperationalState`. Uses Ollama to project pain points and business model pivots. Stores insights in SQLite.
- **ForecasterAgent (MarketOracle)**: Performs time-series forecasting on data extracted from `StratAnalyst`'s database. Projects demand/cost fluctuations 14 days out.
- **PlotterAgent (ChartMaster)**: Consumes projections from `ForecasterAgent` and returns base64 PNG charts.
- **Boardroom Dashboard (Swarm UI)**: Visual interface for human interaction, state toggling (Hats/Personas), and displaying charts.

## 3. Atomic Data Flow
1. **Trigger**: User selects a "Thinking Hat" or Persona in the **Swarm UI**.
2. **State Broadcast**: `MotherBrain` updates `OperationalState` $\rightarrow$ Broadcasts `system.operational_state_change`.
3. **Agent Reaction**: All agents receive the state and update their `instruction_modifier` / sensitivity.
4. **Task Execution**:
   - `MarketScout` feeds current market state to `StratAnalyst`.
   - `StratAnalyst` computes insights based on the current Hat.
   - `ForecasterAgent` calculates trends.
   - `PlotterAgent` renders the visual report.
5. **Dashboard Update**: `MotherBrain` streams the insight + visual report to the `Swarm UI`.

## 4. Operational State Mapping
| Decision Hat | Primary Strategic Focus | Agent Sensitivity |
| :--- | :--- | :--- |
| **White** | Data/Accuracy | High (Metrics focus) |
| **Red** | Emotion/Sentiment | High (Aggressive sentiment capture) |
| **Black** | Risk/Caution | High (Strict compliance/Cautions) |
| **Yellow** | Value/Growth | High (Aggressive opportunity spotting) |
| **Green** | Creativity/Pivot | High (Novel model generation) |
| **Blue** | Orchestration | High (Process efficiency) |

## 5. Deployment Readiness
- **Core Orchestration**: Done.
- **Persistent State**: Done (SQLite).
- **Cognitive Layer**: Done (Ollama + Six Hats).
- **Visualization**: Done (Matplotlib).
- **Interface**: Done (Swarm UI Control Panel).
