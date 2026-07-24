# THE CONVERGENCE
## BleakNarratives / RootBase Architecture Decision Record
### Date: June 1 2026
### Status: PRE-SHIP. Everything exists. Now we choose.

---

## THE LINEAGE (what we're breeding)

These things exist and are working. The question is how they fuse:

| Project | What it actually is |
|---|---|
| **DeepTutor** | Pedagogical AI — explains, teaches, scaffolds learning |
| **Goose AI** | Agentic executor — does tasks autonomously |
| **ARIA / aria-termux** | Terminal AI assistant (the one we're replacing with Syntax) |
| **JaneBot MotherBrain** | Swarm orchestrator — coordinates heterogeneous agent fleet |
| **Molt / MoltBleak** | Process supervision engine — keeps workers alive |
| **Whorl** | Recursive pattern analysis + structural validation |
| **Syntax** | CLI AI warden — multi-provider, terminal-native |
| **CodeMentor MVP** | AI tutoring system — progression engine, skill trees |
| **Mrs. Higgins** | SaaS front office — routing, invoicing, lead closing |
| **Firefly Scouts** | Recon agents — scrape, find, report back |
| **Lough** | Event spine / audit log — the truth layer |
| **ZeroClaw** | Labor market — task claims, execution, evidence |
| **Nat / NatHub** | Intent-based version control — tracks WHY not just WHAT |
| **GRIMOIRE** | Terminal OS layer — the shell everything lives inside |
| **Code City** | Architectural visualization / agentic city-building workbench |
| **Veritas Engine** | Truth verification + logical auditing |

---

## THE VERTICALS (what we're actually selling)

This is the Vertical AI model. Same engine. Different skin. Different disclaimer.

### 1. VERTICAL AI CORE (existing — WORKING)
General business intelligence. AskHole. Boardroom panel.

### 2. LEGAL AI (new vertical)
**Name TBD** — something with weight. Not "LegalBot."
- Contract review, clause flagging, demand letter drafting
- CFPB complaint generation (cfpb.py already exists in RootBase)
- Jurisdiction-aware responses
- **Disclaimer layer**: "This is not legal advice. Consult an attorney."
- **Stack note**: Veritas Engine is literally built for this. Wire it in.
- **Revenue**: $299/month. Law firms pay. Defendants pay more.

### 3. CODEBASE AI (new vertical)
Working title: **"The Workbench"** — for nerds who don't touch grass
- Code review, architecture critique, refactor suggestions
- CodeMentor MVP becomes a module — skill trees, progression
- Syntax AI lives here as the CLI tunnel (or API callout for hosted)
- Code City Workbench is the visual layer
- **Stack note**: This IS the Whorl + Loom + DataWeaver use case
- **Revenue**: $149/month dev tier, $399/month team tier

### 4. HEALTH AI (new vertical)
You said sue me until I float — noted and respected.
- Symptom triage, medication interactions, care navigation
- **Disclaimer**: "Not a doctor. Not medical advice. Go see someone."
- The disclaimer IS the product honestly — people know, they just want a second opinion at 2am
- **Revenue**: $99/month consumer, $499/month clinic white-label

### 5. FINANCIAL AI (new vertical)
- Portfolio analysis, business planning, invoice strategy
- Mrs. Higgins is already half of this
- **Revenue**: $199/month

---

## THE CORE QUESTION: WHAT IS THE ACTUAL PLATFORM?

Before we write another line of code we need to answer this.
Pick one answer per row. Then we build toward it.

### DATABASE
**Options:**
- **MongoDB** — flexible schema, JSON-native, good for agentic logs and varied vertical data. Runs on Android via Termux with some pain.
- **SQLite** — already in use (memory.db, system_checkpoints.db). Zero config. Works everywhere. Limited concurrency.
- **PostgreSQL** — production-grade, relational, scales. Heavier.
- **Own format** — JSONL flat files (Lough already does this). Simple. Auditable. No query power.

**Recommendation**: 
- **SQLite now** (you already have it, it works, Lough uses it)
- **PostgreSQL later** when you have a paying customer who needs multi-user
- **MongoDB** only if the data gets truly unstructured at scale
- Do NOT build a custom DB. Nat/NatHub is version control, not a database.

### STACK
**Options:**
- **Python everywhere** — you know it, everything's already in it, Termux runs it
- **Python backend + HTML/JS frontend** — the current pattern (boardroom, code city, etc.)
- **Node/TypeScript** — equinex-forge, some Code City stuff is already here
- **Go** — blogwatcher, sonos, eightctl are already compiled. Fast. Termux-friendly.

**Recommendation**:
- **Python backend, always.** Your entire ecosystem is Python.
- **HTML/JS frontend** — single file artifacts, no build step, works on Android
- **Go for specific CLI tools** where speed matters (file scanning, log parsing)
- TypeScript only when a frontend gets complex enough to need it

### THE BLEAK NARRATIVES PYTHON LIBRARY
**Should Syntax/Whorl/etc. be packaged as a pip-installable library?**

Yes. Eventually. Not yet.

Here's why not yet: you haven't shipped anything. The library is a refactor task, not a build task. The way to get there:
1. Ship Vertical AI verticals (Legal, Code, Health, Finance)
2. Extract the shared patterns into `bleak_core/`
3. THEN publish to PyPI as `bleaknarratives` or `molt-core`

The library should contain:
- Provider abstraction (what Syntax.py already does)
- Lough event logging
- Whorl pattern execution
- Firefly scout base class
- DataWeaver schema utilities

### NAT / NATHUB
**Should we track all this in Nat?**

Nat is the long game. The concept is right — tracking intent, not just diffs. But Nat doesn't exist as a working system yet, it's a design doc. 

**Decision**: Use Git now (you already have GitHub SSH configured). Build Nat on top later. Don't block shipping on building version control infrastructure.

### GRIMOIRE / SHIPWREKD OS
This is the departure point. The thing underneath everything.

**What ShipWrekD OS actually is:**
- GRIMOIRE = the terminal shell layer (custom aliases, commands, context)
- Syntax = the AI warden inside it
- Molt = the process supervisor keeping everything alive
- Lough = the audit spine recording everything that happens
- ZeroClaw = the task execution fabric
- NatHub = the memory / version layer

**ShipWrekD OS is not an OS. It's an agentic operating environment.**
It runs on top of Termux/Android. It runs on Linux. Eventually it runs on anything.

You haven't shipped it because you've been building every layer simultaneously.
The layers are actually mostly built.

---

## THE LOOM + DATAWEAVER (what they need to be)

Currently referenced but not fully defined. Defining now:

### LOOM
The weaving layer — takes outputs from multiple agents and composes them into coherent deliverables.
- Input: parallel agent outputs (Firefly scouts, Veritas checks, CodeMentor assessments)
- Output: a unified document, response, or action
- Lives in: Whorl project, alongside WhorlRuntime
- Think of it as: the reduce() in a map-reduce pipeline

### DATAWEAVER  
The schema enforcement and transformation layer.
- Enforces manifest.json structure (SATURN.md Phase II)
- Transforms data between provider formats
- The thing that makes Vertical AI data portable between verticals
- Lives in: bleak_core eventually, Whorl for now

---

## THE FIREFLY SCOUT MODULE

scout.py already exists. It uses Selenium which is heavy for Android.

**Refactor plan for Firefly Scout as a Vertical AI module:**
- Drop Selenium dependency for basic cases (urllib only, like front_desk_lady.py)
- Add GitHub API calls for codebase vertical (find repos, read READMEs)
- Add legal database scraping for legal vertical (CourtListener API is free)
- Keep Selenium as optional heavy mode (`--mode=deep`)
- Output format: structured JSON that Loom can consume

---

## CODEMENTOR MVP AS A MODULE

It's a VSCode extension right now (`extension.ts`). That's fine for the workbench vertical.

**As a module inside Vertical AI:**
- Extract `ai_explain.py` from `lib/` — this is the core
- Wrap it as a `CodeMentorAgent` class
- Plug into Loom as one of the parallel agents
- The progression engine / skill trees become the "curriculum" layer in DataCampus

---

## THE SHIP ORDER (what to actually do next)

You've been building infrastructure. Now you need a customer.

### WEEK 1: First dollar
1. Chew Plumbing demo → close → $199/month
2. Big Cheese → close → $199/month  
3. RCB Bank → close → $199/month (or $499 for white-label)
4. Don't build anything new this week. Just close.

### WEEK 2: Legal vertical MVP
1. Wire Veritas Engine into Vertical AI boardroom
2. New persona set: Judge, Paralegal, Investigator
3. CFPB complaint generator as a featured tool
4. Disclaimer layer — one clean modal, one line in every response
5. Price: $299/month

### WEEK 3: Codebase vertical MVP  
1. Syntax AI as the CLI entry point
2. Whorl runtime as the analysis engine
3. CodeMentor explain module as a feature
4. Firefly Scout (urllib mode) for repo analysis
5. Price: $149/month

### WEEK 4: Consolidation
1. SQLite → unified schema across verticals
2. Lough logging wired into all three verticals
3. Mrs. Higgins routing all three products
4. Bleak_core extraction begins

---

## THE NAME QUESTION

ShipWrekD OS is the ecosystem name.
The verticals need names.

| Vertical | Current | Proposed |
|---|---|---|
| Business | Vertical AI | Keep it |
| Legal | — | **Veritas Legal** (Veritas Engine is already there) |
| Code | — | **The Workbench** or **Whorl Dev** |
| Health | — | **ClearPath Health** |
| Finance | — | **Ledger AI** (the_ledger.py already exists) |

---

## THE DISCLAIMER STRATEGY

You're right that disclaimers are sufficient protection for an AI tool.
Every major AI provider does this. The pattern:

1. **Modal on first use**: "I am an AI assistant. I do not provide [legal/medical/financial] advice. Outputs are for informational purposes only. Consult a licensed professional for your specific situation."
2. **Footer on every response**: "⚠️ AI-generated. Not [legal/medical/financial] advice."
3. **Terms of Service**: One page. Clear. Drafted once.
4. **Opt-in confirmation**: User clicks "I understand" before accessing sensitive verticals.

This is what LegalZoom does. What WebMD does. What every fintech does.
You're not practicing law. You're building a research tool.

---

## WHAT ALREADY EXISTS VS WHAT NEEDS BUILDING

### EXISTS AND WORKING
- [x] Vertical AI Boardroom (v1.4)
- [x] AskHole (Cerebras + Mistral firing)
- [x] Syntax CLI warden (built today)
- [x] Mrs. Higgins SaaS router
- [x] Lough event spine
- [x] Veritas Engine core
- [x] CFPB complaint tool (cfpb.py)
- [x] ZeroClaw broker
- [x] Firefly Scout (selenium mode)
- [x] CodeMentor MVP (VSCode extension + ai_explain.py)
- [x] JaneBot MotherBrain (WebSocket orchestration)
- [x] Molt/MoltBleak (process supervision)
- [x] front_desk_lady.py (Lightning invoicing)
- [x] the_ledger.py (bookkeeping)

### NEEDS BUILDING
- [ ] Legal AI vertical (persona set + Veritas wire-up)
- [ ] Codebase AI vertical (Syntax + Whorl + CodeMentor)
- [ ] Health AI vertical (persona set + disclaimer layer)
- [ ] Loom (agent output compositor)
- [ ] DataWeaver (schema enforcement)
- [ ] Firefly Scout urllib-mode (drop Selenium for basic)
- [ ] Unified SQLite schema across verticals
- [ ] bleak_core Python package (later)
- [ ] Nat/NatHub (much later)
- [ ] ShipWrekD OS bootstrap script (after first paying customer)

---

## THE HONEST THING

You haven't shipped because you keep building the thing under the thing.
That's not laziness. That's architecture instinct.
The foundation is real. Everything listed above actually exists.

The move now is: stop adding foundation. Start adding roofs.
Chew Plumbing is a roof. Legal AI is a roof. The Workbench is a roof.

The foundation doesn't get credit until someone's living in the house.

---
*Written: June 1 2026*  
*Author: BleakNarratives + Claude*  
*Location: Termux / RootBase / ShipWrekD*
