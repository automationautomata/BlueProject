# import sqlite3
# connection = sqlite3.connect(".\\DB\\SKUD")
# cursor = connection.cursor()
# # Создаем базу
# with open(".\\dbscripts\\skud_script.sql", "r+") as scriptfile:
#     script = scriptfile.read()
#     cursor.executescript(script)
#     connection.commit()

import json
import sys
import os
from threading import Thread
from tornado.websocket import WebSocketHandler
import time
from typing import Any, Callable
import tornado
sys.path.append(os.getcwd())

from ORM.database import DatabaseConnection
from intercom.ui_db import UiSkudController
from remote.ui import Answer


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
    def initialize(self, actions):
        self.actions = actions

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


skud_db = DatabaseConnection(scriptpath=".\\dbscripts\\skud_script.sql",
                             name="SKUD", dirpath=".\\DB\\")
ui = UiSkudController(skud_db=skud_db)
app = tornado.web.Application([
    (r"/", SkudQueryHandler, dict(actions=ui.action_query_map())),
    (r"/wss", VisitsWebSocket, dict(actions=None))
])
app.listen(8080)
app.get_handler_delegate
Thread(target=tornado.ioloop.IOLoop.current().start, daemon=True).start()

time.sleep(2)
