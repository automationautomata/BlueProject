import json
from typing import Any, Callable
import tornado
from threading import Thread
class Answer:
    def __init__(self, data: Any, error: str) -> None:
        self.data = data
        self.error = error
    def toJSON(self) -> str:
        return json.dumps(self.__dict__)
    
tokens = set()

class SkudQueryHandler(tornado.web.RequestHandler):
    def initialize(self, actions: dict[str, Callable[[str], Answer]]) -> None:
        self.actions = actions
        
    def get(self) -> None:
        if self.get_body_argument("token") in tokens:
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            print(answer.toJSON())
            self.write(answer.toJSON())
        
    def post(self) -> None:
        if self.get_body_argument("token") in tokens:
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())

    def put(self) -> None:
        if self.get_body_argument("token") in tokens:
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())

    def delete(self) -> None:
        if self.get_body_argument("token") in tokens:
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())

class AuthenticationHandler(tornado.web.RequestHandler):
    def initialize(self, verificator: Callable[[str], Answer]):
        self.verificator = verificator

    def get(self) -> None:
        answer = self.verificator(self.get_body_argument("auth"))
        self.write(answer.toJSON())

##        random.randint(a, b)

def create_tornado_server(actions, port: int, isdaemon: bool = True) -> tuple[Thread, tornado.web.Application]:
    app = tornado.web.Application([
        (r"/", SkudQueryHandler, dict(actions=actions))
    ])
    app.listen(port)
    return Thread(target=tornado.ioloop.IOLoop.current().start, daemon=isdaemon), app
