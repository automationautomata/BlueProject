
from threading import Thread
import threading
import time
from typing import Any, Callable
import tornado

from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger
from intercom.auth_controller import AuthenticationController, UiSKUDController
from remote.tools import Answer


class QueryHandler(tornado.web.RequestHandler):
    def initialize(self, action) -> None:
        self.actions = action.action_query_map()
        self.verify = action.verify

    def get(self) -> None:
        print(threading.get_native_id())
        print(self.request.headers) 
        headers = self.request.headers
        if self.verify(token=headers.get("X-Auth"), id=headers.get("X-Id")):
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            print(answer.toJSON())
            self.write(answer.toJSON())
        
    def post(self) -> None:
        if self.verify(self.request.headers.get("auth")):
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())

    def put(self) -> None:
        if self.verify(self.request.headers.get("auth")):
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())

    def delete(self) -> None:
        if self.verify(self.request.headers.get("auth")):
            answer = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
            self.set_header("Content-Type", "text/plain")
            self.write(answer.toJSON())

class AuthenticationHandler(tornado.web.RequestHandler):
    def initialize(self, verificator: Callable[[str], Answer]):
        self.verificator = verificator

    def get(self) -> None:
        answer = self.verificator(self.get_body_argument("auth"))
        self.write(answer.toJSON())


skud_db = DatabaseConnection(scriptpath=".\\SKUD\\dbscripts\\skud_script.sql",
                             name="SKUD", dirpath=".\\SKUD\\DB")
visits = VisitLogger(name="visits", dirpath=".\\SKUD\\DB")

a = AuthenticationController(0, visits, skud_db)

ui = UiSKUDController(skud_db=skud_db)
app = tornado.web.Application([
    (r"/ui+", QueryHandler, dict(action=ui)), 
    (r"/auth", AuthenticationHandler, dict(verificator=a.verificator))
    ])
app.listen(8080)

Thread(target=tornado.ioloop.IOLoop.current().start, daemon=True).start()
time.sleep(200)