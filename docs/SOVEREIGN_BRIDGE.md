# ModMind Bridge: The 'N4N' (Navigation 4 Noobs) Protocol

## 🎯 The Goal
Enable absolute simplicity for non-technical partners to monitor, navigate, and receive the 'brains' of the system without touching a terminal.

## 🛠 The Technical Stack
- **Transport**: Nostr (NIP-01/NIP-30078) for asynchronous, serverless state streaming.
- **Frontend**: Lightweight Flask + Vanilla CSS ( Served as a local web-app on Termux).
- **Sync**: State-event broadcasting (Session logs, revenue updates, and 'Thought' streams).

## 🎨 Visual Separation (The 'Thought' Layer)
To prevent cognitive overload, the bridge parses LLM responses into two distinct visual streams:
1. **The Void (Thoughts)**: 
   - *Styling*: Italic, dimmed gray, smaller font, enclosed in a 'thinking' container.
   - *Source*: Everything inside `<thought>` or `(thinking...)` tags.
2. **The Word (Output)**: 
   - *Styling*: Bold, high contrast, standard size.
   - *Source*: The final actionable response.

## 🗺 Cartographer/N4N Integration
The 'Cartographer' acts as a visual map of the agent's current 'Location' in the task-tree.
- **Input**: Agent state updates (`current_task`, `sub_goal`, `confidence_score`).
- **Output**: A simple breadcrumb UI: `SaaS Pipeline` -> `Mrs. Higgins` -> `Lead Scouting` -> `Analyzing Upwork`.
- **Control**: Simple 'Yes/No' buttons on Mel's dashboard that send a Nostr event back to the primary device to trigger/halt actions.

## 🔄 Session Sync
- **Log Streaming**: Real-time tail of the session log pushed to the relay.
- **File Mirroring**: Key session files (e.g., `income_summary.json`) are base64 encoded into Nostr events or hosted on a temporary local HTTP server that the bridge can fetch.

## 🛡 API Security & Anti-Ban Logic
To prevent 'Account Sharing' or 'Sybil' flags from API providers:
- **Distributed Key Mapping**: The system does NOT share a single API session. It maps `ModMind Pubkey` $\rightarrow$ `Individual API Key`. Each user/team utilizes their own provisioned resources.
- **Local-First Priority**: High-volume tasks are routed to local Ollama models to minimize cloud API footprint.
- **Traffic Jitter**: The `Concierge` layer implements random request spacing (jitter) to avoid rhythmic bot-patterns.
- **IP Consistency**: Execution remains device-local to maintain a natural mobile IP profile.
