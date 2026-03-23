import asyncio

from json import loads
from websockets.asyncio.server import serve


rooms: dict[str, set] = {}
for num in range(1, 6):
    rooms[f"room{num}"] = set()


async def hello(websocket):
    try:
        user = await websocket.recv()
        user = loads(user)
        print(f"<<< На сервер заходит {user['name']}")
        greeting = f"Привет {user['name']} из комнаты {user['room']}!"
        await websocket.send(greeting)
        print(f">>> {greeting}")
        async for message in websocket:
            print(f"Сообщение в {user['room']} от {user['name']}: {message}")

    except Exception as e:
        print(f"Error: {e}")


async def main():
    async with serve(hello, "127.0.0.1", 8765) as server:
        print("Запущен сервер ws://127.0.0.1:8765")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
