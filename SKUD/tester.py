
from threading import Thread
import threading
import time
from typing import Any, Callable
import tornado

from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger
from controllers.auth_controller import AuthenticationController
from controllers.ui_controllers import UiSKUDController
from remote.tools import Answer


class QueryHandler(tornado.web.RequestHandler):
    def initialize(self, action) -> None:
        self.actions = action.actions_map()
        self.verify = action.verify

    def prepare(self): 
        headers = self.request.headers
        if not self.verify(token=headers.get("X-Auth"), id=headers.get("X-Id")):
            self.write(Answer(None, "verification faild").toJSON())
            self.finish()
    
    def get(self, param) -> None:
        print(threading.get_native_id(), self.get_body_argument("data"))
        answer = self.actions[param]['get'](self.get_body_argument("data"))
        #print(answer.toJSON())
        self.write(answer.toJSON())
        
    def post(self, param) -> None:
        answer = self.actions[param]['post'](self.get_body_argument("data"))
        #print(answer.toJSON())
        self.write(answer.toJSON())

    def put(self, param) -> None:
        answer = self.actions[param]['put'](self.get_body_argument("data"))
        #print(answer.toJSON())
        self.write(answer.toJSON())

    def delete(self, param) -> None:
        answer = self.actions[param]['delete'](self.get_body_argument("data"))
        #print(answer.toJSON())
        self.write(answer.toJSON())

class AuthenticationHandler(tornado.web.RequestHandler):
    def initialize(self, authenticatior: Callable[[str], Answer]):
        self.authenticatior = authenticatior

    def get(self) -> None:
        answer = self.authenticatior(self.get_body_argument("auth"))
        self.write(answer.toJSON())


skud_db = DatabaseConnection(scriptpath=".\\dbscripts\\skud_script.sql",
                             name="SKUD", dirpath=".\\DB")
visits = VisitLogger(scriptpath=".\\dbscripts\\visits_script.sql",
                     name="visits", dirpath=".\\DB")

a = AuthenticationController(0, visits, skud_db)

ui = UiSKUDController(skud_db=skud_db)
app = tornado.web.Application([
    (r"/ui/(.*)", QueryHandler, dict(action=ui)), 
    (r"/auth", AuthenticationHandler, dict(authenticatior=a.authenticatior))
    ])
app.listen(8080)

Thread(target=tornado.ioloop.IOLoop.current().start, daemon=True).start()
time.sleep(200)