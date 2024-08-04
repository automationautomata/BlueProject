# import sqlite3
# connection = sqlite3.connect(".\\DB\\SKUD")
# cursor = connection.cursor()
# # Создаем базу
# with open(".\\dbscripts\\skud_script.sql", "r+") as scriptfile:
#     script = scriptfile.read()
#     cursor.executescript(script)
#     connection.commit()

import json
from threading import Thread
import time
from typing import Any, Callable
import tornado

from ORM.database import DatabaseConnection
from intercom.ui_db import UiController
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

# class VisitsWebSocket(tornado.websocket.WebSocketHandler):
#     def initialize(self, actions):
#         self.actions = actions
#     def open(self):
#         print("WebSocket opened")

#     def on_message(self, message):
#         self.write_message(u"You said: " + message)

#     def on_close(self):
#         print("WebSocket closed")
skud_db = DatabaseConnection(scriptpath=".\\dbscripts\\skud_script.sql",
                             name="SKUD", dirpath=".\\DB\\")
ui = UiController(skud_db=skud_db)
app = tornado.web.Application([
    (r"/", SkudQueryHandler, dict(actions=ui.action_query_map()))
])
app.listen(8080)
def st():
    tornado.ioloop.IOLoop.current().start()
Thread(target=tornado.ioloop.IOLoop.current().start, daemon=True).start()

time.sleep(2)