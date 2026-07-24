# SYNTAX -- CLI AI Warden
## Status: Starting fresh in Whorl project
## Date: June 1 2026

### What it is
Terminal-native AI coding assistant for Termux Android.
Better than aria-termux. Named Syntax.
Lives in Whorl as the CLI tunnel digger / AI warden component.

### Stack (confirmed working today)
- Cerebras: gpt-oss-120b -- 1M tokens/day free -- WORKING
- Mistral: mistral-large-latest -- WORKING  
- OpenRouter: nvidia/nemotron-3-super-120b-a12b:free -- WORKING
- Fireworks: $5 credit -- WORKING
- Groq: rate limited but working
- Gemini: rate limited

### Keys location
/storage/emulated/0/RootBase/Official-Vertical-AI-Boardroom/.env
/storage/emulated/0/RootBase/Askhole-Too-Also/V3/.env

### AskHole status
WORKING -- Cerebras and Mistral firing
Location: /storage/emulated/0/RootBase/Askhole-Too-Also/V3/
Good outputs for: plumber, hvac, restaurant, dealership, bank

### Vertical AI Boardroom
WORKING -- v1.4 committed
Concierge failover wired in
Location: /storage/emulated/0/RootBase/Official-Vertical-AI-Boardroom/

### Yvette
Knowledge base built
Demo site built: chew_plumbing.html
Price: $199/month, 30 day guarantee

### Tomorrow
- Chew Plumbing first thing
- Big Cheese after lunch  
- RCB Bank before 4pm

### Syntax next session goals
- Rich terminal UI
- Gemini + Cerebras + Mistral multi-provider
- File ingestion (-f flag)
- Persistent chat loop
- Domain detection (ml/web/cyber/auto)
- Whorl integration
