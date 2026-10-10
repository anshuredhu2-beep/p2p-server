import asyncio
import websockets
import json
import os

connected_clients = set()

async def register(websocket):
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")

async def unregister(websocket):
    connected_clients.remove(websocket)
    print(f"Client disconnected: {websocket.remote_address}")

async def handler(websocket, path=""):
    await register(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister(websocket)

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Server started on port {port}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
