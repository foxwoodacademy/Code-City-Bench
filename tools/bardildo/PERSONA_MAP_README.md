Persona Map Auto-populate

What
- Script: populate_persona_map.py
- Purpose: detect local Ollama models and create tools/bardildo/persona_map.json mapping persona IDs to model names and prompt prefixes.

Usage (on target device)
1. Ensure Ollama is running and reachable: export OLLAMA_URI="http://127.0.0.1:11434"
2. Go to the bardildo folder: cd /path/to/RootBase/tools/bardildo
3. Dry-run to preview: python3 populate_persona_map.py --dry-run
4. Write persona_map.json: python3 populate_persona_map.py

Notes
- The script prefers models smaller than 2GB to be friendly on mobile devices.
- If you already have persona_map.json, the script preserves prompt_prefix values when possible.
