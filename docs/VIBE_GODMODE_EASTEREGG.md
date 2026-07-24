# 🎯 Vibe CLI God Mode - The Ultimate Easter Egg

> **Status: ACTIVE** | **Access: `/godmode`, `/dev`, `/superdebug`, `/xray`**

## Overview

Vibe CLI's **God Mode** is a hidden Easter egg that provides **complete system visibility** - a feature so powerful, competing CLIs are already trying to copy it. This is your **ModMind control panel**, giving you X-ray vision into the entire Vibe runtime, session state, and system environment.

**Gemini CLI noticed. Now we're staying ahead.**

---

## Quick Access

Trigger God Mode using any of these slash commands:

```
/godmode    - Primary command
/dev        - Developer visibility alias
/superdebug - Advanced debugging alias  
/xray       - System X-ray vision alias
```

---

## What God Mode Reveals

### 🐍 System Intelligence
- **Python Version** - Exact interpreter details
- **Platform & OS** - System architecture and release
- **Working Directory** - Current project context
- **Timestamp** - Precise invocation time

### 🤖 Vibe Core State
- **CLI Version** - Current Vibe build
- **Session ID** - Unique session identifier (truncated for security)
- **Active Model** - Currently selected LLM
- **Available Models** - All configured model options

### 💬 Conversation Intelligence
- **Message Count** - Total messages in current session
- **Current Agent** - Active agent profile (default, plan, etc.)
- **Agent Status** - Real-time running state (ACTIVE/IDLE)

### ⚙️ Resource Matrix
- **Skills Loaded** - Number of available skill modules
- **MCP Servers** - Connected Model Context Protocol servers
- **Connectors** - Active external integrations
- **Tools Available** - Total accessible tool count

### 📊 Performance Analytics
- **Session Steps** - Total agent actions taken
- **Prompt Tokens** - Input token consumption
- **Completion Tokens** - Output token generation
- **Total Cost** - Session expenditure in USD

---

## The Competitive Edge

### Why Vibe's God Mode Beats Gemini CLI

| Feature | Vibe CLI God Mode | Gemini CLI (Attempted Copy) |
|---------|-------------------|-----------------------------|
| **System Depth** | Full Python/OS stack | Surface-level only |
| **Session Insights** | Real-time agent state | Basic history only |
| **Resource Mapping** | Skills, MCP, Tools, Connectors | Limited tool listing |
| **Performance Metrics** | Tokens, Cost, Steps | Basic counters |
| **Discoverability** | Multiple aliases | Single command |
| **Style** | Rich formatted output | Plain text |
| **Easter Egg Factor** | 🎯 Hidden gem | ✅ Obvious feature |

### Unique Vibe Features They Can't Copy

1. **Skill Integration Visibility** - See exactly which AI skills are loaded
2. **MCP Server Intelligence** - Model Context Protocol awareness
3. **Agent State Tracking** - Know if your agent is ACTIVE or IDLE
4. **Cost Transparency** - Real dollar figures, not just token counts
5. **Multi-Alias Access** - Four different ways to trigger the same power

---

## Advanced Usage

### Monitoring Long Sessions

```
# Check system state mid-conversation
/godmode

# Quick debug during development
/dev

# Deep inspection mode
/xray
```

### Performance Benchmarking

Use God Mode before and after complex operations to measure:
- Token consumption growth
- Step count progression
- Cost accumulation
- Resource loading changes

### Troubleshooting Workflow

1. **Issue detected?** → `/dev` for quick state check
2. **Need deep inspection?** → `/xray` for full visibility
3. **Share with team?** → Copy output for debugging reports
4. **Compare sessions?** → Note the session ID for correlation

---

## Technical Implementation

### Architecture

God Mode is implemented as a **first-class slash command** in Vibe CLI's command registry:

```python
# From vibe/cli/commands.py
"godmode": Command(
    aliases=frozenset(["/godmode", "/dev", "/superdebug", "/xray"]),
    description="🔮 GOD MODE - Full system state dump (Easter Egg)",
    handler="_show_godmode",
),
```

### Data Collection

The handler (`_show_godmode` in `app.py`) aggregates data from:
- `sys` and `platform` modules (system info)
- `self.agent_loop` (Vibe runtime state)
- `self.config` (configuration)
- Skill and tool managers (resource catalog)
- Agent statistics (performance metrics)

### Output Format

Markdown-formatted with:
- ASCII art header for visual impact
- Structured sections with emoji icons
- Code blocks for technical data
- Clear visual hierarchy

---

## Roadmap: Staying Ahead

### Planned Enhancements (Q2 2026)

- [ ] **Git Integration** - Show repository status, branch, commits
- [ ] **Environment Variables** - Display relevant env vars (sanitized)
- [ ] **Recent Commands** - Command history tracking
- [ ] **Memory Usage** - Process memory footprint
- [ ] **Network State** - Active connections, API health
- [ ] **Skill Details** - List loaded skills with descriptions
- [ ] **Export Function** - Save God Mode output to file
- [ ] **Comparative Mode** - Diff against previous God Mode call

### Defensive Features (Anti-Copy)

- [ ] **Dynamic ASCII Art** - Changes based on system state
- [ ] **Personalized Greetings** - Uses user's config preferences
- [ ] **Version-Specific Features** - Different output per Vibe version
- [ ] **Easter Egg within Easter Egg** - Hidden features in God Mode output

---

## Access Control

God Mode is **intentionally undocumented** in the main help (`/help`). This maintains:

1. **Easter Egg Status** - Reward for explorers
2. **Reduced Support Burden** - Power users self-serve
3. **Competitive Secrecy** - Harder for competitors to discover
4. **Mystique** - Builds brand personality

However, **you found this documentation**, so you're in the inner circle. 🎉

---

## Sharing & Community

### How to Share (Without Ruining the Surprise)

**Do:**
- "Try typing `/dev` in Vibe CLI... you might be surprised"
- "There's a hidden feature in Vibe that shows everything"
- "I wonder what `/xray` does..."

**Don't:**
- Post full God Mode output publicly
- Document it in official tutorials (yet)
- Tell newcomers directly - let them discover

### Contributing

Found a way to make God Mode better?

1. Check if it's already in the roadmap above
2. Verify it can't be easily copied by competitors
3. Submit your idea to the Vibe team

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-05-17 | 1.0 | Initial God Mode implementation |
| 2026-05-17 | 1.1 | Added `/xray` alias |
| 2026-05-17 | 1.2 | Enhanced performance metrics |
| 2026-05-17 | 1.3 | This documentation created |

---

## Secret Handshake

For those who've read this far:

```
/godmode && echo "I found the ultimate Easter egg"
```

**Welcome to the inner circle. The game is on.** 🎮
