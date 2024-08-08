
############################# CLIENT #############################


from threading import Thread
import threading
from typing import Any, Callable
import tornado

from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger
from intercom.ui_db import AuthenticationController, UiSKUDController
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

############################# CLIENT #############################

import json
from typing import Any
import requests

from general.singleton import Singleton

from requests.auth import AuthBase

class TokenAuth(AuthBase):
    """Присоединяет HTTP аутентификацию к объекту запроса."""
    def __init__(self, token, id):
        # здесь настроем любые данные, связанные с аутентификацией 
        self.token = token
        self.id = id

    def __call__(self, req):
        # изменяем и возвращаем запрос
        if self.token:
            req.headers['X-Auth'] = self.token
            req.headers['X-Id'] = self.id
        return req


class SkudApiRequsts(Singleton):
    def __init__(self, url: str) -> None:
        self.url = url
        self.token = None
        self.id = None

    def get(self, body: Any, path="") -> requests.Response | None:
        try:
            response = requests.get(self.url+path, data=body, auth=TokenAuth(self.token, self.id))
            if response.status_code == 200:
                return response
            else:
                print(f"Ошибка {response.status_code}: {response.reason}")
        except Exception as error:
            print("get ERR", error)

    def fmt(self, action, data) -> dict:
        return {"action": action, 
                "data"  : json.dumps(data)}
    
    def get_table(self, table: str, start: int, order_column: str, order_type: bool) -> dict | None:
        action = f"{table} query"
        data = {"start"       : start, 
                "order_type"  : order_type, 
                "order_column": order_column}
 
        response = self.get(self.fmt(action,  data), "/ui")
        try: 
            return response.json()
        except Exception as error:
            print("response:", response.text if response else "None", 
                  "ERR:", error)
        
    def authentication(self, key: int) -> tuple[bool, str]:
        data = json.dumps({"key": key, "id": self.id})
        response = self.get({"auth": data}, "/auth")
        try:
            answer = response.json()
            print(answer)

            err = "answer is None"
            if answer:
                err = answer["error"]
                if err == "":
                    self.token = answer["data"]
                    return True, err
            return False, err
        except BaseException as error:
            return False, error

api = SkudApiRequsts(url="http://localhost:8080")
print("url", api.url)
api.id = 2
while True:
    if input() == "auth":
        print("err, ", api.authentication(12))
    elif input() == "get":
        print("req", api.get_table("entities", 0, "card", False))
    else:
        break