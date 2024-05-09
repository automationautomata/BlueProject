import websocket
import asyncio
# def on_open(ws):
#     print("Connection opened")
    
 
# def on_message(ws, message):
#     print(f"Received message: {message}")
 
# def on_close(ws):
#     print("Connection closed")

# ws.run_forever()
class UICommunicator:
    async def connect(self, path):
        self.path = path
        self.websocket = websocket.WebSocketApp("ws://example.com/ws", on_open=on_open,
                                                 on_message=on_message, on_close=on_close) 
        self.websocket.send("Hello")
    async def handler(self, path):
        message = await self.websocket.recv()
        await self.websocket.send(f"Hello, {message}!")