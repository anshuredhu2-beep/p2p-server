import asyncio
import websockets
import json

connected_clients = set()

async def register(websocket):
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")

async def unregister(websocket):
    connected_clients.remove(websocket)
    print(f"Client disconnected: {websocket.remote_address}")

async def handler(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Broadcast message to all other connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister(websocket)

start_server = websockets.serve(handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
