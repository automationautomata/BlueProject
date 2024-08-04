from threading import Thread
import websocket
import json

from singleton import Singleton

class VisitsWebsocketClient(Singleton):    
    def __init__(self, url) -> None:
        self.url = url
    
    def send_message(ws: websocket.WebSocketApp, data) -> bool:
        try:
            ws.send(json.dump(data))
            return True
        except:
            return False

    def on_message(ws: websocket.WebSocketApp, data) -> None:
        print(data)
        try:
            msg = json.loads(data)
        except:
            print("ERROR", data)

    def on_error(ws: websocket.WebSocketApp, error) -> None:
        print(error)

    def on_close(ws: websocket.WebSocketApp, close_status_code, close_msg) -> None:
        print("### closed ###")

    def on_open(ws: websocket.WebSocketApp) -> None:
        print("Opened connection")

def make_websocket_client(server_url: str) -> tuple[websocket.WebSocketApp, Thread]:
    websocket.enableTrace(True)
    visits_ws = VisitsWebsocketClient(url=server_url)
    ws = websocket.WebSocketApp(server_url, on_open=visits_ws.on_open,
                                     on_message=visits_ws.on_message,
                                     on_error=visits_ws.on_error,
                                     on_close=visits_ws.on_close)
    return ws, Thread(target=ws.run_forever, daemon=True)

