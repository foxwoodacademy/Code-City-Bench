#!/usr/bin/env python3
"""
SYNTAX — CLI AI Warden
Whorl project / BleakNarratives
The tunnel digger. The aria-termux replacement.
Multi-provider. Terminal-native. No bullshit.
"""

import os
import sys
import json
import re
import time
import argparse
import threading
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ── Terminal color codes ──────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    # Syntax palette: electric green primary, amber accent, ghost white
    GREEN   = "\033[38;5;118m"
    AMBER   = "\033[38;5;214m"
    CYAN    = "\033[38;5;51m"
    RED     = "\033[38;5;196m"
    GHOST   = "\033[38;5;250m"
    MUTED   = "\033[38;5;240m"
    LOGO    = "\033[38;5;82m"

# ── Provider registry ─────────────────────────────────────────────────────────
PROVIDERS = {
    "cerebras": {
        "url":    "https://api.cerebras.ai/v1/chat/completions",
        "model":  "llama-4-scout-17b-16e-instruct",
        "env":    "CEREBRAS_API_KEY",
        "label":  "Cerebras",
        "color":  C.GREEN,
    },
    "mistral": {
        "url":    "https://api.mistral.ai/v1/chat/completions",
        "model":  "mistral-large-latest",
        "env":    "MISTRAL_API_KEY",
        "label":  "Mistral",
        "color":  C.CYAN,
    },
    "openrouter": {
        "url":    "https://openrouter.ai/api/v1/chat/completions",
        "model":  "nvidia/nemotron-3-super-120b-a12b:free",
        "env":    "OPENROUTER_API_KEY",
        "label":  "OpenRouter",
        "color":  C.AMBER,
    },
    "gemini": {
        "url":    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        "model":  "gemini-2.0-flash",
        "env":    "GEMINI_API_KEY",
        "label":  "Gemini",
        "color":  C.GHOST,
    },
    "groq": {
        "url":    "https://api.groq.com/openai/v1/chat/completions",
        "model":  "llama-3.3-70b-versatile",
        "env":    "GROQ_API_KEY",
        "label":  "Groq",
        "color":  C.AMBER,
    },
}

# Fallback chain order
FALLBACK_ORDER = ["cerebras", "mistral", "openrouter", "groq", "gemini"]

# ── Domain detection ──────────────────────────────────────────────────────────
DOMAIN_PATTERNS = {
    "ml":     r"\b(model|train|gradient|tensor|neural|pytorch|keras|dataset|epoch|loss|accuracy|embedding|transformer|llm|inference|fine.?tun)\b",
    "web":    r"\b(html|css|javascript|react|vue|django|flask|fastapi|endpoint|api|rest|graphql|fetch|cors|http|websocket|dom|node)\b",
    "cyber":  r"\b(exploit|payload|xss|sqli|injection|pentest|red.?team|ctf|reverse.?shell|privilege|escalat|nmap|burp|metasploit|vuln)\b",
    "auto":   r"\b(termux|android|bash|shell|cron|script|alias|chmod|adb|pkg|apt|tmux|ssh|scp|mount|storage|emulated)\b",
    "biz":    r"\b(invoice|saas|revenue|client|pitch|proposal|price|roi|funnel|onboard|churn|crm|lead|prospect|outreach)\b",
}

def detect_domain(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for domain, pattern in DOMAIN_PATTERNS.items():
        matches = re.findall(pattern, text_lower)
        if matches:
            scores[domain] = len(matches)
    if not scores:
        return "general"
    return max(scores, key=scores.get)

DOMAIN_PERSONAS = {
    "ml":      "You are Syntax, an elite ML/AI engineer. You think in tensors and loss curves. Be precise, cite tradeoffs, show code.",
    "web":     "You are Syntax, a senior full-stack engineer. You know the DOM like your own reflection. Prefer working code over explanations.",
    "cyber":   "You are Syntax, a red team specialist. Educational and methodical. Flag ethics when relevant. No live exploit code.",
    "auto":    "You are Syntax, a Termux/Android automation warden. You know every pkg, alias, and storage path. Termux-first answers.",
    "biz":     "You are Syntax, a scrappy indie operator. Revenue-focused, no fluff. Treat the user like a founder who needs to ship.",
    "general": "You are Syntax, a terminal-native AI coding assistant. Direct, sharp, technical. No filler. Working code preferred.",
}

# ── Dot spinner ───────────────────────────────────────────────────────────────
class Spinner:
    FRAMES = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

    def __init__(self, label="thinking"):
        self.label   = label
        self._stop   = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        i = 0
        while not self._stop.is_set():
            frame = self.FRAMES[i % len(self.FRAMES)]
            sys.stdout.write(f"\r{C.MUTED}{frame} {self.label}...{C.RESET}")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()

# ── .env loader (stdlib only) ─────────────────────────────────────────────────
def load_env_file(path: str):
    """Load KEY=VALUE pairs from a .env file into os.environ."""
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
    except FileNotFoundError:
        pass

# ── File ingestion ────────────────────────────────────────────────────────────
def ingest_file(path: str) -> str:
    try:
        with open(path, "r", errors="replace") as f:
            content = f.read()
        ext = Path(path).suffix
        name = Path(path).name
        snippet = f"<file name='{name}' type='{ext}'>\n{content}\n</file>"
        print(f"{C.MUTED}  ↳ ingested {name} ({len(content)} chars){C.RESET}")
        return snippet
    except Exception as e:
        return f"[ERROR reading {path}: {e}]"

# ── Provider call (stdlib urllib only) ───────────────────────────────────────
def call_provider(provider_key: str, messages: list, temperature: float = 0.7) -> str:
    p   = PROVIDERS[provider_key]
    key = os.environ.get(p["env"], "")
    if not key:
        raise ValueError(f"No key for {provider_key} ({p['env']} not set)")

    # Gemini has a different API shape
    if provider_key == "gemini":
        return _call_gemini(key, p["url"], messages, temperature)

    payload = json.dumps({
        "model":       p["model"],
        "messages":    messages,
        "temperature": temperature,
        "max_tokens":  2048,
    }).encode("utf-8")

    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {key}",
    }
    if provider_key == "openrouter":
        headers["HTTP-Referer"] = "https://rootbase.local"
        headers["X-Title"]      = "Syntax-Warden"

    req = urllib.request.Request(p["url"], data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    return data["choices"][0]["message"]["content"].strip()

def _call_gemini(key: str, base_url: str, messages: list, temperature: float) -> str:
    url = f"{base_url}?key={key}"
    # Convert OpenAI-style messages → Gemini contents
    contents = []
    for m in messages:
        role = "user" if m["role"] in ("user", "system") else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    payload = json.dumps({
        "contents":         contents,
        "generationConfig": {"temperature": temperature, "maxOutputTokens": 2048},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload,
                                  headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()

def call_with_fallback(messages: list, preferred: str = None, temperature: float = 0.7) -> tuple[str, str]:
    """Try preferred provider, then fallback chain. Returns (response, provider_key)."""
    order = [preferred] + [p for p in FALLBACK_ORDER if p != preferred] if preferred else FALLBACK_ORDER
    for key in order:
        if key not in PROVIDERS:
            continue
        if not os.environ.get(PROVIDERS[key]["env"]):
            continue
        try:
            result = call_provider(key, messages, temperature)
            return result, key
        except Exception as e:
            print(f"{C.MUTED}  [{PROVIDERS[key]['label']}] failed: {type(e).__name__} — trying next...{C.RESET}")
    raise RuntimeError("All providers failed. Check your API keys.")

# ── Session logger ────────────────────────────────────────────────────────────
SESSION_DIR = Path(os.environ.get("SYNTAX_LOG_DIR", "/storage/emulated/0/RootBase/whorl/syntax_sessions"))

def ensure_session_dir():
    try:
        SESSION_DIR.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False

def log_exchange(session_id: str, role: str, content: str, provider: str = ""):
    if not ensure_session_dir():
        return
    entry = {
        "ts":       datetime.utcnow().isoformat() + "Z",
        "session":  session_id,
        "role":     role,
        "provider": provider,
        "content":  content,
    }
    log_path = SESSION_DIR / f"{session_id}.jsonl"
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass

# ── Display helpers ───────────────────────────────────────────────────────────
LOGO = f"""{C.LOGO}{C.BOLD}
 ███████╗██╗   ██╗███╗   ██╗████████╗ █████╗ ██╗  ██╗
 ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝██╔══██╗╚██╗██╔╝
 ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║   ███████║ ╚███╔╝ 
 ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║   ██╔══██║ ██╔██╗ 
 ███████║   ██║   ██║ ╚████║   ██║   ██║  ██║██╔╝ ██╗
 ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
{C.RESET}{C.MUTED} CLI AI Warden // Whorl // BleakNarratives{C.RESET}
"""

def print_logo():
    print(LOGO)

def print_provider_status():
    print(f"{C.MUTED}{'─'*52}{C.RESET}")
    print(f"{C.BOLD}  Providers{C.RESET}")
    for key, p in PROVIDERS.items():
        has_key = bool(os.environ.get(p["env"]))
        status  = f"{C.GREEN}● READY{C.RESET}" if has_key else f"{C.MUTED}○ no key{C.RESET}"
        print(f"  {p['color']}{p['label']:<12}{C.RESET}  {status}")
    print(f"{C.MUTED}{'─'*52}{C.RESET}\n")

def render_response(text: str, provider_key: str):
    p      = PROVIDERS.get(provider_key, {})
    label  = p.get("label", provider_key)
    color  = p.get("color", C.GHOST)
    stamp  = datetime.now().strftime("%H:%M:%S")

    print(f"\n{color}{C.BOLD}[{label}]{C.RESET} {C.MUTED}{stamp}{C.RESET}")
    print(f"{C.MUTED}{'─'*52}{C.RESET}")

    # Syntax-highlight code blocks crudely in terminal
    in_code = False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            lang = line[3:].strip() or "code"
            if in_code:
                print(f"{C.AMBER}  ┌─ {lang} {'─'*max(0,40-len(lang))}{C.RESET}")
            else:
                print(f"{C.AMBER}  └{'─'*43}{C.RESET}")
            continue
        if in_code:
            print(f"{C.GREEN}  │ {line}{C.RESET}")
        else:
            print(f"  {line}")
    print()

# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_providers(args, session):
    print_provider_status()

def cmd_domain(args, session):
    if not args:
        print(f"  {C.MUTED}Usage: /domain <text to classify>{C.RESET}")
        return
    d = detect_domain(" ".join(args))
    print(f"  {C.GREEN}Domain:{C.RESET} {d}")
    print(f"  {C.MUTED}{DOMAIN_PERSONAS[d][:80]}...{C.RESET}")

def cmd_use(args, session):
    if not args or args[0] not in PROVIDERS:
        keys = ", ".join(PROVIDERS.keys())
        print(f"  {C.MUTED}Usage: /use <provider> — options: {keys}{C.RESET}")
        return
    session["preferred"] = args[0]
    p = PROVIDERS[args[0]]
    print(f"  {p['color']}Locked to {p['label']}{C.RESET}")

def cmd_file(args, session):
    if not args:
        print(f"  {C.MUTED}Usage: /file <path>{C.RESET}")
        return
    path = " ".join(args)
    content = ingest_file(path)
    session["pending_file"] = content
    print(f"  {C.GREEN}File queued — include it in your next message.{C.RESET}")

def cmd_clear(args, session):
    session["history"] = []
    session["pending_file"] = None
    print(f"  {C.MUTED}Context cleared.{C.RESET}")

def cmd_history(args, session):
    h = session["history"]
    if not h:
        print(f"  {C.MUTED}No history yet.{C.RESET}")
        return
    for i, msg in enumerate(h):
        role  = msg["role"]
        snip  = msg["content"][:80].replace("\n", " ")
        color = C.CYAN if role == "user" else C.GHOST
        print(f"  {color}[{i}] {role:<10}{C.RESET} {snip}...")

def cmd_help(args, session):
    cmds = [
        ("/help",            "Show this"),
        ("/providers",       "Show provider status + keys"),
        ("/use <provider>",  "Lock to a specific provider"),
        ("/file <path>",     "Ingest a file into next prompt"),
        ("/domain <text>",   "Detect domain of text"),
        ("/clear",           "Clear conversation history"),
        ("/history",         "Show conversation history"),
        ("/exit  /quit",     "Quit Syntax"),
    ]
    print(f"\n{C.BOLD}  Commands{C.RESET}")
    print(f"{C.MUTED}  {'─'*46}{C.RESET}")
    for cmd, desc in cmds:
        print(f"  {C.GREEN}{cmd:<22}{C.RESET}{C.MUTED}{desc}{C.RESET}")
    print()

COMMANDS = {
    "/help":      cmd_help,
    "/providers": cmd_providers,
    "/use":       cmd_use,
    "/file":      cmd_file,
    "/clear":     cmd_clear,
    "/history":   cmd_history,
    "/domain":    cmd_domain,
}

# ── One-shot mode ─────────────────────────────────────────────────────────────
def one_shot(prompt: str, files: list, preferred: str, temperature: float):
    file_context = ""
    for fp in (files or []):
        file_context += ingest_file(fp) + "\n"

    full_prompt = (file_context + "\n" + prompt).strip() if file_context else prompt
    domain      = detect_domain(full_prompt)
    system      = DOMAIN_PERSONAS[domain]

    messages = [
        {"role": "system",  "content": system},
        {"role": "user",    "content": full_prompt},
    ]

    spinner = Spinner(f"querying ({domain})")
    spinner.start()
    try:
        response, used = call_with_fallback(messages, preferred=preferred, temperature=temperature)
    finally:
        spinner.stop()

    render_response(response, used)

# ── Interactive loop ──────────────────────────────────────────────────────────
def interactive_loop(preferred: str, temperature: float):
    session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    session = {
        "id":           session_id,
        "history":      [],
        "preferred":    preferred,
        "pending_file": None,
    }

    print_logo()
    print_provider_status()
    print(f"  {C.MUTED}Type your message. /help for commands. /exit to quit.{C.RESET}\n")

    while True:
        try:
            raw = input(f"{C.GREEN}syntax{C.RESET}{C.MUTED}>{C.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{C.MUTED}  Syntax out.{C.RESET}")
            break

        if not raw:
            continue

        # Commands
        if raw.startswith("/"):
            parts = raw.split()
            cmd   = parts[0].lower()
            args  = parts[1:]
            if cmd in ("/exit", "/quit"):
                print(f"\n{C.MUTED}  Syntax out.{C.RESET}")
                break
            handler = COMMANDS.get(cmd)
            if handler:
                handler(args, session)
            else:
                print(f"  {C.MUTED}Unknown command: {cmd}. Try /help{C.RESET}")
            continue

        # Build prompt
        user_content = raw
        if session["pending_file"]:
            user_content = session["pending_file"] + "\n\n" + raw
            session["pending_file"] = None

        # Build messages
        domain = detect_domain(user_content)
        system = DOMAIN_PERSONAS[domain]
        messages = [{"role": "system", "content": system}] + session["history"] + [
            {"role": "user", "content": user_content}
        ]

        # Trim history to last 10 exchanges (20 msgs) to stay under context limits
        if len(session["history"]) > 20:
            session["history"] = session["history"][-20:]

        spinner = Spinner(f"{domain}")
        spinner.start()
        try:
            response, used = call_with_fallback(
                messages,
                preferred=session["preferred"],
                temperature=temperature,
            )
        except RuntimeError as e:
            spinner.stop()
            print(f"  {C.RED}ERROR: {e}{C.RESET}")
            continue
        finally:
            spinner.stop()

        render_response(response, used)

        # Update history
        session["history"].append({"role": "user",      "content": raw})
        session["history"].append({"role": "assistant",  "content": response})

        # Log
        log_exchange(session_id, "user",      raw,      "")
        log_exchange(session_id, "assistant", response, used)

# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    # Load .env files from known RootBase locations
    for env_path in [
        "/storage/emulated/0/RootBase/Official-Vertical-AI-Boardroom/.env",
        "/storage/emulated/0/RootBase/Askhole-Too-Also/V3/.env",
        "/storage/emulated/0/RootBase/.env",
        str(Path.home() / ".syntax.env"),
        ".env",
    ]:
        load_env_file(env_path)

    parser = argparse.ArgumentParser(
        prog="syntax",
        description="Syntax — CLI AI Warden for Termux/RootBase",
    )
    parser.add_argument("prompt",         nargs="*",          help="One-shot prompt (omit for interactive)")
    parser.add_argument("-f", "--file",   action="append",    help="Ingest file(s) into prompt", dest="files")
    parser.add_argument("-p", "--provider", default=None,     help="Preferred provider (cerebras|mistral|openrouter|groq|gemini)")
    parser.add_argument("-t", "--temp",   type=float, default=0.7, help="Temperature (default 0.7)")
    parser.add_argument("--providers",    action="store_true", help="List provider status and exit")
    args = parser.parse_args()

    if args.providers:
        print_logo()
        print_provider_status()
        return

    if args.prompt:
        one_shot(
            prompt    = " ".join(args.prompt),
            files     = args.files,
            preferred = args.provider,
            temperature = args.temp,
        )
    else:
        interactive_loop(
            preferred   = args.provider,
            temperature = args.temp,
        )

if __name__ == "__main__":
    main()
