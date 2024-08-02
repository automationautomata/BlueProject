import tornado
from abc import ABC
from typing import Callable
from threading import Thread

from remote.ui import Answer, SkudQueryHandler

class Actions(ABC):
    def action_query_map(self) -> dict[str, Callable[[str], Answer]]:
        pass

def create_tornado_server(port: int, skud_actions: Actions, 
                          visits_actions: Actions, isdaemon: bool = True) -> tuple[Thread, tornado.web.Application]:
    app = tornado.web.Application([
        (r"/", SkudQueryHandler, dict(actions=skud_actions.action_query_map())),
        (r"/", SkudQueryHandler, dict(actions=visits_actions.action_query_map()))
    ])
    app.listen(port)
    return Thread(target=tornado.ioloop.IOLoop.current().start, daemon=isdaemon), app
