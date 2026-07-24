# Terminal Coach - QRD
## Quick Rundown for Mike

**Save this as**: `/storage/emulated/0/terminal_coach_README.md`

---

## What This Is

A **natural language bash translator** that converts "what you want to do" into actual terminal commands.

You don't need to memorize bash syntax. Just tell Coach what you want, and it gives you the command with explanations.

**Built for people who think in goals, not syntax.**

---

## Quick Start (30 Seconds)

### 1. Save the Script
```bash
cd /storage/emulated/0/
# Copy terminal_coach.py from artifact
chmod +x terminal_coach.py
```

### 2. Run It
```bash
# Interactive mode
python terminal_coach.py

# Or single query mode
python terminal_coach.py find python files
```

### 3. Talk to It
```
💬 What do you want to do? find files modified today

✅ Found exact match: 'find files modified today'
📝 Command: find . -type f -mtime 0
💡 Explanation: Searches for files/directories matching criteria

🔍 Breakdown:
  Command: find
    → Searches for files/directories matching criteria
  -type: Search by type (f=file, d=directory)
  -mtime: Modified time (in days)

❓ Want to run this? (y/n/modify)
→ 
```

**That's it.** Natural language in, bash command out.

---

## Usage Modes

### Interactive Mode (Recommended)
```bash
python terminal_coach.py
```

**Then you can:**
- Ask questions: "find python files"
- Get explanations: "explain ls -lha"
- Run commands: "run pwd"
- See examples: "examples"
- Repeat last: "again"

**Exit with:** `quit`, `exit`, or Ctrl+C

### Single Query Mode
```bash
python terminal_coach.py find files modified this week
# Gives you the command immediately, no interaction
```

---

## What It Knows

### File Operations
| You Say | It Gives You |
|---------|--------------|
| "find python files" | `find . -name "*.py" -type f` |
| "find files modified today" | `find . -type f -mtime 0` |
| "find large files" | `find . -type f -size +10M` |
| "list files by date" | `ls -lht` |
| "show file tree" | `tree -L 2` |
| "disk usage" | `du -sh *` |

### Searching Text
| You Say | It Gives You |
|---------|--------------|
| "search in files" | `grep -r "PATTERN" .` |
| "search python files" | `grep -r "PATTERN" --include="*.py" .` |
| "count lines" | `wc -l` |

### Process Management
| You Say | It Gives You |
|---------|--------------|
| "show running processes" | `ps aux` |
| "find process" | `ps aux | grep` |
| "show system resources" | `top -n 1` |

### Network
| You Say | It Gives You |
|---------|--------------|
| "check internet" | `ping -c 4 google.com` |
| "show my ip" | `curl ifconfig.me` |
| "download file" | `curl -O` |

### Archives
| You Say | It Gives You |
|---------|--------------|
| "compress folder" | `tar -czf archive.tar.gz` |
| "extract archive" | `tar -xzf` |
| "zip folder" | `zip -r archive.zip` |

### Git
| You Say | It Gives You |
|---------|--------------|
| "git status" | `git status` |
| "git commit" | `git commit -m "MESSAGE"` |
| "show git log" | `git log --oneline -10` |

### Mike's Shortcuts
| You Say | It Gives You |
|---------|--------------|
| "find context files" | `find /storage/emulated/0/context_system -type f` |
| "show recent snapshots" | `ls -lht /storage/emulated/0/context_system/context_history/` |
| "find my python code" | `find /storage/emulated/0/root_2025 -name "*.py" -type f` |

---

## How It Works

### 1. You Ask in Natural Language
```
💬 What do you want to do? find python files
```

### 2. Coach Finds the Command
```
✅ Found exact match: 'find python files'
📝 Command: find . -name "*.py" -type f
```

### 3. Coach Explains It
```
💡 Explanation: Searches for files/directories matching criteria

🔍 Breakdown:
  Command: find
    → Searches for files/directories matching criteria
  -name: Search by filename
  -type: Search by type (f=file, d=directory)
```

### 4. You Decide What to Do
```
❓ Want to run this? (y/n/modify)
→ y    # Runs it immediately
→ n    # Just shows the command, doesn't run
→ modify    # Lets you edit before running
```

---

## Special Commands

### `examples`
Shows all available natural language queries:
```
💬 What do you want to do? examples

📚 EXAMPLE QUERIES:

Finding Files:
  • find python files
  • find files modified today
  • find large files

Listing & Viewing:
  • list files by date
  • show file tree
  ...
```

### `explain COMMAND`
Explains any bash command:
```
💬 What do you want to do? explain ls -lha

📖 EXPLAINING: ls -lha

Command: ls
  → Lists directory contents
  -l: Long format (detailed info)
  -h: Human readable (sizes in KB/MB/GB)
  -a: All (including hidden files)
```

### `run COMMAND`
Runs any bash command directly:
```
💬 What do you want to do? run pwd
▶️  Running: pwd
/storage/emulated/0
✅ Command completed successfully
```

### `again`
Repeats the last command you ran:
```
💬 What do you want to do? again
▶️  Running: [previous command]
```

---

## Safety Features

### Won't Run System-Killers
```bash
💬 What do you want to do? run rm -rf /
🚫 DANGEROUS COMMAND DETECTED - NOT RUNNING
This command could destroy your system!
```

**Blocks:**
- `rm -rf /` (deletes everything)
- `dd if=` (disk destroyer)
- `mkfs` (formats disk)
- Fork bombs

### Shows Before Running
Always shows you the command and asks permission before executing.

### Timeout Protection
Commands automatically timeout after 30 seconds (prevents hanging).

---

## Usage Patterns

### Pattern 1: Learning Bash
```
You: "I want to find all Python files"
Coach: Here's the command: find . -name "*.py" -type f
Coach: The -name flag searches by filename
Coach: The -type f flag finds only files, not directories

# Next time you remember: find . -name "*.py" -type f
# You learned by doing
```

### Pattern 2: Quick Tasks
```bash
# Instead of googling "how to compress folder linux"
python terminal_coach.py compress folder

# Instant answer with explanation
```

### Pattern 3: Command Validation
```
You: "Is this command safe? explain rm -rf myproject"
Coach: rm → Removes files/directories (BE CAREFUL!)
Coach: -r → Recursive (includes subdirectories)
Coach: -f → Force (no confirmation)

# Now you understand what it does before running
```

### Pattern 4: Modified Commands
```
Coach: Command: find . -name "*.py" -type f
You: modify
You: find /storage/emulated/0/root_2025 -name "*.py" -type f
# Changed search path to specific directory
```

---

## Common Questions

### "What if it doesn't understand me?"
Try rephrasing. Examples:
- ❌ "gimme the pythons"
- ✅ "find python files"

Or type `examples` to see what it knows.

### "Can I add my own commands?"
Yes! Edit the script, find `self.command_map`:
```python
'your query here': 'bash command here',
```

### "Will it break my system?"
No. It has safety checks and asks before running. **But** if you bypass the checks and run dangerous commands manually, that's on you.

### "Can it learn from me?"
Not yet. But that's what Syntax AI will do (future).

---

## Integration with Other Tools

### With Health Monitor
```bash
# Learn health check commands
python terminal_coach.py
> "show system resources"
# Coach teaches you: top -n 1

# Then use in Health Monitor
```

### With ContextTrail
```bash
# Find context commands
python terminal_coach.py
> "find context files"
# Shows: find /storage/emulated/0/context_system -type f
```

### With Any Tool
Coach is a **learning interface** for bash. Use it to:
- Learn commands for other scripts
- Understand error messages
- Build your own automation

---

## Customization

### Add Your Own Shortcuts
Edit `self.command_map` in the script:
```python
'backup my work': 'tar -czf backup.tar.gz /storage/emulated/0/root_2025',
'check logs': 'tail -f /storage/emulated/0/logs/app.log',
```

### Add More Explanations
Edit `explanations` dictionary:
```python
'your_command': 'What this command does',
```

### Change Safety Settings
Edit `dangerous` list if you want to block more commands (or fewer, at your own risk).

---

## Learning Path

**Week 1:** Use Coach for everything
- Don't type raw bash, ask Coach first
- Read the explanations
- Start recognizing patterns

**Week 2:** Mix Coach + Raw Bash
- Use Coach for new tasks
- Type simple commands yourself
- Use `explain` when confused

**Week 3+:** Graduate
- Mostly type bash yourself
- Use Coach for complex stuff
- You've learned bash without studying

---

## Troubleshooting

### "Command not found: python"
```bash
pkg install python
```

### "No matches found"
Type `examples` to see available commands, or try rephrasing.

### "Command failed with exit code 1"
The bash command ran but failed. Read the error message - Coach shows it.

### Commands run but nothing happens
Check if you're in the right directory. Use `pwd` to see where you are.

---

## What This Doesn't Do

❌ **Doesn't write scripts** - just gives single commands
❌ **Doesn't debug code** - explains bash, not Python/etc
❌ **Doesn't connect to internet** - all local
❌ **Doesn't learn** - same responses every time (for now)

**But:** It's the foundation for Syntax AI, which will do all of these.

---

## Philosophy

**The terminal is powerful but hostile to beginners.**

Cryptic syntax (`tar -xzf`) and arcane flags (`-lha`) create a wall between:
- What you want to do
- How to do it

**Terminal Coach removes that wall.**

You think in goals. Coach thinks in syntax.

**You don't memorize commands. You understand them.**

And understanding leads to mastery.

---

## Next Steps

1. **Run it**: `python terminal_coach.py`
2. **Type `examples`**: See what it can do
3. **Try a query**: "find python files"
4. **Use it daily**: Make it your bash interface for a week
5. **Watch yourself learn**: You'll be typing raw bash without Coach soon

---

## Future Integration

When Syntax AI is built:
- Terminal Coach becomes the **natural language layer**
- Syntax AI provides the **intelligence layer**
- Together they create: **conversational terminal that learns from you**

**This is the first piece of that puzzle.**

---

**Built**: Thread 5, Nov 22 2025, 5:30am
**By**: Mike (architect) + Claude (coarchitect)  
**Status**: Production ready
**Learning curve**: Negative (you learn by using it)

*No homo. Maximum teach. Coach mode forever.*

---

*Last updated: 2025-11-22*