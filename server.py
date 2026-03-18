import asyncio

from websockets.asyncio.server import serve


async def hello(websocket):
    try:
        name = await websocket.recv()
        print(f"<<< {name}")
        greeting = f"Hello {name}!"
        await websocket.send(greeting)
        print(f">>> {greeting}")
    except Exception as e:
        print(f"Error: {e}")


async def main():
    async with serve(hello, "127.0.0.1", 8765) as server:
        print("Server started on ws://127.0.0.1:8765")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
