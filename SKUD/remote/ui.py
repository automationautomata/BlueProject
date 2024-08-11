import json
from threading import Thread
from typing import Callable
import tornado
from tornado.websocket import WebSocketHandler

from remote.tools import Actions, Answer, WebsoketClients


class AuthenticationHandler(tornado.web.RequestHandler):
    '''Класс для аутентификации'''
    def initialize(self, verificator: Callable[[str], Answer]):
        self.verificator = verificator

    def get(self) -> None:
        answer = self.verificator(self.get_body_argument("auth"))
        self.write(answer.toJSON())


class QueryHandler(tornado.web.RequestHandler):
    '''Класс для обработки CRUD запросов'''
    def initialize(self, action: Actions) -> None:
        self.actions = action.action_query_map()
        self.verify = action.verify

    def get(self) -> None:
        headers = self.request.headers
        if self.verify(token=headers.get("X-Auth"), id=headers.get("X-Id")):
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            print(answer.toJSON())
            self.write(answer.toJSON())
        
    def post(self) -> None:
        headers = self.request.headers
        if self.verify(token=headers.get("X-Auth"), id=headers.get("X-Id")):
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())

    def put(self) -> None:
        headers = self.request.headers
        if self.verify(token=headers.get("X-Auth"), id=headers.get("X-Id")):
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())

    def delete(self) -> None:
        headers = self.request.headers
        if self.verify(token=headers.get("X-Auth"), id=headers.get("X-Id")):
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())


class Websoket(WebSocketHandler):
    def initialize(self, action: Actions) -> None:
        self.actions = action.action_query_map()
        self.verify = action.verify
        self.clients = WebsoketClients()
    
    def open(self):
        self.id = self.clients.add(self)
        print("WebSocket opened")

    def on_message(self, data):
        msg = json.loads(data)
        if self.veryfy(msg["token"]):
            self.actions[msg["action"]]
        self.write_message(f"You said: {data}")

    def on_close(self):
        self.clients.remove(self.id)
        print("WebSocket closed")


def create_tornado_server(port: int, auth: Callable[[str], Answer],
                          skud: Actions, visits: Actions, 
                          isdaemon: bool = True) -> tuple[Thread, tornado.web.Application]:
    '''Создает поток, обрабатывыающий запросы от десктоп приложений.
    `port` - номер сокета, skud - обрабатывает сообщения от клиента к БД СКУДа,
    `visits` - обрабатывает сообщения от клиента к БД посещений,
    `auth` - функция, производящяя аутентификацию, 
    `isdaemon` - подчиненный ли поток по отношению к главному.'''
    app = tornado.web.Application([
        (r"/", AuthenticationHandler, dict(verificator=auth)),
        (r"/ui", QueryHandler, dict(action=skud)),
        (r"/wss", Websoket, dict(actions=visits))
    ])
    
    app.listen(port)
    return Thread(target=tornado.ioloop.IOLoop.current().start, daemon=isdaemon), app
