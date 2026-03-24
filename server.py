import asyncio

from json import dumps, loads
from websockets.asyncio.server import serve


rooms: dict[str, dict] = {}
for num in range(1, 6):
    rooms[f"room{num}"] = {
        "users": set(),
        "messages": list(),
        }


async def broadcast(room_id, message, exclude=None):
    for client in rooms[room_id]["users"]:
        if client != exclude:
            await client.send(message)


async def handler(websocket):
    try:
        user = await websocket.recv()
        user = loads(user)
        user, room_id = user['name'], user['room']
        greeting = f"{user} зашёл в комнату {room_id}!"
        for message in rooms[room_id]["messages"]:
            await websocket.send(message)
        await broadcast(room_id, greeting, exclude=websocket)
        rooms[room_id]["users"].add(websocket)
        async for message in websocket:
            await broadcast(room_id, f"{user} пишет: {message}", exclude=websocket)
            rooms[room_id]["messages"].append(f"{user} написал: {message}")
            # if message == "/users":
            #    for user in rooms[room_id]["users"]:
            #        await websocket.send(user)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await broadcast(room_id, f"{user} покинул комнату {room_id}!", exclude=websocket)
        rooms[room_id]["users"].remove(websocket)


async def main():
    async with serve(handler, "127.0.0.1", 8765) as server:
        print("Запущен сервер ws://127.0.0.1:8765")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
