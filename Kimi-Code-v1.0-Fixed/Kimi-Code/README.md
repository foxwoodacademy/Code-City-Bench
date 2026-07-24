# 🧠 Kimi-Code

**Adaptive Coding Mentor** • **Six Thinking Hats** • **Progressive Difficulty** • **Multi-Language**

> *"Training the next generation of developers"*

## What is Kimi-Code?

Kimi-Code is an intelligent coding mentor that adapts to your skill level, challenges you with progressively difficult problems, and teaches you to think about code from multiple perspectives using Edward de Bono's **Six Thinking Hats** methodology.

## Features

- 🎓 **Adaptive Difficulty** — Scales challenges based on your performance
- 🎩 **Six Thinking Hats** — Analyze code through 6 perspectives (White, Red, Black, Yellow, Green, Blue)
- 🌳 **Skill Tree** — Unlockable progression system with 20+ skills
- 💻 **Multi-Language** — Python, JavaScript, Rust, Go, C++ tracks
- 📊 **Persistent State** — Progress saved across sessions
- 🔄 **RootBase Integration** — Syncs with your existing CodeMentor ecosystem
- 🌐 **Web Dashboard** — Visual progress tracking at `localhost:8767`

## Quick Start

```bash
# Setup
kimi-code --setup

# Check status
kimi-code --status

# Start a challenge
kimi-code --challenge python

# Six Hats mode
kimi-code --hats-mode python

# Explain a file
kimi-code --explain myscript.py --mode expert

# Start dashboard
kimi-code --dashboard
```

## Six Thinking Hats for Code

| Hat | Color | Focus | Emoji |
|-----|-------|-------|-------|
| White | #FFFFFF | Facts & Data | 📊 |
| Red | #FF4444 | Intuition & Emotion | 🔥 |
| Black | #333333 | Risks & Cautions | ⚠️ |
| Yellow | #FFD700 | Benefits & Value | ✨ |
| Green | #00FF88 | Creativity & Alternatives | 🌱 |
| Blue | #0066FF | Meta-Analysis & Process | 🧠 |

## Skill Tree

```
Fundamentals          Execution           Design              Quality             Master
─────────────────────────────────────────────────────────────────────────────────────────
Code Reading  ──→  Debugging  ──→  Testing  ──→  Fullstack Mastery  ──→  Architect
     ↓                ↓              ↓
Syntax Mastery  →  Refactoring  →  Security Awareness
     ↓                ↓
Problem Decomp  →  Algorithm Design  →  Optimization
     ↓
System Design  →  (Six Hats Specializations)
```

## Architecture

```
Kimi-Code/
├── core/
│   ├── state_engine.py        # Persistent user state
│   ├── progression_engine.py  # Level/difficulty logic
│   ├── challenge_generator.py # Adaptive challenge creation
│   ├── six_hats.py           # Six Thinking Hats engine
│   ├── api_bridge.py         # Kimi/Gemini/OpenRouter API
│   └── skill_tree.py         # Visual progression system
├── modules/
│   ├── languages/            # Language-specific tracks
│   ├── hats/                # Hat-specific challenge modules
│   ├── difficulty/          # Tiered difficulty implementations
│   └── challenges/          # Challenge type generators
├── bridges/
│   ├── codementor_bridge.py # CodeMentor-MVP integration
│   ├── rootbase_sync.py     # RootBase ecosystem sync
│   └── api_server.py        # HTTP dashboard/API server
└── data/                    # User state & analytics
```

## Integration with RootBase

Kimi-Code lives in `/storage/emulated/0/RootBase/Kimi-Code/` and communicates with:
- **CodeMentor-MVP** — Shares analytics, API keys, challenge data
- **Thoth** — Could export automation scripts
- **Hermes** — Could broadcast achievements

## API Endpoints

When running `--serve`:

- `GET /` — Dashboard
- `GET /api/status` — System status
- `GET /api/progress` — Full progress data
- `GET /api/skills` — Skill tree data
- `GET /api/hats` — Hat mastery data
- `GET /api/challenge?lang=python&diff=5` — Generate challenge

## Configuration

Edit `config.json` or use `kimi-code --setup`:

```json
{
  "primary_provider": "kimi",
  "providers": {
    "kimi": { "api_key": "your-key", "model": "kimi-k2-6" },
    "gemini": { "api_key": "your-key", "model": "gemini-2.0-flash" }
  }
}
```

## License

MIT — Built for the next generation of developers.

---

*Built with 💚 by Kimi for the RootBase ecosystem*
