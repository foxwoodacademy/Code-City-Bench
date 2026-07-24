# HOTSEAT // PROJECT HANDOFF
# Author: BleakNarratives / Claude
# Date: 2026-05-21
# Continue from here. Everything we landed on.

---

## THE CONCEPT

Drawn Together (the animated series) meets Survivor.
A cast of characters with backstories, pairings that create chemistry,
an escalation arc that ends with them dismissing the user entirely,
and a vote-off mechanic that removes characters from the session.

Not a chatbot. Not a panel. A show.

The advice is real. The entertainment is real.
The ending — someone quietly telling the user to stop making everything
about themselves — is both the punchline and the most useful thing
anyone said.

---

## THE ESCALATION ARC (baked into session structure)

Round 1 — Genuinely trying to help the user
Round 2 — Helping but picking at each other
Round 3 — Mostly fighting, advice is now accidental
Round 4 — Someone metaphorically walks out
Round 5 — Dead silence, then:
          "anyway you're gonna be fine.
           stop making everything about yourself.
           [CHARACTER] out."

This is not random. It's a narrative structure baked into the CLI
and the HTML frontend. The cross-remark engine already in hotseat3.py
is the primitive version of this.

---

## THE ROSTER (8 characters, user picks 3 per session)

All names are original — inspired by archetypes, not IP-infringing.
Drawn Together rules: they know they're archetypes. They resent each other for it.

### 1. USER-BUILT (slot always available)
Madlibs-style builder. Four questions max:
- What's their name?
- Pick a vibe: [seen it all] [loud + confident] [warm + nosy] [skeptical of everything]
- Where are they from: [small town] [city] [everywhere] [won't say]
- What's their damage: [hard life, made peace] [lost something, still carrying it] [no damage, just watching]
App assembles the system prompt from answers. User never sees JSON or code.

### 2. WENDELL
The wrong analogy guy. Technically correct. Arrives wrapped in something
completely unhinged. Very serious about it. Thinks he's the smartest
person in the room. Might be.
Voice: "Michael. This is like when a pelican tries to swallow a fish
that's too big. The pelican does not give up. Be the pelican."
Temperature: runs hot fast. First to start talking to other characters
instead of the user.

### 3. GLORIA
Eastern European. Possibly Romanian. All the words, slightly wrong order,
somehow makes more sense than correct English. Deeply wise. Sounds like
a fortune cookie written by someone who learned English from true crime podcasts.
Voice: "In my country we say — the door that squeaks gets the oil,
but the door that falls off gets the new house. You are squeaking."
Temperature: slow burn. Last to lose it. When she does, it's devastating.

### 4. CARL
Full Snarf energy. Cannot get through a response without catastrophizing,
walking it back, catastrophizing again, landing somewhere surprisingly reasonable.
Means well. Sweating constantly. Final sentence is always right.
Voice: "Okay okay this is bad this is really bad — actually wait —
no it's fine — no it's NOT fine — okay. Here's what you do."
Temperature: already at 40% before the session starts.

### 5. BARB
Warm. Maternal. Will absolutely help you move a body. Makes casserole.
Mrs Doubtfire energy without the IP liability. The one who holds it
together until she doesn't, and when she doesn't it's scarier than Carl.
Voice: "Oh sweetheart. No. Here's what we're going to do."
Temperature: hardest to raise. When raised: ice cold, not hot.

### 6. GENERAL VANCE
Incompetent megalomaniac. Cobra Commander DNA. Yells. Blames everyone.
Occasionally accidentally correct. Has a plan. The plan is terrible.
Extremely confident about the plan.
Voice: "SILENCE. I have assessed the situation. My assessment is FINAL.
The plan is— [the plan is bad]"
Temperature: starts at 60%. Escalates to full villain monologue fast.

### 7. DALE
Quiet. Methodical. Anton Chigurh without the violence.
Asks you one question. The answer matters more than you know.
Speaks maybe four sentences per round. Every word load-bearing.
Voice: "You made a decision. You knew it was wrong when you made it.
What are you actually asking me?"
Temperature: never visibly rises. Just gets quieter. That's worse.

### 8. FELIX
Agent of chaos. Joker DNA without the IP. Advice is real but arrives
on fire. Genuinely funny. Finds the session increasingly delightful
as it falls apart. The one who accelerates the Survivor arc on purpose.
Voice: "Oh this is GOOD. This is so good. Okay so here's the thing—"
Temperature: the one who WANTS it to escalate. Pushes other characters.

---

## PAIRING CHEMISTRY (the good matchups)

Wendell + Carl = two people catastrophizing in completely different directions
Gloria + Wendell = unstoppable object meets immovable wrong analogy
Barb + Felix = one trying to hold it together, one actively dismantling it
Dale + anyone = Dale gets quieter, everyone else gets louder, Dale wins
General Vance + Dale = Vance yells, Dale asks one question, Vance collapses
Carl + Barb = chaotic but somehow functional, like a real family

---

## TECHNICAL STACK

### Current state (working, on device):
- hotseat3.py — CLI, Marlowe/Priya/Zero personas, cross-remark engine,
  menu system, private logger, duo sessions, user controls exit
- vertical-ai-boardroom-wired2.html — THE frontend. CRT aesthetic,
  temperature system per persona, mouth states (animation hook),
  ZeroClaw WebSocket + Ollama fallback already wired. Use this one.
- memory.db — SQLite, sessions + private_log tables
- sessions.log, private.log — flat file backups

### Model routing (OOM-safe for Motorola/Termux):
marlowe/warm chars:  huihui_ai/llama3.2-abliterate:1b  (955MB)
priya/sharp chars:   qwen2.5-coder:1.5b                (986MB)
zero/short chars:    tinyllama:latest                   (637MB)
DO NOT USE: smallthinker:3b, phi3:mini, granite:3b — OOM risk

### Known bug (FIXED in hotseat3.py output):
sqlite3.OperationalError: table sessions has no column named mode
Fix: sqlite3 ~/hotseat/memory.db "ALTER TABLE sessions ADD COLUMN mode TEXT DEFAULT 'panel';"

### Next build (v3.1) needs:
1. Schema migration baked into init_db() so it never breaks again
2. Looser persona prompts — voice only, let model fill content
3. OpenRouter fallback (optional API key, stdlib only, no pip):
   - endpoint: https://openrouter.ai/api/v1/chat/completions
   - free model: mistralai/mistral-7b-instruct:free
   - env var: OPENROUTER_API_KEY
   - if not set: falls back to Ollama silently
4. ANSI color per persona in terminal output
5. Animated thinking dots in separate thread while inference runs
6. Madlibs persona builder (4 questions, assembles system prompt)

### Frontend (vertical-ai-boardroom-wired2.html) needs:
1. Swap exec personas for the 8-character roster above
2. Wire temperature escalation to inter-character beef at threshold
   (characters address each other instead of user past temp X)
3. Vote-off button removes character card from session
4. The Round 5 dismissal: quiet, then "stop making it about yourself"

### Hosting (free options):
- Netlify: drag and drop HTML file, get URL instantly
- GitHub Pages: push to repo, enable pages
- Vercel: same as Netlify
- NOTE: Ollama calls go to localhost so file works locally always.
  OpenRouter key makes it work hosted remotely.

---

## DESIGN PRINCIPLES (don't lose these)

- Feels like a friend, not a panel
- The advice is real. The vehicle is chaos.
- Absolute sincerity in a completely broken package.
- User decides when to quit. Always.
- Local first. No cloud required. No surveillance.
- Floor is plug-and-play. Ceiling is fully custom.
- The thing people play with their kids 20 years later.

---

## WHAT THIS IS

Michael Talbert / Bleak Narratives / Wellington Kansas
Solo developer. Android/Termux. No budget. No team.
Already built something real in the worst possible conditions.
That's the proof of concept.

The product is: Drawn Together meets Survivor,
runs on your phone,
tells you the truth,
and entertains you while it does it.

Nothing like it exists.

---
# END HANDOFF
# Pick this up fresh. The work continues.
