Bardildo — Docs

Overview

Bardildo is a snarky CLI bard that scans the RootBase workspace, generates per-project manifest/runbook previews, and provides "buddy" tools for quick triage: DustBunny (dup/entropy hunter), Summarizer (exec briefs), Archivist (release manifest helper), and QA (test discovery). Default behavior is preview-only and non-destructive.

Where it lives

/storage/emulated/0/RootBase/tools/bardildo/
- bardildo.py        CLI entry
- run_bardildo.sh    wrapper script
- bardildo-cli.sh    convenience wrapper
- dustbunny.py       entropy/duplicate scanner (preview-first)
- summarizer.py      summarizer stub
- archivist.py       archivist stub
- qa.py              qa/test discovery stub
- README.md, DOCS.md (this file)

Termux safety notes

- Uses $TMPDIR for temporary outputs; falls back to Termux path.
- Never mutates files unless explicit flags (--write, --write-plan) are provided.
- Avoids in-place sed and unsafe operations on SD card paths.
- Recommended project paths you mentioned are supported: /storage/emulated/0/BleakNarratives and /storage/ED7B-AD5A/root_2026 — pass full path to --target or --path.

Quick install / alias (one-liner for shell rc)

alias bardildo='python3 /storage/emulated/0/RootBase/tools/bardildo/bardildo.py --root /storage/emulated/0/RootBase --write --headless'

Usage examples

# Full scan and write per-folder manifest.json + runbook.txt, print to console
python3 tools/bardildo/bardildo.py --root /storage/emulated/0/RootBase --write --headless

# Run DustBunny preview for one project
python3 tools/bardildo/dustbunny.py --path /storage/emulated/0/RootBase/molt_bleak --preview

# Run a buddy from the main CLI (prints output)
python3 tools/bardildo/bardildo.py --buddy dustbunny --target /storage/emulated/0/RootBase/molt_bleak

# Produce archive suggestion plan (written to $TMPDIR) after preview
python3 tools/bardildo/dustbunny.py --path <proj> --preview --write-plan

Buddy descriptions

- dustbunny: Finds duplicate files (by sha256), large files, and old files. Produces a safe archive plan under $TMPDIR when asked.
- summarizer: Exec brief generator (stub). Later: wire to Ollama personas.
- archivist: Release manifest / changelog helper (stub). Preview-only.
- qa: Quick test discovery and counts.

Why preview-only

Your stack and mobile constraints require conservative operations. Bardildo surfaces risk and gives you control to accept or reject suggested changes.

Next recommended steps (pick any)

1) Wire buddies to local Ollama models (Modelfile personas) for richer persona output (Askhole, Pummelizer, Fartographer, etc.).
2) Add interactive TUI to browse projects and run buddies.
3) Add scheduled nightly scan that writes a short dashboard manifest to a single summary file.
4) Integrate Archivist with ZeroClaw/OpenClaw for marketplace postings (requires auth hooks).

If you want me to implement any next step, say which one and I’ll proceed. Also tell me whether to auto-write manifests by default or keep preview-only (current default: preview-only).