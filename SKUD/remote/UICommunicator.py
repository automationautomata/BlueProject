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

# Надо разделить на клиента и сервер
# Надо отладить и проверить, сейчас это чисто для тестов
class UiCommunicator:
    def __init__(self, router: dict[str, Callable[[str], str]], url="ws://localhost:8080") -> None:
        self.url = url
        self.router = router

    def connect(self) -> None:
        '''Осуществляет соединение с сервером'''
        self.websocket = websocket.WebSocketApp(self.url, on_message=self.handler)
        self.websocket.run_forever() 

    def handler(self, ws: websocket.WebSocketApp, message: str) -> None:
        '''Обрабатывает принытые сообщение, сообщение должно быть в формате json.\n
        Поле `action` - функция которую надо вызвать, `data` - данные которые надо добавить/удалить/взять'''
        try: 
            msg = json.loads(message)
            func = self.router[msg['action']]
            answer = func(msg['data'])
            ws.send(answer)
        except NameError:
            print(f"message: {message}")
            print(NameError)
