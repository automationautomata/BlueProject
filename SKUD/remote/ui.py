import json
from typing import Any, Callable
import tornado
from tornado.websocket import WebSocketHandler
from threading import Thread

class Answer:
    def __init__(self, data: Any, error: str) -> None:
        self.data = data
        self.error = error
    def toJSON(self) -> str:
        return json.dumps(self.__dict__)
    
class SkudQueryHandler(tornado.web.RequestHandler):
    def initialize(self, actions: dict[str, Callable[[str], Answer]]) -> None:
        self.actions = actions

    def get(self) -> None:
        answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
        print(answer.toJSON())
        self.write(answer.toJSON())

    def post(self) -> None:
        answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write(answer.toJSON())

    def put(self) -> None:
        answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write(answer.toJSON())

    def delete(self) -> None:
        answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write(answer.toJSON())

class VisitsWebSocket(WebSocketHandler):
    def initialize(self, actions: dict[str, Callable[[str], Answer]]) -> None:
        self.actions = actions

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")