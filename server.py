import asyncio
import websockets
import os

OUTPUT_PREFIX = "- OUTPUT -"
OUTPUT_FILE = "output.txt"

# Handle each client connection
async def echo(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            if message.startswith(OUTPUT_PREFIX):
                content = message[len(OUTPUT_PREFIX):].lstrip()
                with open(OUTPUT_FILE, "a") as f:
                    f.write(content + "\n")
                await websocket.send("Saved to output.txt")
            else:
                await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")

# Start the WebSocket server
async def main():
    port = int(os.environ.get("PORT", 8765))  # Render sets PORT env var
    async with websockets.serve(echo, "0.0.0.0", port):
        print(f"WebSocket server running on ws://0.0.0.0:{port}")
        await asyncio.Future()  # Keep server running

if __name__ == "__main__":
    asyncio.run(main())
