import asyncio
import os
from aiohttp import web
import websockets
import threading

OUTPUT_PREFIX = "- OUTPUT -"
RETRIEVE_COMMAND = "retrieve=OUTPUT"
output_storage = ""

# WebSocket handler
async def websocket_handler(websocket):
    global output_storage
    try:
        async for message in websocket:
            print(f"Received: {message}")

            if message.startswith(OUTPUT_PREFIX):
                content = message[len(OUTPUT_PREFIX):].lstrip()
                output_storage += content + "\n"
                await websocket.send("Output saved in memory.")
            elif message.strip() == RETRIEVE_COMMAND:
                await websocket.send(f"Stored Output:\n{output_storage.strip()}")
            else:
                await websocket.send(f"Echo: {message}")
    except Exception as e:
        print(f"WebSocket error: {e}")

# HTTP health check (Render expects this)
async def health_check(request):
    return web.Response(text="Server is up")

# aiohttp app
def start_http_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    port = int(os.environ.get("PORT", 8765))
    web.run_app(app, port=port)

# WebSocket server runs on a separate thread
async def start_websocket_server():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(websocket_handler, "0.0.0.0", port + 1):  # +1 to avoid port conflict
        print(f"WebSocket server running on ws://0.0.0.0:{port + 1}")
        await asyncio.Future()

if __name__ == "__main__":
    threading.Thread(target=start_http_server, daemon=True).start()
    asyncio.run(start_websocket_server())
