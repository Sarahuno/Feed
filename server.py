import asyncio
import websockets
import os

OUTPUT_PREFIX = "- OUTPUT -"
RETRIEVE_COMMAND = "retrieve=OUTPUT"

# In-memory output store
output_storage = ""

# Handle each client connection
async def echo(websocket, path):
    global output_storage
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")

            # Save message to output storage
            if message.startswith(OUTPUT_PREFIX):
                content = message[len(OUTPUT_PREFIX):].lstrip()
                output_storage += content + "\n"
                await websocket.send("Output saved in memory.")

            # Retrieve stored output
            elif message.strip() == RETRIEVE_COMMAND:
                await websocket.send(f"Stored Output:\n{output_storage.strip()}")

            # Regular echo
            else:
                await websocket.send(f"Echo: {message}")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")

# Start the WebSocket server
async def main():
    port = int(os.environ.get("PORT", 8765))  # Render sets PORT env var
    async with websockets.serve(echo, "0.0.0.0", port):
        print(f"WebSocket server running on ws://0.0.0.0:{port}")
        await asyncio.Future()  # Keep running

if __name__ == "__main__":
    asyncio.run(main())
