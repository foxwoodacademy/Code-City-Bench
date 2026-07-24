# Implore: Autonomous Grant Intelligence Platform

Implore is an agentic, codebase-aware grant intelligence platform designed to transform any project into fundable grant applications. It autonomously scans codebases, matches them against federal and international grant databases using semantic search, generates technical narratives with strict objectivity guardrails, and renders submission-ready documents.

## Key Features
- **Codebase-as-Input:** Analyzes source code, dependencies, and project structure to infer fundability.
- **Agentic Pipeline:** Stateful, multi-step workflow orchestrated via LangGraph.
- **Brutal Objectivity:** Enforces fact-based, hallucination-free narrative generation using strict template guardrails and semantic auditing.
- **Ecosystem Ready:** Acts as a headless service within the RootBase agent swarm, broadcasting intelligence to other nodes (Syntax-AI, Whorl, etc.) via a standardized JSON API.
- **Global Deployment:** Containerized and ready for production, with regional and multilingual support.

## Getting Started
### Prerequisites
- Python 3.13+
- OpenAI API Key (or other supported LLM provider)

### Installation
```bash
pip install -r requirements.txt
```

### Usage
Run the pipeline to scan a directory and generate grant applications:
```bash
python3 workflow.py --directory /path/to/project
```

## Architecture
Implore follows a modular, stateful graph architecture (`langgraph`), ensuring scalability and robustness. Key modules include:
- `Ingestor`: Handles codebase, URL, and document ingestion.
- `Matcher`: Intent-aware semantic search for grant alignment.
- `Auditor`: NLP-based fact-checking against source data.
- `Generator`: Objective narrative production.
- `SF424Filler`: PDF rendering for submission-ready forms.

## Roadmap Status
- MVP Core: Complete
- Semantic Search: Complete
- Persistence Layer: Complete
- Production Hardening: Complete

## Why Press Conference

Pytch is a moderated press conference, not a panel.

- NotebookLM's Deep Dive hosts are the podium. They always have material.
- Models queue questions instead of free-for-all crosstalk.
- The human is the moderator: tap the NLM hand + mole to grant the mic.
- Every granted question forces the hosts deeper — progressively sharper
  cuts, not a recap loop.

Moat logic: the format keeps the Google engine optimized as a side effect.
The hosts get interrogated into deeper material regardless of what
NotebookLM ships next. Their upgrades make our show better; they can't
make it worse. We don't compete with the engine — we cross-examine it.

Quip rule: no canned strings. Each persona interjection pulls an unused
line from that persona's own actual turn every time the floor opens.
