# import asyncio
# from websockets.server import serve

# async def echo(websocket):
#     async for message in websocket:
#         #print(message)
#         #print("----------")
#         await websocket.send("messag    e")

# async def main():
#     async with serve(echo, "localhost", 8080):
#         await asyncio.Future()  # run forever

# asyncio.run(main())

import json
import websocket
from typing import Callable

class UiCommunicator:
    def __init__(self, router: dict[str, Callable[[str], str]], url="ws://localhost:8080") -> None:
        self.url = url
        self.router = router

    def connect(self) -> None:
        self.websocket = websocket.WebSocketApp(self.url, on_message=self.handler)
        self.websocket.run_forever() 

    def handler(self, ws: websocket.WebSocketApp, message: str) -> None:
        print(message)
        msg = json.loads(message)
        func = self.router[msg['action']]
        answer = func(msg['data'])
        ws.send(answer)