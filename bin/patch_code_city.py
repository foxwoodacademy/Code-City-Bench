"""
patch_code_city.py
Injects a live field event feed into code_city.html.
Handles SD card copy internally — run from anywhere.
"""

import shutil, re
from pathlib import Path

SRC  = Path("/storage/ED7B-AD5A/root_2026/code_city.html")
TMP  = Path("/data/data/com.termux/files/home/code_city_patched.html")
DEST = SRC  # push back to same location

CSS = """
    <style id="field-feed-styles">
      #field-feed {
        position: fixed; bottom: 0; left: 0; right: 0;
        height: 160px;
        background: rgba(0,0,0,0.82);
        border-top: 1px solid #6B1A2A;
        font-family: 'Courier New', monospace;
        font-size: 11px;
        overflow: hidden;
        z-index: 999;
        display: flex;
        flex-direction: column;
      }
      #field-feed-header {
        padding: 3px 10px;
        background: #0e0c09;
        color: #6B1A2A;
        letter-spacing: 0.4em;
        font-size: 9px;
        text-transform: uppercase;
        border-bottom: 1px solid #2a1a1a;
        flex-shrink: 0;
      }
      #field-feed-log {
        flex: 1;
        overflow: hidden;
        padding: 4px 0;
        display: flex;
        flex-direction: column-reverse;
      }
      .ff-line {
        padding: 1px 10px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        animation: ff-in 0.3s ease;
      }
      @keyframes ff-in { from { opacity:0; transform:translateY(4px); } to { opacity:1; } }
      .ff-zeroclaw { color: #c0404a; }
      .ff-jane     { color: #C4A882; }
      .ff-manual   { color: #6a9fd8; }
      .ff-system   { color: #556655; }
      .ff-default  { color: #8a8070; }
    </style>
"""

HTML_PANEL = """
    <div id="field-feed">
      <div id="field-feed-header">Field Event Bus &nbsp;&#x2F;&nbsp; Live</div>
      <div id="field-feed-log"></div>
    </div>
"""

JS = """
    <script id="field-feed-script">
    (function() {
      const log   = document.getElementById('field-feed-log');
      const MAX   = 12;
      let lastTs  = Date.now() / 1000 - 30; // seed: last 30s of history

      const COLOR_MAP = {
        zeroclaw: 'ff-zeroclaw',
        jane:     'ff-jane',
        manual:   'ff-manual',
        system:   'ff-system',
      };

      function addLine(e) {
        const cls  = COLOR_MAP[e.source_layer] || 'ff-default';
        const div  = document.createElement('div');
        div.className = 'ff-line ' + cls;
        div.textContent =
          '[' + e.time_str + ']  ' +
          (e.source_layer || '?').padEnd(16) + '  ' +
          (e.event_type   || '?').padEnd(32) + '  @ ' +
          (e.location     || '?');
        log.prepend(div);
        while (log.children.length > MAX) log.removeChild(log.lastChild);
      }

      function pulse() {
        fetch('http://localhost:7070/poll?since=' + lastTs + '&limit=8')
          .then(r => r.json())
          .then(events => {
            if (!events || !events.length) return;
            // events come newest-first; reverse to add oldest first so feed looks correct
            [...events].reverse().forEach(e => {
              addLine(e);
              if (e.timestamp > lastTs) lastTs = e.timestamp;
            });
          })
          .catch(() => {}); // silent fail — server may not be running
      }

      // seed with last 30s then poll every 3s
      pulse();
      setInterval(pulse, 3000);
    })();
    </script>
"""

def patch():
    print(f"[PATCH] Reading {SRC}")
    html = SRC.read_text(encoding="utf-8")

    if "field-feed-script" in html:
        print("[PATCH] Already patched. Remove existing patch first if you want to re-patch.")
        return

    # Inject CSS before </head>
    html = html.replace("</head>", CSS + "\n</head>", 1)

    # Inject panel div after <body>
    html = html.replace("<body>", "<body>\n" + HTML_PANEL, 1)

    # Inject JS before </body>
    html = html.replace("</body>", JS + "\n</body>", 1)

    print(f"[PATCH] Writing to temp: {TMP}")
    TMP.write_text(html, encoding="utf-8")

    print(f"[PATCH] Pushing back to SD: {DEST}")
    shutil.copy2(str(TMP), str(DEST))
    TMP.unlink()

    print("[PATCH] Done. Open code_city.html and run field_server if not already running.")
    print("        python ~/lough_system/field_server.py &")

if __name__ == "__main__":
    patch()
