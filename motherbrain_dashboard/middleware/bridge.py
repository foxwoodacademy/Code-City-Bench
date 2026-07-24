import asyncio
import json
import websockets
import aiohttp
from aiohttp import web
import os
import sys

# Paths
LOG_FILE = os.path.expanduser("~/.zeroclaw/workspace/audit.log")
DASHBOARD_FILE = "/storage/emulated/0/RootBase/motherbrain_dashboard/dashboard.html"
ZEROCLAW_API = "http://127.0.0.1:7082"

# State
connected_clients = set()

async def tail_log():
    """Tails the audit log in a non-blocking background loop."""
    print("[BRIDGE] Background log tailer initialized.")
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("[SYSTEM] Audit log initialized.\n")

    with open(LOG_FILE, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                await asyncio.sleep(0.2)
                continue
            if connected_clients:
                message = line.strip()
                asyncio.create_task(broadcast_message(message))

async def broadcast_message(message):
    if connected_clients:
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )

async def ws_handler(websocket):
    """Handles incoming WebSocket connections."""
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def serve_dashboard(request):
    """Serves dashboard.html securely over HTTP to bypass Android file restrictions."""
    if os.path.exists(DASHBOARD_FILE):
        with open(DASHBOARD_FILE, "r") as f:
            return web.Response(text=f.read(), content_type='text/html')
    return web.Response(status=404, text=f"Missing dashboard UI file at: {DASHBOARD_FILE}")

async def post_task(request):
    """Forwards POST requests straight to the backend gateway."""
    try:
        data = await request.json()
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{ZEROCLAW_API}/tasks", json=data) as resp:
                text = await resp.text()
                return web.Response(status=resp.status, text=text, content_type='application/json')
    except Exception as e:
        return web.Response(status=500, text=json.dumps({"error": str(e)}))

async def main():
    """Unified entry point running cleanly inside an explicit asyncio context."""
    app = web.Application()
    app.router.add_get('/dashboard', serve_dashboard)
    app.router.add_post('/tasks', post_task)
    
    # 1. Start HTTP Server on 7083
    runner = web.AppRunner(app)
    await runner.setup()
    http_site = web.TCPSite(runner, '127.0.0.1', 7083)
    await http_site.start()
    print("[BRIDGE] HTTP Dashboard Server live at http://127.0.0.1:7083/dashboard")

    # 2. Start WebSocket Server on 7084
    async with websockets.serve(ws_handler, "127.0.0.1", 7084):
        print("[BRIDGE] WebSocket Log Stream live at ws://127.0.0.1:7084")
        
        # 3. Spawn log tailer as an un-awaited task so it doesn't block
        asyncio.create_task(tail_log())
        
        # Keep everything alive
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[BRIDGE] Shutting down gracefully.")
