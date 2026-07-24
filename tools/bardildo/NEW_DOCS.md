Updates: Ollama-backed buddies, TUI, and scheduled scans

New features added:
- ollama_client.py: lightweight wrapper to call local Ollama HTTP API.
- summarizer_ollama.py, archivist_ollama.py, qa_ollama.py: Ollama-backed persona buddies. They call the local model and return persona-flavored output.
- tui.py: curses-based TUI to browse projects and invoke buddies interactively.
- scheduled_scan.py + schedule_run.sh: run periodic scans and write JSON summaries to $TMPDIR (Termux-friendly).

Usage notes
- Ollama: set OLLAMA_URI to your local Ollama instance if different from default (http://127.0.0.1:11434).
- TUI: run python3 tools/bardildo/tui.py (Termux terminal must support curses). Use arrows to navigate, Enter to run buddy.
- Scheduler: run tools/bardildo/schedule_run.sh to start a background scan; it writes summaries to $TMPDIR.

Safety and behavior
- All operations are preview-only by default. scheduled_scan writes summary JSON but does not mutate project files.
- DustBunny's --write-plan writes archive suggestions to $TMPDIR only.

If you want Ollama personas mapped to specific Modelfile entries, provide model names and I'll add a persona mapping file.
