import asyncio
from websockets.asyncio.server import serve

from .ws_handler import custom_handler, redis_subscriber


async def main():
    asyncio.create_task(redis_subscriber())
    async with serve(custom_handler, "localhost", 8765) as server:
        print("WebSocket Server 1 running on ws://localhost:8765")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())