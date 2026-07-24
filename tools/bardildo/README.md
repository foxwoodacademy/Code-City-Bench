Bardildo — The Snarky Repo Bard

What it does
- Scans the RootBase workspace and produces a manifest.json and runbook.txt for each top-level project folder.
- Detects entrypoints, languages, dependencies, and suggests run commands.
- Writes a short, sarcastic "bard_note" for each project to help triage and surface likely issues.

Usage
- In Termux or any Linux shell:
  python3 bardildo.py --root /storage/emulated/0/RootBase --write

Notes
- This tool is intended for quick triage and organization. It is non-destructive and only writes manifest.json and runbook.txt files inside each scanned folder when --write is passed.
- The tone is intentionally rude. Adjust the persona by editing `VOICE` in bardildo.py if you'd prefer a gentler bard.
