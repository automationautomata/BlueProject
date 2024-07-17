import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        #print(message)
        #print("----------")
        await websocket.send("message")

async def main():
    async with serve(echo, "localhost", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())

